from glob import glob
import os
import json 
from summary import Summary
import platform

image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
text_extensions = {'.txt', '.md', '.docx', '.doc', '.pdf', '.xls', '.xlsx'}
# tested
def establish_type(path):
    if os.path.isdir(path):
        return "dir", "dir"
    index = path.rfind('.')

    if path[index:] in image_extensions:
        return "image", path[index+1:]
    elif path[index:] in text_extensions:
        return "text", path[index+1:]
    else:
        return "NONE", "NONE"

class File:
    def __init__(self, path):
        self.path=path
        pass

class Directory(File):
    def __init__(self, path, summary):
        super().__init__(path)
        self.summary = summary
        self.content, self.dir=self.get_content()
        self.jsonfile = self.get_json()
        pass

    def is_file_valid(self, path):
        print(path)
        file_name_tag = path.rfind("/") if path.rfind("\\") == -1 else path.rfind("\\")
        print(file_name_tag)
        doc_name = path[file_name_tag+1:]
        print(doc_name)
        if os.path.isfile(path) and doc_name[0] != "~":
            return True
        else:
            return False

    def get_content(self):
        data = os.listdir(self.path)
        content = [os.path.join(self.path, file) for file in data if self.is_file_valid(os.path.join(self.path, file))]
        dir = [os.path.join(self.path, file) for file in data if os.path.isdir(os.path.join(self.path, file))]
        output_content = []
        output_dir = []
        
        for c in content:
            filetype, doctype = establish_type(c)
            if filetype == "NONE":
                continue
            output_content.append(Readables(c, filetype, doctype, self.summary))
        for d in dir:
            output_dir.append(Directory(d, self.summary))
        return output_content, output_dir
    
    def get_json(self):
        for c in self.content:
            self.jsonfile.append(c.to_json())
        for d in self.dir:
            d.get_json()
    



class Readables(File):
    def __init__(self, path, filetype, doctype, summary):
        super().__init__(path)
        self.filetype = filetype
        self.doctype = doctype
        self.summary = summary.summarize(path, filetype, doctype)

    def to_json(self):
        output = {
            "path":self.path,
            "filetype":self.filetype,
            "doctype":self.doctype,
            "summary":self.summary
        }
        return output

def jsonize(path):
    summary = Summary()
    test = Directory(path, summary)
    jsonlist = json.dumps(test.jsonfile, indent=2)
    print(jsonlist)
    with open('test.json', 'w') as fout:
        json.dump(test.jsonfile, fout, indent=2)

def vectorize(path):
    summary = Summary()
    test = Directory(path, summary)
    test.content
    vectorfile = []
