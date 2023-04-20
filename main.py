import requests
from config import API_key
import json

headers = {
    "accept": "application/json",
    "Authorization": API_key
}


'''
STEP 1:
Get All transactions history of a collection. Using 'Retrieve All Transactions API. Get only sales'
'''

url = "https://api.nftport.xyz/v0/transactions?chain=ethereum&page_size=50&type=sale"

response = requests.get(url, headers=headers)

# TODO now have to sort based on price here 
str = response.text
res = json.loads(str)
info = {}
all_transactions = res['transactions']
for transaction in all_transactions:
    print('--------------------------')
    print(transaction)
    contract_address = transaction['nft']['contract_address']
    print(contract_address)
    price_usd = transaction['price_details']['price_usd']
    print(price_usd)
    info[contract_address] = price_usd


sorted_transactions = sorted(info.items(), key=lambda x:x[1])

print(sorted_transactions)
print(len(sorted_transactions))

with open("all_transactions.json", "w") as f:
    json.dump(response.json(), f, indent=2)


'''
STEP 2:
Get nfts from top 100 highest transactions (metadata + image) 'Retrieve NFT details' of specific contract address of NFT
'''

# Should have a list of all 100 contract addresses with highest transactions
for i in range(100):
    j = 0

url = "https://api.nftport.xyz/v0/nfts/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d?chain=ethereum&page_number=1&page_size=50&include=metadata&refresh_metadata=false"


response = requests.get(url, headers=headers)

# print response to a file as json
with open("all_nfts.json", "w") as f:
    json.dump(response.json(), f, indent=2)


'''
STEP 3:
Get image from ipfs
'''

# url = "https://gateway.ipfs.io/ipfs/QmRRPWG96cmgTn2qSzjwr2qvfNEuhunv6FNeMFGa9bx6mQ"
# response = requests.get(url)

# with open("image.jpg", "wb") as f:
#     f.write(response.content)


'''
STEP 4:
Store image in database (MongoDB)
'''

# TO DO


'''
STEP 5:
Image feature extraction
'''

# TO DO


'''
STEP 6:
Analysis of image features
'''

# TO DO


'''
STEP 7:
Create a recommendation system
'''

# TO DO

'''
STEP 8:
Create a web app
'''

# TO DO
