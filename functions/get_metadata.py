import requests
import json
import os
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
api_key = os.getenv('BLOCKFROST_API_KEY')
policy_id = os.getenv('HM_PRIO_GANG_POLICY')
url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/policy/{policy_id}'
headers = {'project_id': api_key}

# Set the initial page number to 1
page_number = 1

# Keep track of all the retrieved assets
all_assets = []

# Loop through each page of assets until all the assets have been retrieved
while True:
    # Make the GET request to the API to retrieve the assets on the current page
    params = {'page': page_number}
    response = requests.get(url, headers=headers, params=params)

    # Convert the response to a JSON object
    data = response.json()

    # If the current page is empty, all assets have been retrieved
    if len(data) == 0:
        break

    # Add the assets on the current page to the list of all assets
    all_assets.extend(data)

    # Increment the page number for the next request
    page_number += 1

# Loop through each asset and retrieve its metadata, with a progress bar
assets_metadata = {}
for asset in tqdm(all_assets):
    asset_id = asset['asset']
    asset_url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/{asset_id}'
    response = requests.get(asset_url, headers=headers)
    asset_metadata = response.json()
    assets_metadata[asset_id] = asset_metadata

# Write the metadata to a JSON file
with open('nft_metadata.json', 'w') as outfile:
    json.dump(assets_metadata, outfile, indent=4)