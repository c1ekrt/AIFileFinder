from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

import chromadb
from uuid import uuid4

import filesys
from filesys import Directory, File, Readables
from summary import Summary

'''
Disclaimer: There is no way to detect file transferring by auto scanning
'''


class Vectordb():
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.vector_store = Chroma(
            collection_name="example_collection",
            embedding_function=self.embeddings,
            persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
        )

        self.persistent_client = chromadb.PersistentClient()
        self.collection = self.persistent_client.get_or_create_collection("AIFileFinder")

        self.vector_store_from_client = Chroma(
            client=self.persistent_client,
            collection_name="collection_name",
            embedding_function=self.embeddings,
        )
        self.max_document_count = 100
        self.available_id = [i for i in range(self.max_document_count)]
        
        # {path:id}
        self.path2id = dict()
        pass

    def import_document(self, dir:Directory):
        for file in dir.jsonfile:
            if  file["path"] not in self.path2id:
                self.path2id[file["path"]] = self.available_id[0]
                self.available_id = self.available_id[1:]
                self.vectorize_file(file)
            else:   # handle duplication, error tolerance
                self.modify_file()

    def vectorize_file(self, file):
        d = Document(
            page_content=file["summary"],
            metadata={"source":file["path"]},
            id = self.path2id[file["path"]]
        )
        uuids = str(uuid4())
        self.vector_store.add_documents(documents=[d], ids=uuids)
        pass

    def modify_file(self, file):
        pass

    def modify_dir(self, dir):
        pass


DB = Vectordb()
summary = Summary()
path = r"testmanual"
dir = Directory(path, summary)
DB.import_document(dir)
print(DB.path2id)