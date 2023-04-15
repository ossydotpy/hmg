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
            "class":value['onchain_metadata']['Class'],
            "birth_state":value['onchain_metadata']['Birth State'],
            "defense":int(value['onchain_metadata']['Defense']),
            "strength":int(value['onchain_metadata']['Strength']),
            "dexterity":int(value['onchain_metadata']['Dexterity']),
            "hit_points":int(value['onchain_metadata']['Hit Points']),
            "perception":int(value['onchain_metadata']['Perception']),
            "constitution":int(value['onchain_metadata']['Constitution']),
            "vehicle_handling":int(value['onchain_metadata']['Vehicle Handling']),
            "total": sum(int(value['onchain_metadata'][k]) for k in ['Defense', 'Strength', 
                                                                'Dexterity', 'Hit Points', 'Perception',
                                                                'Constitution', 'Vehicle Handling'])
           
            } for k, value in meta.items() if not value['onchain_metadata']['name'].startswith('HM Prio Monster')]
    with open('proto_features.json', 'w') as features:
        json.dump(imp, features)


if __name__=="__main__":
    mm =get_metadata()
    save_important_metadata(mm)
