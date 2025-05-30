#!/usr/bin/env python3
import os
import requests
import json
import shutil
from tqdm import tqdm

# Define the path to read images from
IMAGE_DIR = "/home/ecotrace/fotos/0431/2025/04/15"
# Define the output folder path
OUTPUT_DIR = "./output"
# API endpoint
API_URL = "http://127.0.0.1:8000/classifier/classify_image"

def main():
    # Create the output folder if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        tqdm.write(f"Created output directory: {OUTPUT_DIR}")

    # Get all image files from the specified directory
    try:
        image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    except FileNotFoundError:
        tqdm.write(f"Error: Directory {IMAGE_DIR} not found.")
        return
    except PermissionError:
        tqdm.write(f"Error: Permission denied to access {IMAGE_DIR}.")
        return

    # Sort the image files alphabetically
    image_files.sort()

    tqdm.write(f"Found {len(image_files)} images in {IMAGE_DIR}")

    # Process each image with progress bar
    for image_file in tqdm(image_files, desc="Processing images", unit="image"):
        image_path = os.path.join(IMAGE_DIR, image_file)

        # Make the POST request
        try:
            # For classify_image endpoint, we need to pass the image_path parameter
            payload = {'image_path': image_path}
            files = []
            headers = {}

            response = requests.request("POST", API_URL, headers=headers, data=payload, files=files)

            # Print response status code and content for debugging
            tqdm.write(f"Response status code: {response.status_code}")
            tqdm.write(f"Response content: {response.text[:100]}...")  # Print first 100 chars

            # Parse the response JSON
            try:
                response_json = response.json()

                # Extract only the 'result' part
                if 'result' in response_json:
                    result_data = response_json['result']

                    # Get the classification_name from the result (or fall back to classification_id)
                    if 'classification_name' in result_data and result_data['classification_name']:
                        classification_folder_name = str(result_data['classification_name'])
                    elif 'classification_id' in result_data:
                        classification_folder_name = str(result_data['classification_id'])
                    else:
                        tqdm.write(f"✗ Error: Neither 'classification_name' nor 'classification_id' found in result for {image_file}")
                        continue

                    # Create a folder with the classification_name
                    classification_folder = os.path.join(OUTPUT_DIR, classification_folder_name)
                    if not os.path.exists(classification_folder):
                        os.makedirs(classification_folder)
                        tqdm.write(f"Created classification directory: {classification_folder}")

                    # Copy the input image to the classification folder
                    destination_image = os.path.join(classification_folder, image_file)
                    try:
                        shutil.copy2(image_path, destination_image)
                        tqdm.write(f"✓ Image copied to: {destination_image}")
                    except Exception as copy_error:
                        tqdm.write(f"✗ Error copying image: {str(copy_error)}")

                    # Save the result data as JSON in the classification folder
                    output_file = os.path.join(classification_folder, f"{os.path.splitext(image_file)[0]}.json")
                    with open(output_file, 'w') as f:
                        json.dump(result_data, f)

                    tqdm.write(f"✓ Result saved: {output_file}")
                else:
                    tqdm.write(f"✗ Error: 'result' key not found in response for {image_file}")
            except json.JSONDecodeError as json_error:
                tqdm.write(f"✗ Error parsing JSON response for {image_file}: {str(json_error)}")
                tqdm.write(f"Raw response: {response.text}")

        except Exception as e:
            tqdm.write(f"✗ Error processing {image_file}: {str(e)}")

if __name__ == "__main__":
    main()