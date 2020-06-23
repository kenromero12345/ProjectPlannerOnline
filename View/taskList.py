import tkinter as tk
from tkinter import ttk

cols = ("Title", "Mode", "Severity", "In Progress", "Initial Date", "Due Date", "Bug", "Bonus", "Done")
WIDTH = 45


class TaskList:
    def __init__(self, frame):
        self.mTk = frame
        top_frame = tk.Frame(frame)

        self.mBtnUpdateMember = tk.Button(top_frame, text="Update Member", width=WIDTH)
        self.mBtnUpdateMember.pack(side="right", expand=True, fill='both', padx=5, pady=(5, 0))

        # top_frame_2 = tk.Frame(top_frame)

        self.mBtnAddTask = tk.Button(top_frame, text="Add Task", width=WIDTH)
        self.mBtnAddTask.pack(side="left", expand=True, fill='both', padx=5, pady=(5, 0))

        # self.mBtnDeleteTask = tk.Button(top_frame_2, text="Delete Task", width=WIDTH)
        # self.mBtnDeleteTask.pack(side="left", expand=True, fill='both', padx=5)

        # self.mLblDelete = tk.Label(top_frame_2, text="Delete: OFF", width=WIDTH)
        # self.mLblDelete.pack(side="left", expand=True, fill='both', padx=5)

        # top_frame_2.pack(side="top", expand=True, fill='both')

        top_frame_3 = tk.Frame(frame)

        self.mBtnFilter = tk.Button(top_frame_3, text="Filter", width=WIDTH)
        self.mBtnFilter.pack(side="left", expand=True, fill='both', padx=5)

        self.mBtnResetFilter = tk.Button(top_frame_3, text="Reset Filter", width=WIDTH)
        self.mBtnResetFilter.pack(side="left", expand=True, fill='both', padx=5)

        self.mLblFilter = tk.Label(top_frame_3, text="Filter: OFF", width=WIDTH)
        self.mLblFilter.pack(side="left", expand=True, fill='both', padx=5)

        top_frame_3.pack(side="bottom", expand=True, fill='both', pady=(0, 5))

        top_frame.pack(side="top", expand=True, fill='both')

        bottom_frame = tk.Frame(frame)

        self.mTvTaskList = ttk.Treeview(bottom_frame, columns=cols, show='headings')
        for col in cols:
            self.mTvTaskList.heading(col, text=col, anchor="center")

        for col in cols:
            self.mTvTaskList.column(col, minwidth=66, width=66, stretch=False, anchor="center")

        self.mTvTaskList.column("Title", minwidth=500, width=500, stretch=False, anchor="w")
        self.mTvTaskList.pack(side="left", expand=True, fill='both', padx=(5, 0), pady=5)

        self.mScrollbar = ttk.Scrollbar(bottom_frame, orient="vertical", command=self.mTvTaskList.yview)
        self.mScrollbar.pack(side="left", expand=True, fill='both', padx=(0, 5), pady=5)
        self.mTvTaskList.configure(yscrollcommand=self.mScrollbar.set)

        bottom_frame.pack(side="top", expand=True, fill='both')
