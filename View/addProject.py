import tkinter as tk
from tkinter import ttk
from View import view

NORM_FONT = ("Verdana", 10)


class AddProject:

    def __init__(self, t):
        self.mTk = t
        self.mTk.resizable(0, 0)
        top_frame = tk.Frame(t)
        self.mVarName = tk.StringVar(self.mTk)
        self.mVarName.set("")
        entry_project = ttk.Entry(self.mTk, font=NORM_FONT, textvariable=self.mVarName)
        self.mTk.wm_title("Adding Project...")
        label_name = ttk.Label(self.mTk, text="Name", font=NORM_FONT)
        label_name.pack(side="top", fill="x", pady=(5, 2), padx=5)
        entry_project.pack(side="top", fill="x", padx=10)
        label_description = ttk.Label(self.mTk, text="Description", font=NORM_FONT)
        label_description.pack(side="top", fill="x", pady=(5, 2), padx=5)
        self.mTextDescription = tk.Text(self.mTk, height=5, width=40)
        self.mTextDescription.pack(side="top", fill="x", pady=(0, 2), padx=10)
        top_frame.pack(side="top", expand=True, fill='both')
        self.mFrameCommand = ttk.Frame(self.mTk)
        self.mBtnSubmit = tk.Button(self.mFrameCommand, text="Submit", bg="green", fg="white")
        self.mBtnSubmit.pack(side="left", expand=True, fill='both', padx=5, pady=5)
        self.mBtnCancel = tk.Button(self.mFrameCommand, text="Cancel")
        self.mBtnCancel.pack(side="right", expand=True, fill='both', padx=5, pady=5)
        self.mFrameCommand.pack(side="top", fill="x")
        view.center(self.mTk)
