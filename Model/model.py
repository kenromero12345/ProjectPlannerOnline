from tkinter.filedialog import asksaveasfilename, askopenfilename
import pickle
from pathlib import Path
import os

from Model.save import Save

files = [('All Files', '*.*'),
         ('Python Files', '*.py'),
         ('Text Document', '*.txt')]


class Model:

    def __init__(self):
        self.mTaskList = []
        self.mProjectList = []
        self.mMemberList = []
        self.mUserID = ""
        self.mUsername = ""
        self.mSavedPath = None
        self.mProjectName = ""
        self.mPassword = ""

    def sort_by_title(self, reverse):
        self.mTaskList.sort(reverse=reverse, key=lambda t: t.mTitle)

    def sort_by_mode(self, reverse):
        self.mTaskList.sort(reverse=reverse, key=lambda t: t.mMode)

    def sort_by_in_progress(self, reverse):
        self.mTaskList.sort(reverse=reverse, key=lambda t: t.mInProgress)

    def sort_by_initial_date(self, reverse):
        self.mTaskList.sort(reverse=reverse, key=lambda t: t.mInitialDate)

    def sort_by_due_date(self, reverse):
        self.mTaskList.sort(reverse=reverse, key=lambda t: t.mDueDate)

    def sort_by_severity(self, reverse):
        self.mTaskList.sort(reverse=reverse, key=lambda t: t.mSeverity)

    def load_task_list(self):
        file = askopenfilename(filetypes=files, defaultextension=files)
        if not file:  # askopenfilename return `None` if dialog closed with "cancel".
            return False
        self.load(file)
        return True

    def load(self, file):
        var = pickle.load(open(file, "rb"))
        self.mUsername = var.mUsername
        self.mPassword = var.mPassword

    def save(self, file):
        var = Save(self.mUsername, self.mPassword)
        pickle.dump(var, open(file, "wb"))

    # def load(self, file):
    #     var = pickle.load(open(file, "rb"))
    #     self.mTaskList = var.mTaskList
    #     self.mProjectName = var.mProjectName
    #
    # def load_path(self, file):
    #     self.mSavedPath = pickle.load(open(file, "rb"))
    #     self.mProjectName = self.mSavedPath.split("/")[-1].split(".")[0]
    #
    # def save_as_task_list(self):
    #     file = asksaveasfilename(filetypes=files, defaultextension=files)
    #     if not file:  # asksaveasfilename return `None` if dialog closed with "cancel".
    #         return False
    #     self.save(file)
    #     self.mSavedPath = file
    #     self.mProjectName = self.mSavedPath.split("/")[-1].split(".")[0]
    #     self.save_path(str(Path(os.getcwd()).parent) + "\\auto_save_path.txt")
    #     return True
    #
    # def save_task_list(self):
    #     self.save(self.mSavedPath)
    #
    # def save(self, file):
    #     var = Save(self.mProjectName, self.mTaskList)
    #     pickle.dump(var, open(file, "wb"))
    #
    # def save_path(self, file):
    #     pickle.dump(self.mSavedPath, open(file, "wb"))

    def getNames(self):
        lst = []
        for m in self.mMemberList:
            lst.append(m.mName)
        return lst
