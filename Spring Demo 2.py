from NewDadsDoor import classes

import tkinter as tk, tkinter.ttk as ttk
from alcustoms.tkinter import smarttkinter, advancedtkinter

SmartFrame = smarttkinter.ttk.SmartFrame

class MainPane(smarttkinter.GMMixin, SmartFrame):
    def __init__(self,parent,**kw):
        super().__init__(parent,**kw)

        ttk.Label(self, text = "Quick Spring Demo", style = "Title.TLabel")

        f = SmartFrame(self)
        row = [
            ttk.Label(f,text="Wire", sytle = "Bold.TLabel"),
            ttk.Label(f,text="OD", sytle = "Bold.TLabel"),
            ttk.Label(f,text="Unc.Length", sytle = "Bold.TLabel"),
            ttk.Label(f,text="Coils", sytle = "Bold.TLabel"),
            ttk.Label(f,text="Lift", sytle = "Bold.TLabel"),
        ]
        for i,header in enumerate(row, start = 1):
            header.grid(row = 0, col = i)
        for spring in range(2):
            spring += 1 
            row = [
                ttk.Label(f,text=f"Spring {spring}", sytle = "Bold.TLabel")
                ttk.
                ]
            for i,cell in enumerate(row):
                cell.grid(row = spring, column = i)
             
