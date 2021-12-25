import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import font
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning
from PyPDF2 import PdfFileReader 
from pdf2image import convert_from_path
# import pandas as pd
# import numpy as np
import sys
import os
import re


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), "images", relative_path)


class InputFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(
            [0],
            weight=1,
        )

        # browse frame
        self.browse_frame = ttk.LabelFrame(self, text="Reference File")
        self.browse_frame.grid(column=0, row=0, sticky=tk.EW, ipadx=5, ipady=3)
        self.browse_frame.columnconfigure(
            [0],
            weight=1,
        )

        self.filepath = tk.StringVar()
        filepath_entry = ttk.Entry(self.browse_frame, textvariable=self.filepath)
        filepath_entry.grid(column=0, row=0, sticky=tk.EW)
        filepath_entry.focus()

        self.img_mglass = tk.PhotoImage(file=resource_path("mglass.png"))
        load_button = ttk.Button(
            self.browse_frame, image=self.img_mglass, command=self.browse_file
        )
        load_button.grid(column=1, row=0)

        # pdf view frame
        self.pdf_frame=ttk.Frame(self)
        self.pdf_frame.grid(column=0, row=1, sticky=tk.EW, ipadx=5, ipady=3)
        self.pdf_frame.columnconfigure(
            [0],
            weight=1,
        )

        self.pagenum_list=tk.StringVar(value=[])
        self.pages=tk.Listbox(self.pdf_frame,listvariable=self.pagenum_list)
        self.pages.grid(column=0,row=0,sticky=tk.EW)

        button_frame=ttk.Frame(self.pdf_frame)
        button_frame.grid(column=1,row=0)

        up_button = ttk.Button(button_frame, text="⬆", command=self.up_item)
        up_button.grid(row=0, column=0)

        down_button = ttk.Button(button_frame, text="⬇", command=self.down_item)
        down_button.grid(row=1, column=0)

    def browse_file(self):
        """
        Handle button click event
        """
        self.filepath.set(filedialog.askopenfilename(
            filetypes=[("pdf file", "*.pdf"), ("all", "*")],
            title="load",
        ))
        # self.df=pd.read_csv(f'{self.filepath}',encoding='shift_jis',header=None)
        # self.filepath_entry.delete(0, tk.END)
        # self.filepath_entry.insert(tk.END, self.filepath)
        self.pdf=pdf=PdfFileReader(self.filepath.get())
        num_pages=pdf.getNumPages()
        self.pagenum_list.set([i for i in range(num_pages)])
    
    def up_item(self):
        selected=int(self.pages.curselection()[0])
        if selected!=0:
            _list=self.pagenum_list.get()
            print(_list)
            _list[selected-1],_list[selected]=_list[selected],_list[selected-1]
            self.pagenum_list.set(_list)

    def down_item(self):
        pass


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("")
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial",weight="bold")
        
        self.attributes("-alpha", 0.0)
        self.resizable(width=True, height=False)
        self.minsize(width=400, height=20)
        # icon = tk.PhotoImage(file=resource_path(""))
        # self.tk.call("wm", "iconphoto", self._w, icon)

        # layout on the root window
        self.columnconfigure(0, weight=1)
        self.__create_widgets()

    def __create_widgets(self):
        # create the input frame
        input_frame = InputFrame(self)
        input_frame.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)


def center(win):
    w = win.winfo_screenwidth()  # モニター横幅取得
    h = win.winfo_screenheight()  # モニター縦幅取得
    w = int(w / 2 - float(re.split("[+x]", win.geometry())[0]) / 2)  # メイン画面横幅分調整
    h = int(h / 2 - float(re.split("[+x]", win.geometry())[1]) / 2)  # メイン画面縦幅分調整
    win.geometry("+" + str(w) + "+" + str(h))  # 位置設定
    app.attributes("-alpha", 1.0)


if __name__ == "__main__":
    app = App()
    center(app)
    app.mainloop()
