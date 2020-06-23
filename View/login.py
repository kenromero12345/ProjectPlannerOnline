import tkinter as tk
from tkinter import ttk

# from View.view import center

NORM_FONT = ("Verdana", 10)


class Login:
    def __init__(self, frame):
        self.mTk = frame
        top_frame = tk.Frame(frame)
        label_username = tk.Label(top_frame, text="Username", width=10)
        label_username.pack(side="left", expand=True, fill='both', padx=5, pady=5)
        self.mVarUsername = tk.StringVar(self.mTk)
        self.mVarUsername.set("")
        entry_username = ttk.Entry(top_frame, font=NORM_FONT, textvariable=self.mVarUsername)
        entry_username.pack(side="left", expand=True, padx=5)
        top_frame.pack(side="top", expand=True, fill='both')

        mid_frame = tk.Frame(frame)
        label_password = tk.Label(mid_frame, text="Password",
                                  width=10)
        label_password.pack(side="left", expand=True, fill='both', padx=5)
        self.mVarPassword = tk.StringVar(self.mTk)
        self.mVarPassword.set("")
        entry_password = ttk.Entry(mid_frame, show="*", font=NORM_FONT, textvariable=self.mVarPassword)
        entry_password.pack(side="left", expand=True, fill='both', padx=5)
        mid_frame.pack(side="top", expand=True, fill='both')

        # bottom_frame = tk.Frame(frame)
        self.mBtnRegister = tk.Button(frame, text="Register", width=10)
        self.mBtnRegister.pack(side="left", expand=True, fill='both', padx=5, pady=5)
        self.mBtnLogin = tk.Button(frame, text="Login", width=10)
        self.mBtnLogin.pack(side="left", expand=True, fill='both', padx=5, pady=5)
        # bottom_frame.pack(side="top", expand=True, fill='both')

        # self.mTk.wm_title("Login")

        # center(frame)
