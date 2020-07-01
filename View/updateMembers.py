import tkinter as tk
from tkinter import ttk
from View import view

cols = ("Name",)
WIDTH = 45


class UpdateMembers:
    def __init__(self, frame):
        self.mTk = frame
        self.mTk.resizable(0, 0)
        top_frame = tk.Frame(frame)

        self.mBtnAddMember = tk.Button(top_frame, text="Add Member", width=WIDTH)
        self.mBtnAddMember.pack(side="left", expand=True, fill='both', padx=5, pady=(5, 0))

        top_frame.pack(side="top", expand=True, fill='both')

        bottom_frame = tk.Frame(frame)

        self.mTvMemberList = ttk.Treeview(bottom_frame, columns=cols, show='headings')

        self.mTvMemberList.heading("Name", text="Name", anchor="center")
        # for col in cols:
        #     self.mTvTaskList.heading(col, text=col, anchor="center")
        #
        # for col in cols:
        #     self.mTvTaskList.column(col, minwidth=66, width=66, stretch=False, anchor="center")

        self.mTvMemberList.column("Name", minwidth=300, width=300, stretch=False, anchor="w")
        self.mTvMemberList.pack(side="left", expand=True, fill='both', padx=(5, 0), pady=5)

        self.mScrollbar = ttk.Scrollbar(bottom_frame, orient="vertical", command=self.mTvMemberList.yview)
        self.mScrollbar.pack(side="left", expand=True, fill='both', padx=(0, 5), pady=5)
        self.mTvMemberList.configure(yscrollcommand=self.mScrollbar.set)

        bottom_frame.pack(side="top", expand=True, fill='both')
        view.center(self.mTk)

