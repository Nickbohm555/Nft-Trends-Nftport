# import json file and count the number of items

import json


# with open("all_nfts_3.json", "r") as f:
#     data = json.load(f)
"""
# Count the number of NFTs
num_nfts = 0
for i in range(len(data)):
    num_nfts += len(data[i]["nfts"])

print(f"Total number of NFTs: {num_nfts}")
"""
# =============================================================================

# Get the image url of each NFT
"""
image_urls = []
for i in range(len(data)):
    for j in range(len(data[i]["nfts"])):
        try:
            image_urls.append(data[i]["nfts"][j]["metadata"]["image"])
        except TypeError:
            continue

print(len(image_urls))

# send _urls to a file
with open("image_url_3.json", "w") as f:
    json.dump(image_urls, f, indent=2)
"""

# import image_urls_test.json file
with open("image_urls_test2.json", "r") as f:
    image_urls = json.load(f)

# # count lenght of file (number of image urls)
# # print(len(image_urls))

# loop through items in image_urls_test.json and remove items of length greater than 200
for i in range(len(image_urls)):
    try:
        if len(image_urls[i]) > 200:
            image_urls.pop(i)
        # if it starts with "ipfs://" removit it and replace with "https://gateway.ipfs.io/ipfs/"
        elif image_urls[i].startswith("ipfs://"):
            image_urls[i] = "https://gateway.ipfs.io/ipfs/" + image_urls[i][7:]
        # if it doesn't start with "https://" add "https://gateway.ipfs.io/ipfs/"
        elif not image_urls[i].startswith("https://"):
            image_urls[i] = "https://gateway.ipfs.io/ipfs/" + image_urls[i]
    except IndexError:
        break
print(len(image_urls))

# write new list to file
with open("image_urls_test2.json", "w") as f:
    json.dump(image_urls, f, indent=2)
"""
# download image from url
import requests

url = image_urls[0]
response = requests.get(url)

with open("image.jpg", "wb") as f:
    f.write(response.content)
"""
