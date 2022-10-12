
import requests
from datetime import datetime
import hashlib
from pprint import pprint as pp
from dotenv import load_dotenv
import os
import pandas as pd
import string

from mypackage.hash_function import hash_params
from mypackage.character import get_character_data
from mypackage.filtering_data import filtering_data

load_dotenv()

timestamp = datetime.now()
pub_key = os.getenv('PUBLIC_KEY')
priv_key = os.getenv('PRIVATE_KEY')

data = {'character_name': [], 'event_appearances': [], 'series_appearances': [],
        'stories_appearances': [], 'comics_appearances': [], 'character_id': []}

hash = hash_params(timestamp, pub_key, priv_key)

characters = list(string.ascii_lowercase)

# get_character_data(data, timestamp, pub_key, hash, characters, timestamp) # TAKES LONG TIME TO GET RESULTS
get_character_data(data, timestamp, pub_key, hash, ['s']) # Only taking character 's' to to get results fast

marvel_df = pd.DataFrame(data)

print(filtering_data(marvel_df))
