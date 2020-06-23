import tkinter as tk
from datetime import date
from tkinter import ttk
from View import view
from tkcalendar import DateEntry

MODES = [
    "Backlog",
    "Todo",
    "Testing"
]
NORM_FONT = ("Verdana", 10)


class FilterTasks:

    def __init__(self, t):
        self.mTk = t
        self.mTk.resizable(0, 0)
        self.mTk.wm_title("Filtering Tasks")
        self.mIsTodo = True
        self.mIsTesting = True
        self.mIsBacklog = True

        # mode
        label_mode = ttk.Label(self.mTk, text="Mode", font=NORM_FONT)
        label_mode.pack(side="top", fill="x", pady=(5, 2), padx=5)
        self.mBtnBacklog = tk.Button(self.mTk, text=MODES[0], width=25, bg="peach puff", fg="white",
                                     command=self.backlogClicked)
        self.mBtnBacklog.pack(anchor=tk.W, fill="x", pady=2, padx=10)
        self.mBtnTodo = tk.Button(self.mTk, text=MODES[1], width=25, bg="blue", fg="white",
                                  command=self.todoClicked)
        self.mBtnTodo.pack(anchor=tk.W, fill="x", pady=2, padx=10)
        self.mBtnTesting = tk.Button(self.mTk, text=MODES[2], width=25, bg="yellow2", fg="white",
                                     command=self.testingClicked)
        self.mBtnTesting.pack(anchor=tk.W, fill="x", pady=2, padx=10)

        # type
        label_type = ttk.Label(self.mTk, text="Type", font=NORM_FONT)
        label_type.pack(side="top", fill="x", pady=(5, 2), padx=5)
        frame_type = ttk.Frame(self.mTk)
        self.mIsBugOn = True
        self.mIsBonusOn = True
        self.mBtnBug = tk.Button(frame_type, text="Bug ON", command=self.bugClicked)

        # get default button color
        self.mOrigBtnColor = self.mBtnBug.cget("bg")

        # type continued
        self.mBtnBug.config(bg="red", fg="white")
        self.mBtnBug.pack(side="left", expand=True, fill='both', padx=5, pady=5)
        self.mBtnBonus = tk.Button(frame_type, text="Bonus ON", command=self.bonusClicked, bg="purple", fg="white")
        self.mBtnBonus.pack(side="right", expand=True, fill='both', padx=5, pady=5)
        frame_type.pack(side="top", fill="x")

        frame_type2 = ttk.Frame(self.mTk)
        self.mIsBugOff = True
        self.mIsBonusOff = True
        self.mBtnBugOff = tk.Button(frame_type2, text="Bug OFF", command=self.bugOffClicked, bg="red2", fg="white")
        self.mBtnBugOff.pack(side="left", expand=True, fill='both', padx=5, pady=5)
        self.mBtnBonusOff = tk.Button(frame_type2, text="Bonus OFF", command=self.bonusOffClicked, bg="purple2",
                                      fg="white")
        self.mBtnBonusOff.pack(side="right", expand=True, fill='both', padx=5, pady=5)
        frame_type2.pack(side="top", fill="x")

        # initial date labels
        frame_label_init_date = ttk.Frame(self.mTk)
        label_initial_date_min = ttk.Label(frame_label_init_date, text="Initial Date Min", font=NORM_FONT)
        label_initial_date_min.pack(side="left", fill="x", pady=(5, 0), padx=5)
        label_initial_date_max = ttk.Label(frame_label_init_date, text="Initial Date Max", font=NORM_FONT)
        label_initial_date_max.pack(side="right", fill="x", pady=(5, 0), padx=5)
        frame_label_init_date.pack(side="top", fill="x")

        # initial date
        frame_init_date = ttk.Frame(self.mTk)
        self.mDEInitialMin = DateEntry(frame_init_date, width=12, background='blue', foreground='white', borderwidth=2)
        self.mDEInitialMin.set_date(date.min)
        self.mDEInitialMin.bind("<<DateEntrySelected>>", self.dEInitialMinClicked)
        self.mDEInitialMin.pack(side="left", expand=True, fill='both', pady=5, padx=5)
        self.mDEInitialMax = DateEntry(frame_init_date, width=12, background='blue', foreground='white', borderwidth=2)
        self.mDEInitialMax.set_date(date.max)
        self.mDEInitialMax.pack(side="right", expand=True, fill='both', pady=5, padx=5)
        self.mDEInitialMax.bind("<<DateEntrySelected>>", self.dEInitialMaxClicked)
        frame_init_date.pack(side="top", fill="x")

        # due date labels
        frame_label_due_date = ttk.Frame(self.mTk)
        label_due_date_min = ttk.Label(frame_label_due_date, text="Due Date Min", font=NORM_FONT)
        label_due_date_min.pack(side="left", fill="x", pady=5, padx=5)
        label_initial_date_max = ttk.Label(frame_label_due_date, text="Due Date Max", font=NORM_FONT)
        label_initial_date_max.pack(side="right", fill="x", pady=5, padx=5)
        frame_label_due_date.pack(side="top", fill="x")

        # due date
        frame_due_date = ttk.Frame(self.mTk)
        self.mDEDueMin = DateEntry(frame_due_date, width=12, background='blue', foreground='white', borderwidth=2)
        self.mDEDueMin.set_date(date.min)
        self.mDEDueMin.bind("<<DateEntrySelected>>", self.dEDueMinClicked)
        self.mDEDueMin.pack(side="left", expand=True, fill='both', pady=5, padx=5)
        self.mDEDueMax = DateEntry(frame_due_date, width=12, background='blue', foreground='white', borderwidth=2)
        self.mDEDueMax.bind("<<DateEntrySelected>>", self.dEDueMaxClicked)
        self.mDEDueMax.set_date(date.max)
        self.mDEDueMax.pack(side="right", expand=True, fill='both', pady=5, padx=5)
        frame_due_date.pack(side="top", fill="x")

        # severity min
        self.mScaleSeverityMin = tk.Scale(self.mTk, from_=1.0, to=10.0, tickinterval=1, orient="horizontal",
                                          command=self.minScaleMoved)
        label_severity_min = ttk.Label(self.mTk, text="Min Severity", font=NORM_FONT)
        label_severity_min.pack(side="top", fill="x", pady=(5, 0), padx=5)
        self.mScaleSeverityMin.pack(side="top", fill="x", padx=10)

        # severity max
        self.mScaleSeverityMax = tk.Scale(self.mTk, from_=1.0, to=10.0, tickinterval=1, orient="horizontal",
                                          command=self.maxScaleMoved)
        self.mScaleSeverityMax.set(10)
        label_severity_max = ttk.Label(self.mTk, text="Max Severity", font=NORM_FONT)
        label_severity_max = ttk.Label(self.mTk, text="Max Severity", font=NORM_FONT)
        label_severity_max.pack(side="top", fill="x", padx=5)
        self.mScaleSeverityMax.pack(side="top", fill="x", padx=10)

        # in progress
        self.mIsYes = True
        self.mIsNo = True
        label_in_progress = ttk.Label(self.mTk, text="In Progress", font=NORM_FONT)
        label_in_progress.pack(side="top", fill="x", pady=(0, 2), padx=5)
        frame_in_progress = ttk.Frame(self.mTk)
        self.mBtnYes = tk.Button(frame_in_progress, text="Yes", width=30, bg="green", fg="white",
                                 command=self.yesClicked)
        self.mBtnYes.pack(side="left", fill="x", pady=(2, 8), padx=(10, 5))
        self.mBtnNo = tk.Button(frame_in_progress, text="No", width=30, bg="red", fg="white",
                                command=self.noClicked)
        self.mBtnNo.pack(side="right", fill="x", pady=(2, 8), padx=(5, 10))
        frame_in_progress.pack(side="top", fill="x")

        # in done
        self.mIsDoneOn = True
        self.mIsDoneOff = True
        label_done = ttk.Label(self.mTk, text="Done", font=NORM_FONT)
        label_done.pack(side="top", fill="x", pady=(0, 2), padx=5)
        frame_done = ttk.Frame(self.mTk)
        self.mBtnDoneOn = tk.Button(frame_done, text="Yes", width=30, bg="green", fg="white",
                                    command=self.doneOnClicked)
        self.mBtnDoneOn.pack(side="left", fill="x", pady=(2, 8), padx=(10, 5))
        self.mBtnDoneOff = tk.Button(frame_done, text="No", width=30, bg="red", fg="white",
                                     command=self.doneOffClicked)
        self.mBtnDoneOff.pack(side="right", fill="x", pady=(2, 8), padx=(5, 10))
        frame_done.pack(side="top", fill="x")

        separator = ttk.Separator(self.mTk, orient="horizontal")
        separator.pack(side="top", fill="x", padx=5)

        # commands
        self.mFrameCommand = ttk.Frame(self.mTk)
        self.mBtnSubmit = tk.Button(self.mFrameCommand, text="Filter", bg="gray", fg="white")
        self.mBtnSubmit.pack(side="left", expand=True, fill='both', padx=5, pady=5)
        self.mBtnCancel = tk.Button(self.mFrameCommand, text="Cancel", command=self.mTk.destroy)
        self.mBtnCancel.pack(side="right", expand=True, fill='both', padx=5, pady=5)
        self.mFrameCommand.pack(side="top", fill="x")
        view.center(self.mTk)

    def bugClicked(self):
        if self.mIsBugOn:
            self.mBtnBug.config(bg=self.mOrigBtnColor, fg="black")
        else:
            self.mBtnBug.config(bg="red", fg="white")
        self.mIsBugOn = not self.mIsBugOn

    def bonusClicked(self):
        if self.mIsBonusOn:
            self.mBtnBonus.config(bg=self.mOrigBtnColor, fg="black")
        else:
            self.mBtnBonus.config(bg="purple", fg="white")
        self.mIsBonusOn = not self.mIsBonusOn

    def bugOffClicked(self):
        if self.mIsBugOff:
            self.mBtnBugOff.config(bg=self.mOrigBtnColor, fg="black")
        else:
            self.mBtnBugOff.config(bg="red2", fg="white")
        self.mIsBugOff = not self.mIsBugOff

    def bonusOffClicked(self):
        if self.mIsBonusOff:
            self.mBtnBonusOff.config(bg=self.mOrigBtnColor, fg="black")
        else:
            self.mBtnBonusOff.config(bg="purple2", fg="white")
        self.mIsBonusOff = not self.mIsBonusOff

    def minScaleMoved(self, instance):
        if self.mScaleSeverityMin.get() > self.mScaleSeverityMax.get():
            self.mScaleSeverityMax.set(self.mScaleSeverityMin.get())

    def maxScaleMoved(self, instance):
        if self.mScaleSeverityMin.get() > self.mScaleSeverityMax.get():
            self.mScaleSeverityMin.set(self.mScaleSeverityMax.get())

    def dEInitialMinClicked(self, instance):
        if self.mDEInitialMin.get() > self.mDEInitialMax.get():
            self.mDEInitialMax.set_date(self.mDEInitialMin.get_date())

    def dEInitialMaxClicked(self, instance):
        if self.mDEInitialMin.get() > self.mDEInitialMax.get():
            self.mDEInitialMin.set_date(self.mDEInitialMax.get_date())

    def dEDueMinClicked(self, instance):
        if self.mDEDueMin.get() > self.mDEDueMax.get():
            self.mDEDueMax.set_date(self.mDEDueMin.get_date())

    def dEDueMaxClicked(self, instance):
        if self.mDEDueMin.get() > self.mDEDueMax.get():
            self.mDEDueMin.set_date(self.mDEDueMax.get_date())

    def todoClicked(self):
        if self.mIsTodo:
            self.mBtnTodo.config(fg="black", bg=self.mOrigBtnColor)
        else:
            self.mBtnTodo.config(fg="white", bg="blue")
        self.mIsTodo = not self.mIsTodo

    def testingClicked(self):
        if self.mIsTesting:
            self.mBtnTesting.config(fg="black", bg=self.mOrigBtnColor)
        else:
            self.mBtnTesting.config(fg="white", bg="yellow2")
        self.mIsTesting = not self.mIsTesting

    def backlogClicked(self):
        if self.mIsBacklog:
            self.mBtnBacklog.config(fg="black", bg=self.mOrigBtnColor)
        else:
            self.mBtnBacklog.config(fg="white", bg="peach puff")
        self.mIsBacklog = not self.mIsBacklog

    def yesClicked(self):
        if self.mIsYes:
            self.mBtnYes.config(fg="black", bg=self.mOrigBtnColor)
        else:
            self.mBtnYes.config(fg="white", bg="green")
        self.mIsYes = not self.mIsYes

    def noClicked(self):
        if self.mIsNo:
            self.mBtnNo.config(fg="black", bg=self.mOrigBtnColor)
        else:
            self.mBtnNo.config(fg="white", bg="red")
        self.mIsNo = not self.mIsNo

    def doneOnClicked(self):
        if self.mIsDoneOn:
            self.mBtnDoneOn.config(fg="black", bg=self.mOrigBtnColor)
        else:
            self.mBtnDoneOn.config(fg="white", bg="green")
        self.mIsDoneOn = not self.mIsDoneOn

    def doneOffClicked(self):
        if self.mIsDoneOff:
            self.mBtnDoneOff.config(fg="black", bg=self.mOrigBtnColor)
        else:
            self.mBtnDoneOff.config(fg="white", bg="red")
        self.mIsDoneOff = not self.mIsDoneOff
