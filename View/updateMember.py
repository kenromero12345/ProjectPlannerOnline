from View.addMember import AddMember
from tkinter import ttk
import tkinter as tk


class UpdateMember(AddMember):
    def __init__(self, t, m):
        AddMember.__init__(self, t)
        self.mOldName = m.mName
        self.mVarName.set(m.mName)
        self.mBtnSubmit.config(text="Update")
        self.mTk.wm_title("Updating Member...")
        self.mBtnDelete = tk.Button(self.mFrameCommand, text="Delete", bg='red', fg='white')
        self.mBtnDelete.pack(side="right", expand=True, fill='both', padx=5, pady=5)