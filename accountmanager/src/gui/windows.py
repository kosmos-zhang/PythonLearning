#coding: utf-8

import sys, os
import tkinter as tk
import tkMessageBox
from utils.service import RootService

class LoginWindow:
    Logon = False

    def __init__(self, title='Login', width=300, height=120):
        self.w = width
        self.h = height

        self.root = tk.Tk(className=title)
        self.root.resizable(False, False)   #禁止修改窗口大小
        self.packCtrls()
        self.center()                       #窗口居中
        self.root.mainloop()

    def center(self):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = int((ws - self.w)/2)
        y = int((hs - self.h)/2)
        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))

    def packCtrls(self):
        tk.Label(self.root, text='Please Enter The Root Password:', anchor='w').pack()

        self.pwd = tk.StringVar()
        entry = tk.Entry(self.root, textvariable=self.pwd)
        entry['show']="*"
        entry.pack()

        tk.Button(self.root, text='Login', command=self.authenticate, width=10).pack(padx=30, side='left')
        tk.Button(self.root, text='Close', command=self.root.quit, width=10).pack(padx=30, side='right')

    def authenticate(self):
        rService = RootService()
        self.Logon = rService.authentication(self.pwd.get())
        if self.Logon:
            self.root.destroy()
        else:
            tkMessageBox.showerror("Account Manager", "Password error, please reenter!")

class MainWindow:
    def __init__(self, title='Main', width=300, height=120):
        self.w = width
        self.h = height

        self.root = tk.Tk(className=title)

    def Show(self):
        self.root.mainloop()
