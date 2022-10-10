#Source code - https://gist.github.com/farleykr/cc77fae2df679de05148e6acbcc0893d

import requests  
from datetime import datetime
import hashlib
from pprint import pprint as pp
from dotenv import load_dotenv
import os

load_dotenv()

timestamp = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
pub_key = os.getenv('PUBLIC_KEY')
priv_key = os.getenv('PRIVATE_KEY')

def hash_params():
    hash_md5 = hashlib.md5()
    hash_md5.update(f'{timestamp}{priv_key}{pub_key}'.encode('utf-8'))
    hashed_params = hash_md5.hexdigest()
    
    return hashed_params

params = {'ts': timestamp, 'apikey': pub_key, 'hash': hash_params()};
res = requests.get('https://gateway.marvel.com:443/v1/public/characters?nameStartsWith=s&limit=100',params=params)

results = res.json()
pp(results)