import tkinter as tk

from View.addTask import AddTask
from datetime import datetime

class UpdateTask(AddTask):
    def __init__(self, t, members, member_names, task):
        AddTask.__init__(self, t, members, member_names)
        self.mVarTitle.set(task.mTitle)
        self.mVarInProgress.set(task.mInProgress)
        self.mScaleSeverity.set(task.mSeverity)
        # self.mVarAssignees.set(task.mAssignees)
        for a in task.mAssignees:
            # self.mLBAssignees.activate(self.mLBAssignees.get(0, "end").index(a))
            index = self.mLBAssignees.get(0, "end").index(a)
            self.mLBAssignees.selection_set(index)
            self.mLBAssignees.see(index)
            self.mLBAssignees.activate(index)
            self.mLBAssignees.selection_anchor(index)

        # print(task.mAssignees)

        self.mVarMode.set(task.mMode)
        if isinstance(task.mInitialDate, str):
            self.mDEInitial.set_date(datetime.strptime(task.mInitialDate, '%Y-%m-%d'))
        else:
            self.mDEInitial.set_date(task.mInitialDate)
        self.mIsBug = task.mIsBugOn
        self.mIsBonus = task.mIsBonusOn
        if self.mIsBug:
            self.bugClicked()  # duplicate needed because it changes the variable
            self.bugClicked()
        if self.mIsBonus:
            self.bonusClicked()  # duplicate needed
            self.bonusClicked()
        self.mTextDescription.insert(1.0, task.mDesc)
        self.mBtnSubmit.config(text="Update")
        self.mBtnDelete = tk.Button(self.mFrameCommand, text="Delete", bg='red', fg='white')
        self.mBtnSubmit.config(bg="yellow2")
        self.mBtnDelete.pack(side="right", expand=True, fill='both', padx=5, pady=5)
        if task.mIsDone:
            self.mCloseOpenBtn = tk.Button(self.mFrameCommand, text="Open", bg="orange", fg="white")
        else:
            self.mCloseOpenBtn = tk.Button(self.mFrameCommand, text="Close", bg="green", fg="white")
        self.mCloseOpenBtn.pack(side="right", expand=True, fill='both', padx=5, pady=5)
        self.mOldTitle = task.mTitle
        self.mTk.wm_title("Updating Task...")
