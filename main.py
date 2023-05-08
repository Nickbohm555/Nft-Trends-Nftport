import requests
from config import API_key
import json
import datetime

headers = {"accept": "application/json", "Authorization": API_key}

"""
STEP 1:
Get 50 top selling contracts by sales.
"""


def getTopSellingContracts():
    """
    Returns a list of the top 50 selling contracts.

    returns: list of top 50 selling contracts
    """
    url = "https://api.nftport.xyz/v0/contracts/top?page_size=50&page_number=1&period=24h&order_by=sales&chain=ethereum&chain=polygon"

    response = requests.get(url, headers=headers)

    str = response.text
    res = json.loads(str)
    info = []
    all_contracts = res["contracts"]
    for contract in all_contracts:
        contract_address = contract["contract_address"]
        info.append(contract_address)

    # with open("top_contracts.json", "w") as f:
    #     json.dump(response.json(), f, indent=2)

    return info


"""
STEP 2 & 3:
2) Get nfts from top 50 highest transactions (metadata + image) 'Retrieve NFT details' of specific contract address of NFT
3) Get image from ipfs
4. Get transaction data
"""


def createImageUrl(image):
    """
    Returns a url for an image.

    image: hash of image
    returns: image url
    """
    # remove faulty items
    if len(image) > 200:
        return None
    # if it starts with "ipfs://" removit it and replace with "https://gateway.ipfs.io/ipfs/"
    elif image.startswith("ipfs://"):
        image = "https://gateway.ipfs.io/ipfs/" + image[7:]
    # if it doesn't start with "https://" add "https://gateway.ipfs.io/ipfs/"
    elif not image.startswith("https://"):
        image = "https://gateway.ipfs.io/ipfs/" + image
    return image


def getImageHash(image):
    """
    Returns the hash of an image.

    image
    returns: image hash
    """
    if image.startswith("https://ipfs.io/ipfs/"):
        hash = image.split("/")[4]
        return hash
    elif image.startswith("ipfs://"):
        hash = image.split("//")[1].split("/")[0]
        return hash
    elif image.startswith("https://arweave.net/"):
        hash = image.split("/")[3]
        return hash
    else:
        return image


def getTransactionData(contract_address, token_id):
    """
    Returns transaction data for a specific NFT.

    contract_address: contract address of NFT
    token_id: token id of NFT

    returns: transaction data
    """
    transaction_data = []
    url = f"https://api.nftport.xyz/v0/transactions/nfts/{contract_address}/{token_id}?chain=ethereum&page_size=50&type=sale"
    response = requests.get(url, headers=headers)
    transaction_data.append(response.json())
    try:
        if transaction_data[0]["response"] == "OK":
            return transaction_data
        else:
            return None
    except KeyError:
        return None


def processNFTs(num):
    """
    Returns a list of NFTs with the following information:
    - contract_address
    - token_id
    - image_url
    - metadata
    - transaction_data

    num: number of NFTs to process
    returns: list of NFTs
    """
    # print("Collecting NFT data...")

    info = getTopSellingContracts()

    NFTs_all = []
    for i in range(num):
        contract_address = info[i]

        url = f"https://api.nftport.xyz/v0/nfts/{contract_address}?chain=ethereum&page_number=1&page_size=50&include=metadata&refresh_metadata=false"

        try:
            # retrieve NFT details
            response = requests.get(url, headers=headers)

            response.raise_for_status()
            NFTs_all.append(response.json())
        except requests.exceptions.RequestException as e:
            # print(f"An error occurred: {e}")
            continue

    NFTs_limited = []
    for nfts in NFTs_all:
        for i, nft in enumerate(nfts["nfts"][:10]):  # limit to 10
            # get transaction data using contract address and token id
            contract_address = nft["contract_address"]
            token_id = nft["token_id"]
            transaction_data = getTransactionData(contract_address, token_id)
            try:
                NFT = {
                    "contract_address": contract_address,
                    "token_id": token_id,
                    "image_url": createImageUrl(nft["metadata"]["image"]),
                    "image_hash": getImageHash(nft["metadata"]["image"]),
                    "metadata": nft["metadata"],
                    "transaction_data": transaction_data[0]["transactions"],
                    "date_collected": datetime.datetime.timestamp(
                        datetime.datetime.now()
                    ),
                }
                if NFT["image_url"] is not None and NFT["transaction_data"] is not None:
                    NFTs_limited.append(NFT)
            except (TypeError, KeyError):
                continue

    # include timestamp in filename
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d")

    # with open(f"NFTs_limited_{timestamp}.json", "w") as f:
    #     json.dump(NFTs_limited, f, indent=2)

    # print(f"Number of NFTs: {len(NFTs_limited)}")

    return NFTs_limited


