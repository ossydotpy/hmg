# future update
# allow for dynamic selection of features

import json
import os
import aiohttp
import requests

from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
api_key = os.getenv('BLOCKFROST_API_KEY')
HM_PRIO_GANG_POLICY = os.getenv('HM_PRIO_GANG_POLICY')



async def send_api_request(apiurl, headers=None, params = None):
    async with aiohttp.ClientSession() as session:
      async with session.get(apiurl, headers=headers, params=params) as response:
        data = await response.json()
        return data, response.status
      

class Features:
    """
    A class that provides tools to save essential features from the HerMonsters Collection.
    
    Args:
    load_path (str): The path to the uncleaned NFT metadata file.
    starts_with (str, optional): The common prefix of all NFT names in the collection. Defaults to "HM".

    Attributes:
        max_points (dict): A dictionary containing the maximum points for each class.


    """
    def __init__(self, load_path, starts_with="HM"):
        self._load_path = load_path
        self._starts_with = starts_with
        self._max_points = {
            'Berserker': 395, 'Racer': 410, 'Bruiser': 400, 'Sentinel': 400,
            'Loose Cannon': 410, 'Sharpshooter': 400, 'Survivalist': 395,
            'Demolition': 390, 'Hero': 400, 'Shield': 400, 'Ghost': 410,
            'Scout': 400, 'Tank': 400, 'Stuntman': 395, 'Hulk': 395,
            'Driver': 400, 'Ranger': 400, 'Juggernaut': 400, 'Ninja': 400,
            'Mercenary': 420
        }

    @property
    def max_points(self):
        """
          Get the dictionary containing the maximum points for each class.

          Returns:
              dict: A dictionary where the keys are class names and the values are the maximum points.

        """
        return self._max_points

    @property
    def metadata(self):
        with open(self._load_path, 'r') as f:
            data = json.load(f)
        return data

    def save_metadata(self, save_path):
        """
        Save the desired metadata (default values as of now).

        Args:
            save_path (str): The name of the output file.

        """
        metadata = self.metadata
        useful_meta = [
            {
                "name": value['onchain_metadata']['name'],
                "id": value["asset"],
                "class": value['onchain_metadata']['Class'],
                "birth_state": value['onchain_metadata']['Birth State'],
                "image": "https://ipfs.blockfrost.dev/ipfs/" + value['onchain_metadata']['image'][7:],
                "defense": int(value['onchain_metadata']['Defense']),
                "strength": int(value['onchain_metadata']['Strength']),
                "dexterity": int(value['onchain_metadata']['Dexterity']),
                "hit_points": int(value['onchain_metadata']['Hit Points']),
                "perception": int(value['onchain_metadata']['Perception']),
                "constitution": int(value['onchain_metadata']['Constitution']),
                "vehicle_handling": int(value['onchain_metadata']['Vehicle Handling']),
                "total": sum(int(value['onchain_metadata'][k]) for k in
                             ['Defense', 'Strength', 'Dexterity', 'Hit Points', 'Perception',
                              'Constitution', 'Vehicle Handling']),

                "total_minus_hp": sum(int(value['onchain_metadata'][k]) for k in
                                      ['Defense', 'Strength', 'Dexterity', 'Perception',
                                       'Constitution', 'Vehicle Handling']),

                "max": self._max_points.get(value['onchain_metadata']['Class'], None),
                "max_minus_hp": self._max_points.get(value['onchain_metadata']['Class'], 0) -
                                 int(value['onchain_metadata']['Hit Points']),

            } for k, value in metadata.items() if value['onchain_metadata']['name'].startswith(self._starts_with)]

        with open(f'data/{save_path}_features.json', 'w') as f:
            json.dump(useful_meta, f)


class Collection:
    """
    A class to retrieve and save metadata for assets under a collection based on a specific policy ID.

    Args:
        policy_id (str): The policy ID for the collection.

    Attributes:
        _policy_id (str): The policy ID for the collection.
        _url (str): The URL to fetch the collection's data.
        _headers (dict): The headers for the HTTP requests.
        _all_assets (list): A list to store all the retrieved assets' data.

    """

    def __init__(self, policy_id):
        self._policy_id = policy_id
        self._url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/policy/{policy_id}'
        self._headers = {'project_id': api_key}
        self._all_assets = []

    @property
    def policy_id(self):
        """
        Get the policy ID for the assets.

        Returns:
            str: The policy ID.

        """
        return self._policy_id

    @property
    def url(self):
        """
        Get the URL to fetch the collection's data.

        Returns:
            str: The URL.

        """
        return self._url

    @property
    def headers(self):
        """
        Get the headers for the HTTP requests.

        Returns:
            dict: The headers.

        """
        return self._headers

    @property
    def all_assets(self):
        """
        Get the list of all retrieved assets' data.

        Returns:
            list: The list of assets' data.

        """
        return self._all_assets

    def get_asset_data(self):
        """
        Retrieve the assets' data based on the policy ID.

        Returns:
            dict: A dictionary mapping asset IDs to their metadata.

        """
        page_number = 1
        
        while True:
            params = {'page': page_number}
            response = requests.get(self.url, headers=self.headers, params=params)
            data = response.json()
            if len(data) == 0:
                break

            self.all_assets.extend(data)
            page_number += 1

        assets_metadata = {}
        for asset in tqdm(self.all_assets):
            asset_id = asset['asset']
            asset_url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/{asset_id}'
            response = requests.get(asset_url, headers=self.headers)
            asset_metadata = response.json()
            assets_metadata[asset_id] = asset_metadata

        return assets_metadata
    
    def save_metadata(self, save_path):
        """
        Save the assets' metadata to a file.

        Args:
            save_path (str): The path to save the metadata file.

        Returns:
            str: A message indicating the status of the operation.

        """
        assets_metadata = self.get_asset_data()
        with open(save_path, 'w') as outfile:
            json.dump(assets_metadata, outfile, indent=4)
        print(f"Data saved to {save_path}!")