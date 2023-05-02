import requests
from config import API_key
import json

headers = {"accept": "application/json", "Authorization": API_key}


"""
STEP 1:
Get 50 top selling contracts by sales.
"""


def getTopSellingContracts():
    url = "https://api.nftport.xyz/v0/contracts/top?page_size=50&page_number=1&period=24h&order_by=sales&chain=ethereum&chain=polygon"

    response = requests.get(url, headers=headers)

    str = response.text
    res = json.loads(str)
    info = []
    all_contracts = res["contracts"]
    for contract in all_contracts:
        contract_address = contract["contract_address"]
        info.append(contract_address)

    with open("top_contracts.json", "w") as f:
        json.dump(response.json(), f, indent=2)
    return info


"""
STEP 2 & 3:
2) Get nfts from top 50 highest transactions (metadata + image) 'Retrieve NFT details' of specific contract address of NFT
3) Get image from ipfs
"""


def get_image_urls(num):
    info = getTopSellingContracts()

    image_urls = set()
    metadata_limited = []

    tokens = []
    tokens_limited = []

    image_dictionary = {}
    for i in range(num):
        items = []
        contract_address = info[i]

        url = f"https://api.nftport.xyz/v0/nfts/{contract_address}?chain=ethereum&page_number=1&page_size=50&include=metadata&refresh_metadata=false"

        try:
            # retrieve NFT details
            response = requests.get(url, headers=headers)

            response.raise_for_status()
            items.append(response.json())
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        items_image = []
        metadata_all = []
        for i in range(len(items)):
            try:
                for j in range(len(items[i]["nfts"])):
                    # image_urls.add(items[i]["nfts"][j]["metadata"]["image"])
                    items_image.append(items[i]["nfts"][j]["metadata"]["image"])
                    metadata_all.append(items[i]["nfts"][j]["metadata"])

                    tokens.append(items[i]["nfts"][j]['token_id'])

                    
            except (TypeError, KeyError):
                continue

        
        for i in range(10):
            try:
                image_urls.add(items_image[i])
                metadata_limited.append(metadata_all[i])
                tokens_limited.append(tokens[i])

            except IndexError:
                break

    image_urls = list(image_urls)

    # cleaning - loop through image_urls and remove faulty items
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

    with open("image_urls_top_nfts.json", "w") as f:
        json.dump(image_urls, f, indent=2)

    with open("metadata.json", "w") as f:
        json.dump(metadata_limited, f, indent=2)


    with open("tokens.json", "w") as f:
            json.dump(tokens_limited, f, indent=2)

    return image_urls


get_image_urls(50)



"""
STEP 4A:
Get transaction data for these NFT's
"""
def getTransactionData():
    url = "https://api.nftport.xyz/v0/transactions/nfts/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/567?chain=ethereum&page_size=50&type=sale"
    response = requests.get(url, headers=headers)
    
    with open("transactionData.json", "w") as f:
        json.dump(response.json(), f, indent=2)


getTransactionData()
"""
STEP 4:
Get image binary data and store to database
"""


"""
STEP 4:
Store image in database (MongoDB)
"""

# TO DO


"""
STEP 5:
Image feature extraction
"""

# TO DO


"""
STEP 6:
Analysis of image features
"""

# TO DO


"""
STEP 7:
Create a recommendation system
"""

# TO DO

"""
STEP 8:
Create a web app
"""

# TO DO
