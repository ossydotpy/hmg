import requests
import json

# Replace <YOUR_API_KEY> with your actual Blockfrost API key
api_key = 'mainnet9xRVFCPHypbGnNyiFmtkgEOvZrZFmYn6'

# Replace <POLICY_ID> with the actual policy ID you want to query
policy_id = 'fec7dfa59902eb40f65a62812662769962d5662f2a6bc2804b829881'

# Construct the URL to get all the asset IDs under the policy
url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/policy/{policy_id}/addresses'

# Set the headers to include your API key
headers = {
    'project_id': api_key
}

# Make the GET request to the API to retrieve the asset IDs
response = requests.get(url, headers=headers)

# Convert the response to a JSON object
data = response.json()

# Loop through each asset ID and retrieve the asset metadata
assets_metadata = {}
for asset_data in data:
    asset_id = asset_data['asset']
    url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/{asset_id}'
    response = requests.get(url, headers=headers)
    asset_metadata = response.json()
    onchain_metadata_url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/{asset_id}/metadata'
    onchain_metadata_response = requests.get(onchain_metadata_url, headers=headers)
    onchain_metadata = onchain_metadata_response.json()
    asset_metadata['onchain_metadata'] = onchain_metadata
    assets_metadata[asset_id] = asset_metadata

# Write the metadata to a JSON file
with open('nft_metadata.json', 'w') as outfile:
    json.dump(assets_metadata, outfile)
