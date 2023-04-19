import requests
from config import API_key
import json


'''
STEP 1:
Get transaction history of a collection
'''

# TO DO

'''
STEP 2:
Get nfts from top 100 highest transactions (metadata + image)
'''

url = "https://api.nftport.xyz/v0/nfts/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d?chain=ethereum&page_number=1&page_size=50&include=metadata&refresh_metadata=false"

headers = {
    "accept": "application/json",
    "Authorization": API_key
}

response = requests.get(url, headers=headers)

# print response to a file as json
with open("response.json", "w") as f:
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
