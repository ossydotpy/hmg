import json
import re


#reading and returning the metadata content
def get_metadata():
    with open('data/prio&proto_metadata.json','r') as data:
        content = json.load(data)
    return content

# max points per class
max_points = {'Berserker': 395, 'Racer': 410, 
 'Bruiser': 400, 'Sentinel': 400, 
 'Loose Cannon': 410, 'Sharpshooter': 400, 
 'Survivalist': 395, 'Demolition': 390, 
 'Hero': 400, 'Shield': 400, 'Ghost': 410, 
 'Scout': 400, 'Tank': 400, 'Stuntman': 395, 
 'Hulk': 395, 'Driver': 400, 'Ranger': 400, 
 'Juggernaut': 400, 'Ninja': 400, 'Mercenary': 420}

#saving the needed bits
def save_important_metadata(meta):    
    imp = [{
            "name":value['onchain_metadata']['name'],
            "id":value["asset"],
            "class":value['onchain_metadata']['Class'],
            "birth_state":value['onchain_metadata']['Birth State'],
            "image": "https://ipfs.blockfrost.dev/ipfs/" + value['onchain_metadata']['image'][7:],
            "defense":int(value['onchain_metadata']['Defense']),
            "strength":int(value['onchain_metadata']['Strength']),
            "dexterity":int(value['onchain_metadata']['Dexterity']),
            "hit_points":int(value['onchain_metadata']['Hit Points']),
            "perception":int(value['onchain_metadata']['Perception']),
            "constitution":int(value['onchain_metadata']['Constitution']),
            "vehicle_handling":int(value['onchain_metadata']['Vehicle Handling']),
            "total": sum(int(value['onchain_metadata'][k]) 
                                for k in ['Defense', 'Strength', 
                                    'Dexterity', 'Hit Points', 'Perception',
                                    'Constitution', 'Vehicle Handling']),

            "total_minus_hp":sum(int(value['onchain_metadata'][k]) 
                                 for k in ['Defense', 'Strength', 
                                    'Dexterity', 'Perception',
                                    'Constitution', 'Vehicle Handling']),

            "max": max_points.get(value['onchain_metadata']['Class'], None),
            "max_minus_hp":max_points.get(value['onchain_metadata']['Class'], 0)-int(value['onchain_metadata']['Hit Points']),
           
            } for k, value in meta.items() if not value['onchain_metadata']['name'].startswith('HM Prio Monster')]
    
    with open('data/proto_features.json', 'w') as features:
        json.dump(imp, features)


if __name__=="__main__":
    mm =get_metadata()
    save_important_metadata(mm)
