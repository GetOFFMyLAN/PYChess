from tkinter import *
from tkinter import ttk
from enum import Enum

# win properties


class Properties(Enum):
    WIN_NAME = "Chess"
    WIN_BG = "#FFF"


def win_proc():
    root = Tk()
    return root


def win_setup(proc):
    win_frame = ttk.Frame
