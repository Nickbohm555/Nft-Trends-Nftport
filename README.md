### Nft-Trends-OpenSea


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



