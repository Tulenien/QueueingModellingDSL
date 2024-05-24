import tkinter as tk
from tkinter import ttk


def default_window(window, name, size, color):
    window.title(name)
    window.geometry(size)
    window.configure(bg=color)

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x_offset = (window.winfo_screenwidth() - width) // 2
    y_offset = (window.winfo_screenheight() - height) // 2
    window.geometry('{}x{}+{}+{}'.format(width, height, x_offset, y_offset))


