
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
                    data['stories_appearances'].append(
                        i['stories']['available'])
                    data['comics_appearances'].append(i['comics']['available'])
                    data['character_id'].append(i['id'])
    except:
        print('API or Hash keys are missing')


hash = hash_params()

characters = list(string.ascii_lowercase)

# get_character_data(pub_key, hash, characters) # TAKES LONG TIME TO GET RESULTS
get_character_data(pub_key, hash, ['s']) # Only taking character 's' to to get results fast

marvel_df = pd.DataFrame(data)


def filter_character_data_via_name(df, column, value):
    filtered_data_df = df[df[column].str.contains(value, case=False, na=False)]
    return filtered_data_df


def filter_character_data(df, column, condition, value):
    if condition == 1:
        filtered_data_df = df[df[column] > value]
    elif condition == 2:
        filtered_data_df = df[df[column] < value]
    elif condition == 3:
        filtered_data_df = df[df[column] == value]
    else:
        print('Wrong choice')

    return filtered_data_df


print('Columns in a dataframe:')
print('1. Character Name')
print('2. Event Appearances')
print('3. Series Appearances')
print('4. Stories Appearances')
print('5. Comics Appearances')
print('6. Character ID')
column = int(input('Enter the column(1-6) to filter on: '))

column_dict = {1: 'character_name', 2: 'event_appearances', 3: 'series_appearances',
               4: 'stories_appearances', 5: 'comics_appearances', 6: 'character_id'}

if column == 1:
    value = input('Enter the character to search for: ')
    marvel_filtered_df = filter_character_data_via_name(
        marvel_df, column_dict[column], value)
elif column >= 2 and column <= 5:
    print('1. Greater than')
    print('2. Lesser than')
    print('3. Equal to')
    condition = int(input('Enter the condition(1-3): '))
    if condition>3 or condition<1:
        marvel_filtered_df = 'Wrong Choice'
    else:
        value = int(input('Enter value: ')) 
        marvel_filtered_df = filter_character_data(
            marvel_df, column_dict[column], condition, value)
elif column == 6:
    value = int(input('Enter character id: '))
    marvel_filtered_df = filter_character_data(
        marvel_df, column_dict[column], 3, value)
else:
    marvel_filtered_df = 'Wrong Choice'
# marvel_filtered_df = filter_character_data(marvel_df,'series_appearances',10)
print(marvel_filtered_df)
