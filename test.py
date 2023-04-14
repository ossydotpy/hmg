import json
import re


#reading and returning the metadata content
def get_metadata():
    with open('nft_metadata.json','r') as data:
        content = json.load(data)
    return content

#saving the needed bits
def save_important_metadata(meta):
    imp = [{
            "name":value['onchain_metadata']['name'],
            "image":value['onchain_metadata']['image'],
            "defense":int(value['onchain_metadata']['Defense']),
            "strength":int(value['onchain_metadata']['Strength']),
            "dexterity":int(value['onchain_metadata']['Dexterity']),
            "hit_points":int(value['onchain_metadata']['Hit Points']),
            "perception":int(value['onchain_metadata']['Perception']),
            "constitution":int(value['onchain_metadata']['Constitution']),
            "vehicle_handling":int(value['onchain_metadata']['Vehicle Handling'])
        } for k, value in meta.items()]

    with open('features.json', 'w') as features:
        json.dump(imp, features)


def retrieve_features():
    with open('features.json','r') as features:
        data = json.load(features)
    return data


def search_dicts():
    nfts = retrieve_features()
    while True:
        keyword = input('Enter search query (e.g. "#1" or "sword"):\n>>> ')
        if keyword.startswith('#'):
            exact_match = re.match(r'^#(\d+)$', keyword)
            if exact_match:
                number = int(exact_match.group(1))
                results = [d for d in nfts if int(d['name'].split()[-1][1:]) == number]
            else:
                results = [d for d in nfts if keyword.lower() in d['name'].lower()]
            if results:
                return results
            else:
                print('No results found for query:', keyword)
        else:
            print('Search query must start with "#"')



mm =get_metadata()
print(search_dicts())
