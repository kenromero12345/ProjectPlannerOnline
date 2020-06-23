import tkinter as tk
from tkinter import ttk

from Model.member import Member
from View import view
from tkcalendar import DateEntry

NORM_FONT = ("Verdana", 10)
MODES = [
    "Backlog",
    "Todo",
    "Testing"
]


class AddTask:

    def __init__(self, t, members, member_names):
        self.mTk = t
        self.mTk.resizable(0, 0)
        self.mVarInProgress = tk.StringVar(self.mTk)
        self.mScaleSeverity = tk.Scale(self.mTk, from_=1.0, to=10.0, tickinterval=1, orient="horizontal")
        self.mVarAssignees = tk.StringVar(self.mTk)
        self.mVarMode = tk.StringVar(self.mTk)
        self.mTextDescription = tk.Text(self.mTk, height=5, width=20)
        self.mVarTitle = tk.StringVar(self.mTk)
        self.mVarTitle.set("")
        m_entry_title = ttk.Entry(self.mTk, font=NORM_FONT, textvariable=self.mVarTitle)
        self.mTk.wm_title("Adding Task...")
        label_title = ttk.Label(self.mTk, text="Title", font=NORM_FONT)
        label_title.pack(side="top", fill="x", pady=(5, 2), padx=5)
        m_entry_title.pack(side="top", fill="x", padx=10)
        label_description = ttk.Label(self.mTk, text="Description", font=NORM_FONT)
        label_description.pack(side="top", fill="x", pady=(5, 2), padx=5)
        self.mTextDescription.pack(side="top", fill="x", padx=10)
        label_mode = ttk.Label(self.mTk, text="Mode", font=NORM_FONT)
        label_mode.pack(side="top", fill="x", pady=(5, 2), padx=5)
        self.mVarMode.set(MODES[0])  # initialize
        # for text in MODES:
        self.mRBtnBacklog = tk.Radiobutton(self.mTk, text=MODES[0], indicatoron=0, width=25, val=MODES[0],
                                           variable=self.mVarMode, command=self.backlogClicked,
                                           selectcolor="peach puff", fg="white")
        self.mRBtnBacklog.pack(anchor=tk.W, fill="x", pady=2, padx=10)
        self.mRBtnTodo = tk.Radiobutton(self.mTk, text=MODES[1], indicatoron=0, width=25, val=MODES[1],
                                        variable=self.mVarMode, command=self.todoClicked, selectcolor="blue")
        self.mRBtnTodo.pack(anchor=tk.W, fill="x", pady=2, padx=10)
        self.mRBtnTesting = tk.Radiobutton(self.mTk, text=MODES[2], indicatoron=0, width=25, val=MODES[2],
                                           variable=self.mVarMode, command=self.testingClicked, selectcolor="yellow2")
        self.mRBtnTesting.pack(anchor=tk.W, fill="x", pady=2, padx=10)
        label_type = ttk.Label(self.mTk, text="Type", font=NORM_FONT)
        label_type.pack(side="top", fill="x", pady=(5, 2), padx=5)
        frame_type = ttk.Frame(self.mTk)
        self.mIsBug = False
        self.mIsBonus = False
        self.mBtnBug = tk.Button(frame_type, text="Bug", command=self.bugClicked)
        self.mBtnBug.pack(side="left", expand=True, fill='both', padx=5, pady=5)
        self.mBtnBonus = tk.Button(frame_type, text="Bonus", command=self.bonusClicked)
        self.mBtnBonus.pack(side="right", expand=True, fill='both', padx=5, pady=5)
        self.mOrigBtnColor = self.mBtnBug.cget("bg")
        frame_type.pack(side="top", fill="x")
        frame_label_date = ttk.Frame(self.mTk)
        label_initial_date = ttk.Label(frame_label_date, text="Initial Date", font=NORM_FONT)
        label_initial_date.pack(side="left", fill="x", pady=(5, 0), padx=5)
        label_due_date = ttk.Label(frame_label_date, text="Due Date", font=NORM_FONT)
        label_due_date.pack(side="right", fill="x", pady=(5, 0), padx=5)
        frame_label_date.pack(side="top", fill="x")
        frame_date = ttk.Frame(self.mTk)
        self.mDEInitial = DateEntry(frame_date, width=12, background='blue', foreground='white', borderwidth=2)
        self.mDEInitial.pack(side="left", expand=True, fill='both', pady=5, padx=5)
        self.mDEDue = DateEntry(frame_date, width=12, background='blue', foreground='white', borderwidth=2)
        self.mDEDue.pack(side="right", expand=True, fill='both', pady=5, padx=5)
        frame_date.pack(side="top", fill="x")
        label_severity = ttk.Label(self.mTk, text="Severity", font=NORM_FONT)
        label_severity.pack(side="top", fill="x", pady=(5, 0), padx=5)
        self.mScaleSeverity.pack(side="top", fill="x", padx=10)
        self.mVarInProgress.set("Yes")  # initialize
        label_assignees = ttk.Label(self.mTk, text="Assignees", font=NORM_FONT)
        label_assignees.pack(side="top", fill="x", pady=(5, 2), padx=5)
        if len(members) == 0:
            members.append(Member("Me"))
            member_names.append("Me")
        # self.mVarAssignees.set(members[0].mName)
        # cb_assignees = ttk.Combobox(self.mTk, values=member_names, state="readonly",
        #                             textvariable=self.mVarAssignees)
        # cb_assignees.pack(fill="x", padx=5)
        frame_assign = tk.Frame(self.mTk)
        self.mLBAssignees = tk.Listbox(frame_assign, selectmode=tk.MULTIPLE, height=3)
        for item in member_names:
            self.mLBAssignees.insert(tk.END, item)
        self.mLBAssignees.pack(side="left", expand=True, fill='both', padx=(5, 0))

        self.mScrollbar = ttk.Scrollbar(frame_assign, orient="vertical", command=self.mLBAssignees.yview)
        self.mScrollbar.pack(side="left", fill='both', padx=(0, 5), pady=5)
        self.mLBAssignees.configure(yscrollcommand=self.mScrollbar.set)

        frame_assign.pack(side="top", fill="x")

        label_in_progress = ttk.Label(self.mTk, text="In Progress", font=NORM_FONT)
        label_in_progress.pack(side="top", fill="x", pady=(5, 2), padx=5)
        # TODO only if TESTING or TODO not Backlog
        self.mFrameInProgress = ttk.Frame(self.mTk)
        self.mRbtnYes = tk.Radiobutton(self.mFrameInProgress, text="Yes", indicatoron=0, width=30, val="Yes",
                                       variable=self.mVarInProgress, selectcolor="green", fg="white",
                                       command=self.yesClicked)
        self.mRbtnYes.pack(side="left", fill="x", pady=(2, 8), padx=(10, 5))
        self.mRbtnNo = tk.Radiobutton(self.mFrameInProgress, text="No", indicatoron=0, width=30, val="No",
                                      variable=self.mVarInProgress, selectcolor="red", command=self.noClicked)
        self.mRbtnNo.pack(side="right", fill="x", pady=(2, 8), padx=(5, 10))
        self.mFrameInProgress.pack(side="top", fill="x")
        separator = ttk.Separator(self.mTk, orient="horizontal")
        separator.pack(side="top", fill="x", padx=5)
        self.mFrameCommand = ttk.Frame(self.mTk)
        self.mBtnSubmit = tk.Button(self.mFrameCommand, text="Submit", bg="green", fg="white")
        self.mBtnSubmit.pack(side="left", expand=True, fill='both', padx=5, pady=5)
        self.mBtnCancel = tk.Button(self.mFrameCommand, text="Cancel")
        self.mBtnCancel.pack(side="right", expand=True, fill='both', padx=5, pady=5)
        self.mFrameCommand.pack(side="top", fill="x")
        view.center(self.mTk)

    def bugClicked(self):
        if self.mIsBug:
            self.mBtnBug.config(bg=self.mOrigBtnColor, fg="black")
        else:
            self.mBtnBug.config(bg="red", fg="white")
        self.mIsBug = not self.mIsBug

    def bonusClicked(self):
        if self.mIsBonus:
            self.mBtnBonus.config(bg=self.mOrigBtnColor, fg="black")
        else:
            self.mBtnBonus.config(bg="purple", fg="white")
        self.mIsBonus = not self.mIsBonus

    def backlogClicked(self):
        self.mRBtnBacklog.config(fg="white")
        self.mRBtnTesting.config(fg="black")
        self.mRBtnTodo.config(fg="black")

    def todoClicked(self):
        self.mRBtnBacklog.config(fg="black")
        self.mRBtnTesting.config(fg="black")
        self.mRBtnTodo.config(fg="white")

    def testingClicked(self):
        self.mRBtnBacklog.config(fg="black")
        self.mRBtnTesting.config(fg="white")
        self.mRBtnTodo.config(fg="black")

    def yesClicked(self):
        self.mRbtnYes.config(fg="white")
        self.mRbtnNo.config(fg="black")

    def noClicked(self):
        self.mRbtnYes.config(fg="black")
        self.mRbtnNo.config(fg="white")
