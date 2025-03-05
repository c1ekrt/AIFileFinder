
import hashlib
import json 
import pandas as pd 

def to_checksum(loader):
    output = str(hashlib.md5(loader.load()[0].page_content.strip().encode('utf-8')).hexdigest())
    return output

def json2dataframe(jsn):
    data = json.loads(jsn)
    df = pd.json_normalize(data)
    return df