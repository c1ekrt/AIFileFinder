
import hashlib
import json 

def to_checksum(loader):
    output = str(hashlib.md5(loader.load()[0].page_content.strip().encode('utf-8')).hexdigest())
    return output
