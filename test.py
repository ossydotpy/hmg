import json

def get_metadata():
    with open('nft_metadata.json','r') as data:
        content = json.load(data)
    return content

def save_important_metadata(meta):
    imp =[]
    for k,value in meta.items():
        deets = {
            "name":value['onchain_metadata']['name'],
            "defense":int(value['onchain_metadata']['Defense']),
            "strength":int(value['onchain_metadata']['Strength']),
            "dexterity":int(value['onchain_metadata']['Dexterity']),
            "hit_points":int(value['onchain_metadata']['Hit Points']),
            "perception":int(value['onchain_metadata']['Perception']),
            "constitution":int(value['onchain_metadata']['Constitution']),
            "vehicle_handling":int(value['onchain_metadata']['Vehicle Handling'])
        }
        imp.append(deets)
    with open('features.json','a') as features:
        json.dump(imp,features)


def retrieve_features():
    with open('features.json','r') as features:
        data = json.load(features)
    return data


def search_dicts():
    nfts = retrieve_features()
    keyword = input('dfdfd\n>>> ')
    results = []
    for d in nfts:
        for value in d.values():
            if isinstance(value, str) and keyword in value:
                results.append(d)
                break
    return results
save_important_metadata(get_metadata())
print(search_dicts())



# def display_stats():
#     nft = search_list_of_dicts()
#     template="""
#     nft deets
#     name:
#     """
#     pass



# def search_list_of_dicts():
#     nfts = retrieve_features()
#     keyword = input('dfdfd\n>>> ')
#     results = []
#     for item in nfts:
#         if keyword in item.values():
#             results.append(item)
#     return results

# print(search_list_of_dicts())