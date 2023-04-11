import requests
import json

api_key = 'mainnet9xRVFCPHypbGnNyiFmtkgEOvZrZFmYn6'
policy_id = 'fec7dfa59902eb40f65a62812662769962d5662f2a6bc2804b829881'
url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/policy/{policy_id}'

headers = {
    'project_id': api_key
}

# Make the GET request to the API to retrieve the asset IDs
response = requests.get(url, headers=headers)

# Convert the response to a JSON object
data = response.json()

# Loop through each asset ID and retrieve the asset metadata
assets_metadata = {}
for asset in data:
    asset_id = asset['asset']
    url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/{asset_id}'
    response = requests.get(url, headers=headers)
    asset_metadata = response.json()
    assets_metadata[asset_id] = asset_metadata

# Write the metadata to a JSON file
with open('nft_metadata.json', 'w') as outfile:
    json.dump(assets_metadata, outfile, indent=4)
