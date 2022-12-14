# Importing required libraries
import requests
from datetime import datetime
import hashlib
from pprint import pprint as pp
from dotenv import load_dotenv
import os
import pandas as pd
import string
import argparse

# Importing functions from mypackage folder
from mypackage.hash_function import hash_params
from mypackage.character import get_character_data
from mypackage.filtering_data import filtering_data

load_dotenv()

# Getting timestamp, public-key and private-key
timestamp = datetime.now()
# pub_key = os.getenv('PUBLIC_KEY')
# priv_key = os.getenv('PRIVATE_KEY')

# Creating dictionary with required keys
data = {'character_name': [], 'event_appearances': [], 'series_appearances': [],
        'stories_appearances': [], 'comics_appearances': [], 'character_id': []}

# Getting public and private key from user
parser= argparse.ArgumentParser(description="Enter the keys")
parser.add_argument('pub_key', type=str, help='Enter the public-key')
parser.add_argument('priv_key', type=str, help='Enter the private-key')
args=parser.parse_args()
pub_key= getattr(args, 'pub_key', 'public-key is not entered')
priv_key=getattr(args, 'priv_key', 'private-key is not entered')

# Getting hash value using timestamp, public-key and private-key as parameters
hash = hash_params(timestamp, pub_key, priv_key)

# List of characters from 'a' to 'z'
characters = list(string.ascii_lowercase)

# Passing the characters as parameter and getting
final_data = get_character_data(data, timestamp, pub_key, hash, characters) # TAKES LONG TIME TO GET RESULTS
# final_data = get_character_data(data, timestamp, pub_key, hash, ['s']) # Only taking character 's' to to get results fast

# Converting data into a dataframe
marvel_df = pd.DataFrame(final_data)

# Printing the final result
print(filtering_data(marvel_df))
