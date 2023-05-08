# Discovering NFT Trends w/ NFTPort Data, IPFS, & Property Analysis

## Abstract
NFT trend analysis can be valuable for numerous reasons. Firstly, it can provide insights into the popularity and demand for different types of NFTs, which can help creators and investors make informed decisions about what types of NFTs to create or invest in.

Secondly, NFT trend analysis can also help identify patterns and trends in the NFT market, such as seasonal fluctuations or the impact of current events or cultural phenomena. Understanding these trends can provide valuable information to creators and investors on when and how to release their NFTs to maximize their exposure and potential profits.

Finally, NFT trend analysis can also provide insights into the behavior of buyers and collectors in the NFT market, such as their preferences for certain marketplaces or their willingness to pay higher prices for certain types of NFTs. This information can help creators and investors better understand their target audience and make more informed decisions about pricing and distribution strategies.

Overall, NFT trend analysis can be a valuable tool for anyone involved in the NFT market, providing valuable insights and information that can help maximize their success in this emerging digital asset space.

## Background
NFTs, or non-fungible tokens, are unique digital assets that are verified on a blockchain network, which ensures that the asset is one-of-a-kind and cannot be duplicated or replaced. NFTs are a rapidly growing sector in the digital asset space, with a lot of potential for creators and collectors alike.

For this project, we used [NFTPort](https://www.nftport.xyz/) and their [API](https://docs.nftport.xyz/docs) to collect NFT data for analysis. NFTPort is a blockchain-based platform that simplifies the process of creating, managing, and selling NFTs for creators, artists, and businesses. NFTPort provides a user-friendly interface that enables creators to mint their NFTs and launch them on various marketplaces, such as OpenSea and Rarible, without needing technical knowledge of blockchain technology. The platform also offers features such as automatic royalties and access control, making it easier for creators to monetize their NFTs and control their distribution. With NFTPort, creators can tap into the growing market for NFTs and benefit from the increased demand for digital ownership and authenticity.


## Step 1: User Input - Get Count of NFT Collections

- The program asks the user to input a count of NFT (Non-Fungible Token) collections to get.
- The count is stored as an integer in the count variable.
- The input function is used to receive user input and the int function is used to convert the input into an integer.
- The prompt message provided to the user specifies that the input count should not exceed 50.
- The count variable is later used in the processNFTs function to determine how many NFT collections to retrieve from an external source.

## Step 2: Getting NFTs - Processing NFTs

- Retrieves the top 50 selling NFT contracts.
- Retrieves NFT details, including metadata and image, for each of the top 50 contracts.
- Retrieves transaction data for each NFT.
- Creates a list of NFTs with the following information: contract address, token ID, image URL, metadata, and transaction data.
- The processNFTs() function takes a number as input, which specifies the number of NFTs to process, and returns a list of processed NFTs.
- The code limits the number of NFTs retrieved from each contract to 10.

## Step 3: Store NFT Data in Firebase

- Store data in a Firebase database using the Firebase Admin SDK for Python.
- The firebase_admin package is imported, along with credentials and db modules.
- The databaseURL is imported from a config file.
- A credential certificate is created using firebase_config.json.
- The Firebase app is initialized with this certificate and the databaseURL using firebase_admin.initialize_app.
- The writeFB function is defined to take in data and write it to the Firebase database.
- The function loops through each item in the data list, which represents the NFTs, and pushes each item to the Firebase database using the set method.

![Firebase Screenshot](https://github.com/Nickbohm555/Nft-Trends-Nftport/blob/main/firebase/firebase_setup.png)
**NOTE:** Check [here](https://github.com/Nickbohm555/Nft-Trends-Nftport/blob/main/firebase/data_sample.json) for sample data from Firebase.

## Step 4: User Input - Get Top NFTs to Analyze

- Retrieve the latest NFTs (non-fungible tokens) to analyze from a Firebase database.
- The function getImagesFB(count) retrieves a list of image URLs from the Firebase database.
- The count parameter specifies the latest number of images to retrieve.
- If count is set to "all", then all the images in the database are retrieved.
- The function iterates through the latest NFTs based on the date they were collected, then extracts the image URL associated with each NFT.
- The image URLs are stored in a list, which is returned by the function.

## Step 5: Analyzing NFTs - Top 5 Most Common Colors

- Use the getTop20ImageRGB(image_url) function to analyze the colors in an image.
- The function takes an image URL as an input and returns a list of the 20 most common colors in the image.
- The function uses the OpenCV library to read the image data from the URL.
- The function converts the image to grayscale and applies binary thresholding to create a binary image.
- It then finds contours in the binary image and extracts color information for each contour.
- The function creates a dictionary to store color counts and iterates through the contours to add each color to the dictionary or increment its count.
- The function sorts the color counts by count in descending order and returns the 20 most common colors as a list.
- Finally, the function displays the image with detected objects.

**NOTE:** The pre-trained YOLO v3 weights file is too large to upload to GitHub, but you can download it to the `objectDetectionFiles` folder using this in your terminal:

```python
wget https://pjreddie.com/media/files/yolov3.weights
```

## Step 6: Analyzing NFTs - Top 5 Most Common Attributes

- To analyze NFTs, the getImageObjects(image_url) function is used
- The function takes an image URL as an input and returns a list of objects found in the image
- YOLOv3 object detection algorithm is used to identify objects in the image
- Configuration files for the algorithm are loaded and output layers are retrieved
- The function processes the image using the YOLOv3 algorithm and identifies the classes of objects found in the image
- A list of the objects found in the image is returned

## Step 7: Print Results - Top 5 Colors and Attributes

- The main function calls the getImagesFB(count) function to retrieve the latest NFTs to analyze
- Iterates through the list of image URLs and calls the getTop20ImageRGB(image_url) function to extract the 20 most common colors in each image
- The getImageObjects(image_url) function is called to extract the objects in each image
- The top 5 most common colors and objects for each image are printed to the console

## Step 8: Display Results - Top 5 Colors Plot

- To visualize the top 5 most common colors in an image, the getTop20ImageRGB(image_url) function is used
- The function takes an image URL as an input and returns a list of the 20 most common colors in the image
- OpenCV library is used to read the image data from the URL
- The image is converted to grayscale and binary thresholding is applied to create a binary image
- Contours are found in the binary image and color information is extracted for each contour
- A dictionary is created to store color counts and iterate through the contours to add each color to the dictionary or increment its count
- The color counts are sorted by count in descending order and the 20 most common colors are returned as a list
- A bar chart of the top 5 most common colors for each image is displayed using the matplotlib library.

## Results
![Results Screenshot](https://github.com/Nickbohm555/Nft-Trends-Nftport/blob/main/media/results.png)

### Demo
https://user-images.githubusercontent.com/89931114/236924723-2d070c2b-1d0b-4d27-a611-c30b4be58060.mp4

## Future Work

We believe this work can be extended for a number of future projects:
- Analyze trends over time
- Use the results to create an NFT
- Make predictions about what kinds of NFTs will be popular in the future

## Contributors
- [Keir Keenan](https://github.com/keirkeenan)
- [Nick Bohm](https://github.com/Nickbohm555)

Check out our other projects!
