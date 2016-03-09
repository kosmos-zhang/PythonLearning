#coding: utf-8

import sys, os
import tkinter as tk
import tkMessageBox
from utils.service import RootService

class AccWindows(tk.Tk):
    def __init__(self, title, width, height):
        tk.Tk.__init__(self, className=title)
        self.w = width
        self.h = height

        self.title(title)
        self.iconbitmap('icons/am.ico')

    def _center(self):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int((ws - self.w) / 2)
        y = int((hs - self.h) / 2)

        self.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))

class LoginWindow(AccWindows):
    Logon = False

    def __init__(self, title='Login', width=300, height=120):
        AccWindows.__init__(self, title, width, height)

        self.resizable(False, False)   #禁止修改窗口大小
        self.packCtrls()
        self._center()

    def packCtrls(self):
        tk.Label(self, text='Please Enter The Root Password:', anchor='w').pack()

        self.pwd = tk.StringVar()
        entry = tk.Entry(self, textvariable=self.pwd, show='*')
        entry.pack()
        entry.focus_set()
        entry.bind('<Return>', self.authenticate)

        tk.Button(self, text='Login', command=self.authenticate, width=10).pack(padx=30, side='left')
        tk.Button(self, text='Close', command=self.quit, width=10).pack(padx=30, side='right')

    def authenticate(self, *args):
        rService = RootService()
        self.Logon = rService.authentication(self.pwd.get())
        if self.Logon:
            self.destroy()
        else:
            tkMessageBox.showerror("Account Manager", "Password error, please reenter!")

class MainWindow(AccWindows):
    def __init__(self, title='Account Manager', width=800, height=600):
        AccWindows.__init__(self, title, width, height)

        # create menu
        self.__createMenu()
        
        # toolbar
        self.__createToolBar()
        
        # splitter window
        self.__createSplitterWindow()
        
        # set the status bar
        self.__createStatusBar()

        self._center()

    def __createMenu(self):
        menuData = (
                    (0, 'Account',      (0, 'New Account', 'Add new account', self.onNewAcc, 'Ctrl+N', '<Control-n>'),
                                        (0, 'Account details', 'Show detailed information of selected account', self.onShowDetail, '', ''),
                                        (0, 'Edit account', 'Edit the selected account', self.onEditAccount, '', ''),
                                        (0, 'Move to trash', 'Move selected account to trash', self.onRemove, '', ''),
                                        (0, 'Recover from trash', 'Recover selected account from', self.onRecover, '', ''),
                                        (5, 'Remove selected account', 'Remove selected account', self.onRemove, '', ''),
                                        (-1, '', '', '', '', ''),
                                        (0, 'Quit', 'Quit Account Manager', self.onQuit, 'Ctrl+Q', '<Control-q>'),
                    ), (0, 'Setting',   (0, 'Root password', 'managing root password', self.onRootPwd, '', ''),
                                        (0, 'Password Generator', 'Generating a random password', self.onPwdGen, '', ''),
                                        (0, 'New Tag', 'Add new Tag', self.onNewTag, '', ''),
                                        (0, 'Empty trash', 'Empty trash', self.onEmptyTrash, '', ''),
                    ), (0, 'Help',      (0, 'About', 'About Account Manager...', self.onAbout, '', ''),
                   ), )

        menubar = tk.Menu(self)

        for entry in menuData:
            menuShortcut = entry[0]
            menuLabel = entry[1]
            menuItems = entry[2:]
            menubar.add_cascade(label=menuLabel, underline=menuShortcut, menu=self.__getMenu(menubar, menuItems))

        # display the menu
        self.config(menu=menubar)

    def __getMenu(self, menubar, menuItems):
        menu = tk.Menu(menubar, tearoff=0)
        for underline, label, hint, handler, accelerator, bindkey in menuItems:
            if not label:
                menu.add_separator()
                continue

            menu.add_command(label=label, underline=underline, command=handler, accelerator=accelerator)

            if accelerator:
                self.bind_all(bindkey, handler)

        return menu

    def __createToolBar(self):
        toolbar = tk.Canvas(self, bg='#00FF00', height=30)
        toolbar.pack(fill=tk.BOTH)

    def __createSplitterWindow(self):
        panedWindow = tk.PanedWindow(orient=tk.HORIZONTAL)
        panedWindow.pack(fill=tk.BOTH, expand=1)

        left = tk.Canvas(panedWindow, bg='#0000FF', width=150)
        panedWindow.add(left)

        right = tk.Label(panedWindow, text='Right pane', bg='#FF0000')
        panedWindow.add(right)

    def __createStatusBar(self):
        statusbar = tk.Label(self, text='Welcome to use Account Manager!')
        statusbar.pack(padx=10, side='left')

    def onNewAcc(self, *args):
        print 'new account'

    def onShowDetail(self):
        pass

    def onEditAccount(self):
        pass

    def onRemove(self):
        pass

    def onRecover(self):
        pass

    def onQuit(self, *args):
        self.quit()

    def onRootPwd(self):
        pass

    def onPwdGen(self):
        pass

    def onNewTag(self):
        pass

    def onEmptyTrash(self):
        pass

    def onAbout(self):
        pass