# EXAMPLE:
# processNFTs(50)


"""
STEP 4:
Store data in Firebase DB
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from config import databaseURL

# configure db
cred = credentials.Certificate("firebase_config.json")
default_app = firebase_admin.initialize_app(cred, {"databaseURL": databaseURL})


# write to db
def writeFB(data):
    """
    Writes data to Firebase DB.

    data: data to write
    """

    ref = db.reference("/")
    # with open(data, "r") as f:
    #     file_contents = json.load(f)
    for nft in data:
        ref.push().set(nft)

    return


# EXAMPLE:
# writeFB("NFTs_limited_2023-05-04.json")

"""
STEP 5:
1) Read data from Firebase DB
2) Image feature extraction
"""


def getImagesFB(count):
    """
    Returns a list of image urls from Firebase DB.

    count: latest number of images to retrieve
    returns: list of image urls
    """
    # print("Retrieving image urls from Firebase DB...")

    images = []
    if count == "all":
        for nft in ref.get():
            r = db.reference(f"{nft}/image_url")
            image_url = r.get()
            images.append(image_url)
    else:
        r = db.reference("/")
        nfts = r.order_by_child("date_collected").limit_to_last(count).get()

        for nft in nfts:
            image_url = nfts[nft]["image_url"]
            images.append(image_url)

    # print("Image urls retrieved!")
    return images


import cv2
import numpy as np
import io
import requests
import webcolors


def getTop20ImageRGB(image_url):
    """
    Returns the RGB values of the 20 most common colors in an image.

    image_url: url of image
    returns: list of RGB values
    """
    top5_colors = []

    # Load image from URL
    url = image_url
    response = requests.get(url)
    binary_data = io.BytesIO(response.content)

    # Read binary data as image
    img = cv2.imdecode(
        np.frombuffer(binary_data.read(), np.uint8), cv2.IMREAD_UNCHANGED
    )

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply binary thresholding to create binary image
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Find contours in binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create dictionary to store color counts
    color_counts = {}
    colors = []
    # Iterate through contours and extract color information
    for contour in contours:
        # Get bounding box coordinates
        x, y, w, h = cv2.boundingRect(contour)

        # Extract object from image
        object_img = img[y : y + h, x : x + w]

        # Get mean color values of object
        object_color = cv2.mean(object_img)[:3]

        # Round color values to nearest 10 to reduce color noise
        object_color = tuple([int(round(c / 10.0)) * 10 for c in object_color])

        # Add color to dictionary or increment count
        if object_color in color_counts:
            color_counts[object_color] += 1
        else:
            color_counts[object_color] = 1

        # Convert BGR to RGB
        rgb_color = tuple(reversed(object_color))
        # Get closest color name
        # Get closest color name
        try:
            closest_name = webcolors.hex_to_name(webcolors.rgb_to_hex(rgb_color))
        except ValueError:
            closest_name = "unknown"
        colors.append(closest_name)

        # Draw bounding box around object
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Sort color counts by count in descending order
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)

    # Print main colors
    # print("Main colors:")
    for color, count in sorted_colors[:20]:
        # print("- {}: {}".format(color, count))
        top5_colors.append(color)

    # Display image with detected objects
    # cv2.imshow("Detected Objects", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return top5_colors


from PIL import Image


def getImageObjects(image_url):
    """
    Returns a list of objects found in the image at the given URL.

    params:
        url (str): The URL of the image to be analyzed.

    returns:
        objects (list): A list of objects found in the image.
    """

    objects = []

    # setup files
    config = "objectDetectionFiles/yolov3.cfg"
    weights = "objectDetectionFiles/yolov3.weights"
    classes_names = "objectDetectionFiles/yolov3.txt"

    def get_output_layers(net):
        layer_names = net.getLayerNames()
        try:
            output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        except:
            output_layers = [
                layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()
            ]

        return output_layers

    def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
        label = str(classes[class_id])

        color = COLORS[class_id]

        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

        cv2.putText(
            img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
        )

    # Load image from URL
    response = requests.get(image_url)
    binary_data = io.BytesIO(response.content)

    # Open the image from binary data as a PIL image
    pil_image = Image.open(binary_data).convert("RGB")

    # Convert the PIL image to a NumPy array
    image_array = np.array(pil_image)

    # Convert the NumPy array to a cv2 image
    image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    classes = None

    with open(classes_names, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    net = cv2.dnn.readNet(weights, config)

    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        try:
            box = boxes[i]
        except:
            i = i[0]
            box = boxes[i]

        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(
            image,
            class_ids[i],
            confidences[i],
            round(x),
            round(y),
            round(x + w),
            round(y + h),
        )
        objects.append(classes[class_ids[i]])

    # cv2.imshow("object detection", image)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    return objects


# EXAMPLE:
# url = "https://img.freepik.com/premium-photo/man-stands-hilltop-with-phone-his-hands-against-background-thick-fog-empty-bench-young-man-standing-it-concept-loneliness-longing_678914-3743.jpg"
# # print(getImageObjects(url))
# print(getImageRGB(url))


"""
STEP 6:
Analysis of image features
"""
from collections import Counter


def getTopImageColors(count):
    """
    Returns a list of the 5 most common colors found in the images.

    params:
        count (int): The number of images to be analyzed.

    returns:
        colors (list): A list of colors found in the images.
    """

    colors = []

    image_urls = getImagesFB(count)

    for image_url in image_urls:
        try:
            for color in getTop20ImageRGB(image_url):
                colors.append(color)
        except:
            continue

    # Count occurrences of each color
    color_counts = Counter(colors)

    # Get top 5 most common colors
    top_c = color_counts.most_common(5)
    top_colors = [t[0] for t in top_c]

    return top_colors


def getTopImageAttributes(count):
    """
    Returns a list of the top 5 image attributes from Firebase (metadata) + image feature extraction.

    params:
        count (int): The number of images to analyze.

    returns:
        attributes (list): A list of the top 5 image attributes.
    """

    attributes = []

    image_urls = getImagesFB(count)

    for image_url in image_urls:
        for attribute in getImageObjects(image_url):
            attributes.append(attribute)

    if count == "all":
        for nft in ref.get():
            features = db.reference(f"{nft}/metadata/attributes").get()
            try:
                for feature in features:
                    attribute = (feature["trait_type"], feature["value"])
                    attributes.append(attribute)
            except TypeError:
                continue

    else:
        r = db.reference("/")
        nfts = r.order_by_child("date_collected").limit_to_last(count).get()
        for nft in nfts:
            features = db.reference(f"{nft}/metadata/attributes").get()
            try:
                for feature in features:
                    attribute = (feature["trait_type"], feature["value"])
                    attributes.append(attribute)
            except TypeError:
                continue

    # Count occurrences of each attribute
    attribute_counts = Counter(attributes)

    # Get top 5 most common attributes
    top_attr = attribute_counts.most_common(5)
    top_attributes = [t[0] for t in top_attr]

    return top_attributes


"""
STEP 7:
Create a recommendation system
"""

import matplotlib.pyplot as plt


def main():
    """ """

    # get count from user input
    count = int(input("Enter the number of NFT collections to get (up to 50): "))

    # get NFTs
    print("Getting NFTs...")
    nfts = processNFTs(count)

    # write NFTs to Firebase
    print("Storing NFT data in Firebase...")
    writeFB(nfts)

    # get top 5 most common colors
    num = int(input("Enter the number of NFTs to analyze (type number or 'all'): "))

    print("Analyzing NFTs...")
    top_colors = getTopImageColors(num)

    # get top 5 most common attributes
    top_attributes = getTopImageAttributes(num)

    # print results
    print("===========================================")
    print("RESULTS")
    print("===========================================")
    print(f"Top 5 colors: {top_colors}")
    print(f"Top 5 attributes: {top_attributes}")

    # display colors
    def display_colors(colors):
        fig, ax = plt.subplots(figsize=(len(colors), 1))
        ax.imshow([colors], aspect="auto", extent=(0, len(colors), 0, 1))
        ax.set_axis_off()
        plt.show()

    display_colors(top_colors)

    return


if __name__ == "__main__":
    main()
