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

    def search_file(self, prompt):
        answer = search(path=self.dir.path, prompt=prompt)
        df = pd.DataFrame(answer)
        return df


# gradio has no clean ui for folder path submission vvv

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
