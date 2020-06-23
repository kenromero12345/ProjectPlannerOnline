class Task:
    def __init__(self, title, desc, mode, assignees, severity, in_progress, init_date, due_date, isBug, isBonus, isDone):
        self.mTitle = title
        self.mDesc = desc
        self.mMode = mode
        if self.mMode == "Backlog":
            self.mIsBacklog = True
            self.mIsTodo = False
            self.mIsTesting = False
        elif self.mMode == "Todo":
            self.mIsBacklog = False
            self.mIsTodo = True
            self.mIsTesting = False
        elif self.mMode == "Testing":
            self.mIsBacklog = False
            self.mIsTodo = False
            self.mIsTesting = True
        self.mAssignees = assignees
        self.mSeverity = severity
        self.mInProgress = in_progress
        if self.mInProgress:
            self.mIsYes = True
            self.mIsNo = False
        else:
            self.mIsNo = True
            self.mIsYes = False
        self.mInitialDate = init_date
        self.mDueDate = due_date
        self.mIsBug = isBug
        if self.mIsBug:
            self.mIsBugOn = True
            self.mIsBugOff = False
        else:
            self.mIsBugOff = True
            self.mIsBugOn = False
        self.mIsBonus = isBonus
        if self.mIsBonus:
            self.mIsBonusOn = True
            self.mIsBonusOff = False
        else:
            self.mIsBonusOff = True
            self.mIsBonusOn = False
        self.mIsDone = isDone
        if self.mIsDone:
            self.mIsDoneOn = True
            self.mIsDoneOff = False
        else:
            self.mIsDoneOff = True
            self.mIsDoneOn = False
