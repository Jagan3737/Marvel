
import requests
from datetime import datetime
import hashlib
from pprint import pprint as pp
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

timestamp = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
pub_key = os.getenv('PUBLIC_KEY')
priv_key = os.getenv('PRIVATE_KEY')


def hash_params():
    hash_md5 = hashlib.md5()
    hash_md5.update(f'{timestamp}{priv_key}{pub_key}'.encode('utf-8'))
    hashed_params = hash_md5.hexdigest()

    return hashed_params


data = {'character_name': [], 'event_appearances': [], 'series_appearances': [],
        'stories_appearances': [], 'comics_appearances': [], 'character_id': []}


def get_character_data(nameStartsWith):
    for offset in range(3):
        params = {'ts': timestamp, 'apikey': pub_key,
                  'hash': hash_params(), 'limit': 100, 'offset': 100*offset}
        res = requests.get('https://gateway.marvel.com:443/v1/public/characters?nameStartsWith=' +
                           nameStartsWith, params=params)
        results = res.json()

        for i in results['data']['results']:
            data['character_name'].append(i['name'])
            data['event_appearances'].append(i['events']['available'])
            data['series_appearances'].append(i['series']['available'])
            data['stories_appearances'].append(i['stories']['available'])
            data['comics_appearances'].append(i['comics']['available'])
            data['character_id'].append(i['id'])

char_start_with = input('Enter a character/name that starts with : ')
get_character_data(char_start_with)
df = pd.DataFrame(data)
print(df)
