import tkinter as tk
from tkinter import ttk

from View.view import center

NORM_FONT = ("Verdana", 10)


class Register:
    def __init__(self, frame):
        self.mTk = frame
        top_frame = tk.Frame(frame)
        label_username = tk.Label(top_frame, text="Username", width=10, anchor=tk.W, justify=tk.LEFT)
        label_username.pack(side="left", expand=True, fill='both', padx=5, pady=5)
        self.mVarUsername = tk.StringVar(self.mTk)
        self.mVarUsername.set("")
        entry_username = ttk.Entry(top_frame, font=NORM_FONT, textvariable=self.mVarUsername)
        entry_username.pack(side="left", expand=True, padx=5)
        top_frame.pack(side="top", expand=True, fill='both')

        mid_frame = tk.Frame(frame)
        label_password = tk.Label(mid_frame, text="Password",
                                  width=10, anchor=tk.W, justify=tk.LEFT)
        label_password.pack(side="left", expand=True, fill='both', padx=5)
        self.mVarPassword = tk.StringVar(self.mTk)
        self.mVarPassword.set("")
        entry_password = ttk.Entry(mid_frame, show="*", font=NORM_FONT, textvariable=self.mVarPassword)
        entry_password.pack(side="left", expand=True, fill='both', padx=5)
        mid_frame.pack(side="top", expand=True, fill='both')

        bottom_frame = tk.Frame(frame)
        label_re_password = tk.Label(bottom_frame, text="Re-Password", width=10, anchor=tk.W, justify=tk.LEFT)
        label_re_password.pack(side="left", expand=True, fill='both', padx=5, pady=5)
        self.mVarRePassword = tk.StringVar(self.mTk)
        self.mVarRePassword.set("")
        entry_re_password = ttk.Entry(bottom_frame, show="*", font=NORM_FONT, textvariable=self.mVarRePassword)
        entry_re_password.pack(side="left", expand=True, padx=5)
        bottom_frame.pack(side="top", expand=True, fill='both')

        # bottom_frame = tk.Frame(frame)
        self.mBtnRegister = tk.Button(frame, text="Register", width=10)
        self.mBtnRegister.pack(side="left", expand=True, fill='both', padx=5, pady=5)
        self.mBtnCancel = tk.Button(frame, text="Cancel", width=10)
        self.mBtnCancel.pack(side="left", expand=True, fill='both', padx=5, pady=5)
        self.mTk.resizable(False, False)
        # bottom_frame.pack(side="top", expand=True, fill='both')

        self.mTk.wm_title("Register")

        center(frame)
