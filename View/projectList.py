import tkinter as tk
from tkinter import ttk

from View import view
# from View.view import center
from View import view

WIDTH = 45
cols = ("Name",)


class ProjectList:
    def __init__(self, frame):
        self.mTk = frame
        top_frame = tk.Frame(frame)
        self.mBtnAddTask = tk.Button(top_frame, text="Add Project", width=WIDTH)
        self.mBtnAddTask.pack(side="left", expand=True, fill='both', padx=5, pady=(5, 0))
        top_frame.pack(side="top", expand=True, fill='both')

        bottom_frame = tk.Frame(frame)

        self.mTvProjectList = ttk.Treeview(bottom_frame, columns=cols, show='headings')

        self.mTvProjectList.heading("Name", text="Name", anchor="center")

        self.mTvProjectList.column("Name", minwidth=300, width=300, stretch=False, anchor="w")
        self.mTvProjectList.pack(side="left", expand=True, fill='both', padx=(5, 0), pady=5)

        self.mScrollbar = ttk.Scrollbar(bottom_frame, orient="vertical", command=self.mTvProjectList.yview)
        self.mScrollbar.pack(side="left", expand=True, fill='both', padx=(0, 5), pady=5)
        self.mTvProjectList.configure(yscrollcommand=self.mScrollbar.set)

        bottom_frame.pack(side="top", expand=True, fill='both')

        view.center(self.mTk)

        self.mTk.wm_title("Project Planner - Projects")
