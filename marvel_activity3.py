
import requests
from datetime import datetime
import hashlib
from pprint import pprint as pp
from dotenv import load_dotenv
import os
import pandas as pd
import string

load_dotenv()

timestamp = datetime.now()
pub_key = os.getenv('PUBLIC_KEY')
priv_key = os.getenv('PRIVATE_KEY')


def hash_params():
    hash_md5 = hashlib.md5()
    hash_md5.update(f'{timestamp}{priv_key}{pub_key}'.encode('utf-8'))
    hashed_params = hash_md5.hexdigest()

    return hashed_params


data = {'character_name': [], 'event_appearances': [], 'series_appearances': [],
        'stories_appearances': [], 'comics_appearances': [], 'character_id': []}


def get_character_data(api_key, hash=None, characters=[]):
    try:
        for letter in characters:
            for offset in range(3):
                params = {'ts': timestamp, 'apikey': api_key,
                          'hash': hash, 'limit': 100, 'offset': offset*100}
                res = requests.get('https://gateway.marvel.com:443/v1/public/characters?nameStartsWith=' +
                                   letter, params=params)
                results = res.json()

                for i in results['data']['results']:
                    data['character_name'].append(i['name'])
                    data['event_appearances'].append(i['events']['available'])
                    data['series_appearances'].append(i['series']['available'])
                    data['stories_appearances'].append(i['stories']['available'])
                    data['comics_appearances'].append(i['comics']['available'])
                    data['character_id'].append(i['id'])
    except:
        print('API or Hash keys are missing')


hash = hash_params()

characters = list(string.ascii_lowercase)

get_character_data(pub_key, hash, characters)
# get_character_data(pub_key)

marvel_df = pd.DataFrame(data)
print(marvel_df)
