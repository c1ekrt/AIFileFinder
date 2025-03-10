from glob import glob
import os
import json 
from summary import Summary
import platform
from langchain_core.documents import Document
import hashlib
from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_community.document_loaders.word_document import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader, PyPDFLoader, TextLoader

from util import to_checksum

FILE_LOADER_MAPPING = {
    "doc": (UnstructuredWordDocumentLoader, {}),
    "docx": (UnstructuredWordDocumentLoader, {}),
    "md": (UnstructuredMarkdownLoader, {}),
    "pdf": (PyPDFLoader, {}),
    "txt": (TextLoader, {"encoding": "utf8"}),
}

# image not implement yet
image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
text_extensions = {'.txt', '.md', '.docx', '.doc', '.pdf', '.xls', '.xlsx'}

# identify file type
def establish_type(path):
    if os.path.isdir(path):
        return "dir", "dir"
    index = path.rfind('.')

    if path[index:] in image_extensions:
        return "image", "NONE"
    elif path[index:] in text_extensions:
        return "text", path[index+1:]
    else:
        return "NONE", "NONE"

# file structure
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
        file_name_tag = path.rfind("/") if path.rfind("\\") == -1 else path.rfind("\\")
        doc_name = path[file_name_tag+1:]
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
            if filetype == "NONE" or filetype == "image":
                continue
            output_content.append(Readables(c, filetype, doctype, self.summary))
        for d in dir:
            output_dir.append(Directory(d, self.summary))
        return output_content, output_dir
    
    def get_json(self):
        jsonfile = []
        for c in self.content:
            jsonfile.append(c.to_json())
        for d in self.dir:
            jsonfile += d.jsonfile
        return jsonfile
    
    def jsonize(self, filename):
        with open(f'{filename}.json', 'w', encoding='utf-8') as fout:
            json.dump(self.jsonfile, fout, indent=2)

class Readables(File):
    def __init__(self, path, filetype, doctype, summary):
        super().__init__(path)
        self.loader_class, self.loader_args = FILE_LOADER_MAPPING[doctype]
        self.filetype = filetype
        self.doctype = doctype
        self.summary = summary.summarize(path=path, filetype=filetype, doctype=doctype)
        loader = self.loader_class(path, **self.loader_args)
        self.checksum = to_checksum(loader)

    def to_json(self):
        output = {
            "path":self.path,
            "filetype":self.filetype,
            "doctype":self.doctype,
            "summary":self.summary,
            "checksum":self.checksum
        }
        return output

def vectorize(path):
    summary = Summary()
    test = Directory(path, summary)
    output = []
    for jf in test.jsonfile:
        output.append(Document(page_content=jf[summary], metadata={"source":jf[path]}))


