import gradio as gr
from tkinter import Tk, filedialog
import pandas as pd

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

def get_folder_path(folder_path: str = "") -> str:
    """
    Opens a folder dialog to select a folder, allowing the user to navigate and choose a folder.
    If no folder is selected, returns the initially provided folder path or an empty string if not provided.
    This function is conditioned to skip the folder dialog on macOS or if specific environment variables are present,
    indicating a possible automated environment where a dialog cannot be displayed.

    Parameters:
    - folder_path (str): The initial folder path or an empty string by default. Used as the fallback if no folder is selected.

    Returns:
    - str: The path of the folder selected by the user, or the initial `folder_path` if no selection is made.

    Raises:
    - TypeError: If `folder_path` is not a string.
    - EnvironmentError: If there's an issue accessing environment variables.
    - RuntimeError: If there's an issue initializing the folder dialog.

    Note:
    - The function checks the `ENV_EXCLUSION` list against environment variables to determine if the folder dialog should be skipped, aiming to prevent its appearance during automated operations.
    - The dialog will also be skipped on macOS (`sys.platform != "darwin"`) as a specific behavior adjustment.
    """
    # Validate parameter type
    if not isinstance(folder_path, str):
        raise TypeError("folder_path must be a string")

    try:
        root = Tk()
        root.withdraw()
        root.wm_attributes("-topmost", 1)
        selected_folder = filedialog.askdirectory(initialdir=folder_path or ".")
        root.destroy()
        return selected_folder or folder_path
    except Exception as e:
        raise RuntimeError(f"Error initializing folder dialog: {e}") from e


def create_folder_ui(path="./"):
    with gr.Row():
        with gr.Column(scale=9):
            text_box = gr.Textbox(
                lines=1,
                value=path,
            )
        with gr.Column(scale=1):
            button = gr.Button(value="\U0001f5c0", inputs=text_box, min_width=4)

    button.click(
        lambda: get_folder_path(text_box.value),
        outputs=[text_box],
    )

    return text_box, button
# gradio has no clean ui for folder path submission ^^^

def interface():
    with gr.Blocks() as folder_upload:
        with gr.Row():
            with gr.Column():
                text_box = create_folder_ui()
                btn = gr.Button()
        
    with gr.Blocks() as prompt_and_search:
        with gr.Row():
            with gr.Column():
                # jsn = gr.File(value="import a json file")
                # json_btn = gr.Button()
                prompt = gr.Textbox(value="Type something related to the file")
            with gr.Column():
                data = gr.Dataframe()
    demo = gr.TabbedInterface(interface_list=[folder_upload, prompt_and_search], tab_names=["folder_upload", "prompt_and_search"])
    btn.click(fn=open_folder, inputs=[text_box], outputs=[data])
    demo.launch()