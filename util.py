
import hashlib
import json 
import pandas as pd 
import os

# image not implement yet
image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
text_extensions = {'.txt', '.md', '.docx', '.doc', '.pdf', '.xls', '.xlsx'}

def to_checksum(loader):
    output = str(hashlib.md5(loader.load()[0].page_content.strip().encode('utf-8')).hexdigest())
    return output

def json2dataframe(jsn):
    data = json.loads(jsn)
    df = pd.json_normalize(data)
    return df

def is_file_valid(path):
        file_name_tag = path.rfind("/") if path.rfind("\\") == -1 else path.rfind("\\")
        doc_name = path[file_name_tag+1:]
        if os.path.isfile(path) and doc_name[0] != "~":
            return True
        else:
            return False
        
class GetFileCount:
    def __init__(self, path):
        self.count = 0
        self.path = path
        self.get_file_count(self.path)

    def get_file_count(self, path):
        data = os.listdir(path)
        content = [os.path.join(path, file) for file in data if is_file_valid(os.path.join(path, file))]
        dir = [os.path.join(path, file) for file in data if os.path.isdir(os.path.join(path, file))]
        self.count += len(content)
        for d in dir:
            self.get_file_count(d)
            