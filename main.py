import requests
from config import API_key
import json

headers = {"accept": "application/json", "Authorization": API_key}


"""
STEP 1:
Get All transactions history of a collection. Using 'Retrieve All Transactions API. Get only sales'
"""

url = "https://api.nftport.xyz/v0/contracts/top?page_size=50&page_number=1&period=24h&order_by=sales&chain=ethereum&chain=polygon"

response = requests.get(url, headers=headers)


# TODO now have to sort based on price here
str = response.text
res = json.loads(str)
info = []
all_contracts = res["contracts"]
for contract in all_contracts:
    print("--------------------------")
    print(contract)
    contract_address = contract["contract_address"]
    print(contract_address)
    info.append(contract_address)


with open("all_top_contracts.json", "w") as f:
    json.dump(response.json(), f, indent=2)


"""
STEP 2:
Get nfts from top 100 highest transactions (metadata + image) 'Retrieve NFT details' of specific contract address of NFT
"""

# Should have a list of all 100 contract addresses with highest transactions


def get_image_urls(num):
    # get items for each contract address
    image_urls = set()
    for i in range(num):
        items = []
        contract_address = info[i]
        print(contract_address)

        url = f"https://api.nftport.xyz/v0/nfts/{contract_address}?chain=ethereum&page_number=1&page_size=50&include=metadata&refresh_metadata=false"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            items.append(response.json())
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        # get image url of each NFT (for each contract address)

        for i in range(len(items)):
            for j in range(len(items[i]["nfts"])):
                try:
                    image_urls.add(items[i]["nfts"][j]["metadata"]["image"])
                except (TypeError, KeyError):
                    continue

    # send image_urls to a file
    image_urls = list(image_urls)
    with open("image_urls_test.json", "w") as f:
        json.dump(image_urls, f, indent=2)

    return len(image_urls)


get_image_urls(50)

# # print response to a file as json
# with open("all_nfts_1.json", "w") as f:
#     json.dump(items, f, indent=2)


"""
STEP 3:
Get image from ipfs
"""

# url = "https://gateway.ipfs.io/ipfs/QmRRPWG96cmgTn2qSzjwr2qvfNEuhunv6FNeMFGa9bx6mQ"
# response = requests.get(url)

# with open("image.jpg", "wb") as f:
#     f.write(response.content)


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
