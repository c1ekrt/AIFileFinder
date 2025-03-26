import gradio as gr
from tkinter import Tk, filedialog
import pandas as pd
import os

from summary import Summary
from vectorize import Vectordb, search
from filesys import Directory, Readables
from util import json2dataframe

class MainApp():

    def __init__(self, DB:Vectordb, dir:Directory):
        self.DB = DB
        self.dir = dir

    def import_json(self, jsn):
        pass

    def search_file(self, prompt, count):
        answer = search(DB=self.DB, prompt=prompt, count=count)
        df = pd.DataFrame(answer)
        return df

def open_folder(path):
    DB, dir = call_main(path)
    return MainApp(DB, dir)
    pass

def call_main(path):
    DB = Vectordb()
    summary = Summary()
    dir = Directory(path, summary)
    DB.import_document(dir)
    return DB, dir
