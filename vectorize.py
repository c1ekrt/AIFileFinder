from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate

from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
import chromadb
from uuid import uuid4

import filesys
from filesys import Directory, File, Readables
from summary import Summary

'''
Disclaimer: There is no way to detect file transferring by auto scanning
'''
# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    source: List[str]
    answer: str

class Vectordb():
    def __init__(self):
        model_name = "BAAI/bge-m3"
        model_kwargs = {"device": "cuda"}
        encode_kwargs = {"normalize_embeddings": True}
        self.embeddings = HuggingFaceBgeEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)
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
        # {uuid: id}
        self.uuid2id = dict()
        # {path:(uuid, checksum)}
        self.path2uuid = dict()
        self.prompt = template = PromptTemplate.from_template(
            """
            你是一個找尋檔案位置的小幫手，使用者會詢問使用者需要找的檔案的特徵，而小幫手只需要回答最相似的文件的位置即可，文件內容需要從context中獲得。
            Question: {question} 
            Context: {context} 
            Answer:
            """
            )
        self.llm = ChatOllama(
            model="llama3.2:1b",
            temperature=0.1,
        )
        self.content = []
        pass

    def import_document(self, dir:Directory):
        self.content = dir.content
        for file in dir.jsonfile:
            if  file["path"] not in self.path2uuid:
                self.vectorize_file(file)
            else:   # handle duplication, error tolerance
                if file["checksum"] != self.path2uuid[file["path"]][1] : 
                    modified_uuid = self.path2uuid[file["path"]][0]
                    modified_id = self.uuid2id[modified_uuid]
                    self.path2uuid.pop(file["path"])
                    self.modify_file(file, modified_id, modified_uuid) # untested

    def vectorize_file(self, file):
        id = self.available_id[0]
        d = Document(
            page_content=file["summary"],
            metadata={"source":file["path"]},
            id = id
        )
        self.available_id = self.available_id[1:]
        uuid = str(uuid4())
        self.path2uuid[file["path"]] = (uuid, file["checksum"])
        self.uuid2id[uuid] = id
        self.vector_store.add_documents(documents=[d], ids=uuid)
        pass

    def modify_file(self, file, id, uuid):    # untested
        update_doc = Document(
            page_content=file["summary"],
            metadata={"source":file["path"]},
            id = id
        )
        self.vector_store.update_document(documents=update_doc, ids=uuid)
        pass

    def retrieve(self, state):
        # Define application steps

        retrieved_docs = self.vector_store.similarity_search(state["question"])
        return {"context": retrieved_docs, "source":[path.metadata for path in retrieved_docs] }
        pass

    
    def generate(self, state: State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = self.prompt.invoke({"question": state["question"], "context": self.content})
        response = self.llm.invoke(messages)
        return {"answer": response.content}



def search(path, prompt):
    DB = Vectordb()
    summary = Summary()
    dir = Directory(path, summary)
    DB.import_document(dir)

    graph_builder = StateGraph(State).add_sequence([DB.retrieve, DB.generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()

    result = graph.invoke({"question": f"請幫我在context提供資料的範圍內尋找有關{prompt}的資料, 如果相關請將文件結尾 source 的路徑作為答案"})

    print(f'Context: {result["source"]}\n\n')
    print(f'Answer: {result["answer"][0]}')
    return result["source"]
    pass