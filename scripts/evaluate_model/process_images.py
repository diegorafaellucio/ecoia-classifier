#!/usr/bin/env python3
import os
import requests
import json
from tqdm import tqdm

# Define the path to read images from
IMAGE_DIR = "/home/ecotrace/fotos/0431/2025/04/15"
# Define the output folder path
OUTPUT_DIR = "../output"
# API endpoint
API_URL = "http://127.0.0.1:8000/classifier/evaluate_model"

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
            payload = {'model': 'meat'}
            files = [
                ('image', (image_file, open(image_path, 'rb'), 'image/jpeg'))
            ]
            headers = {}

            response = requests.request("POST", API_URL, headers=headers, data=payload, files=files)

            # Parse the response JSON
            response_json = response.json()

            # Extract only the 'result' part
            if 'result' in response_json:
                result_data = response_json['result']

                # Save only the result part to the output folder with the same name as the image file
                base_name = os.path.splitext(image_file)[0]
                output_file = os.path.join(OUTPUT_DIR, f"{base_name}.json")

                with open(output_file, 'w') as f:
                    json.dump(result_data, f)

                # Using tqdm.write to avoid interfering with the progress bar
                tqdm.write(f"✓ Result saved: {output_file}")
            else:
                tqdm.write(f"✗ Error: 'result' key not found in response for {image_file}")

        except Exception as e:
            tqdm.write(f"✗ Error processing {image_file}: {str(e)}")

if __name__ == "__main__":
    main()
