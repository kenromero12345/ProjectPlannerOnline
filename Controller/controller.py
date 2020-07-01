import _pickle
import os
import tkinter as tk
from pathlib import Path
from os import path
from tkinter import messagebox

from Model import model, member
from Model import task
from Model.member import Member
from Model.task import Task
from SQL.connection import insertUser, selectUser, connect, selectUserFromNameAndPW, selectProjectFromUserID, \
    insertProject, deleteProject, selectTasks, selectTasksAssignees, insertMember, selectMembers, deleteMember
from View import view, editDeletePopup, updateMembers
from View.addMember import AddMember
from View.addProject import AddProject
from View.addTask import AddTask
from View.editDeletePopup import EditDeletePopup
from View.filterTasks import FilterTasks
from View.register import Register
from View.updateMember import UpdateMember
from View.updateTask import UpdateTask

DELETE_OFF = "Delete: OFF"

DELETE_ON = "Delete: ON"

ABOUT_MSG = "A python application for project planning for programmers to use to be efficient in their tasks with " \
            "their team or their own.\n\nCreated by Ken Gil Romero, a master student of University of Washington"

HELP_MSG = "A little tutorial to help users use the application.\n\nTo Add a task, click the add task button or the " \
           "File menu then New...\n\tA new window will appear where the user will input information for a task "

PROJECT_MSG = "A little tutorial to help users use the application.\n\nTo Add a project..."

FILTER_OFF = "Filter: OFF"
FILTER_ON = "Filter: ON"


# AUTO_SAVE_PATH_TXT = "\\auto_save_path.txt"
# AUTO_SAVE_PROJECT_TXT = "\\auto_save_project.txt"
AUTO_LOGIN = "\\auto_login.txt"


class Controller:
    def __init__(self):
        # initialize variables
        self.addProject = None
        self.mIsDoneUpdated = False
        self.mAddTask = None
        self.mUpdateTask = None
        self.mAddMember = None
        self.mTLColumnClicked = None
        self.mUpdateMembers = None
        self.mIsReverse = False
        self.mFilterTasks = None
        self.mPath = Path(os.getcwd())
        self.mUpdateMember = None
        # self.mRoot = tk.Tk()
        self.mModel = model.Model()
        self.mView = view.View()
        self.mIsNo = None
        self.mIsYes = None
        self.mDEInitialMin = None
        self.mDEInitialMax = None
        self.mDEDueMin = None
        self.mDEDueMax = None
        self.mScaleSeverityMin = None
        self.mScaleSeverityMax = None
        self.mIsBugOn = None
        self.mIsBonusOff = None
        self.mIsBacklog = None
        self.mIsTodo = None
        self.mIsTesting = None
        self.mIsDoneOn = None
        self.mIsDoneOff = None
        self.mIsBugOff = None
        self.mIsBonusOff = None
        self.mIsBonusOn = None
        self.mUpdateMembers = None
        self.mDeleteMode = False
        self.mEditDeletePopup = None
        self.mRegister = None
        connect()
        self.setupLogin()

        # self.mRoot.protocol('WM_DELETE_WINDOW', self.quit_and_save)  # override close button

    def setupLogin(self):
        self.mView.mLogin.mBtnLogin.config(command=self.login)
        self.mView.mLogin.mBtnRegister.config(command=self.register)

    def setupTaskListFunctions(self):
        # menu bar command
        self.mView.mMenuFile.entryconfigure(0, command=self.createAddProject)
        self.mView.mMenuFile.entryconfigure(3, command=self.viewProjects)
        # self.mView.mMenuFile.entryconfigure(4, command=self.saveProject)
        # self.mView.mMenuFile.entryconfigure(5, command=self.saveAsProject)
        self.mView.mMenuFile.entryconfigure(1, command=self.addTask)
        self.mView.mMenuFile.entryconfigure(2, command=self.updateMembers)
        self.mView.mMenuFile.entryconfigure(5, command=self.logout)
        self.mView.mMenuFile.entryconfigure(6, command=self.exit)
        self.mView.mMenuHelp.entryconfigure(0, command=helpTutorial)
        self.mView.mMenuHelp.entryconfigure(1, command=about)
        self.mView.mMenuEdit.entryconfigure(0, command=self.openFilter)
        self.mView.mMenuEdit.entryconfigure(1, command=self.taskListUpdate)

        # Task list
        self.mView.mTaskList.mBtnAddTask.config(command=self.addTask)
        # self.mView.mTaskList.mBtnDeleteTask.config(command=self.deleteTaskMode)
        self.mView.mTaskList.mBtnUpdateMember.config(command=self.updateMembers)
        self.mView.mTaskList.mBtnFilter.config(command=self.openFilter)
        self.mView.mTaskList.mBtnResetFilter.config(command=self.taskListUpdate)
        self.mView.mTaskList.mTvTaskList.bind("<Double-1>", self.taskClicked)  # taskDoubleClicked
        self.mView.mTaskList.mTvTaskList.bind("<Button-1>", self.taskClicked)

    def viewProjects(self):
        print("view projects")
        self.setupProjectList()

    def login(self):
        if not(self.mView.mLogin.mVarUsername.get() == "" and self.mView.mLogin.mVarPassword.get() == ""):
            print("login")
            user = selectUserFromNameAndPW(self.mView.mLogin.mVarUsername.get(),
                                           self.mView.mLogin.mVarPassword.get())
            if len(user) == 0:
                messagebox.showwarning(title="Warning", message="Username and Password is not found")
            else:
                self.mModel.mPassword = self.mView.mLogin.mVarPassword.get()
                self.mModel.mUserID = user[0][0]
                self.mModel.mPassword = user[0][2]
                self.mModel.mUsername = user[0][1]
                self.setupProjectList()
                self.mModel.save(str(self.mPath.parent) + AUTO_LOGIN)
        else:
            print("no saved login")

    def setupProjectList(self):
        self.getUserProjectList()
        self.mView.createProjectList(self.mModel.mProjectList)
        self.mView.mProjectList.mBtnAddTask.config(command=self.createAddProject)
        self.mView.mProjectList.mTvProjectList.bind("<Double-1>", self.projectClicked)  # taskDoubleClicked
        self.mView.mProjectList.mTvProjectList.bind("<Button-1>", self.projectClicked)
        self.mView.mMenuFile.entryconfigure(0, command=self.createAddProject)
        self.mView.mMenuFile.entryconfigure(2, command=self.logout)
        self.mView.mMenuFile.entryconfigure(3, command=self.exit)
        self.mView.mMenuHelp.entryconfigure(0, command=helpProject)
        self.mView.mMenuHelp.entryconfigure(1, command=about)
        self.projectListUpdate()
    def getUserProjectList(self):
        temp = selectProjectFromUserID(self.mModel.mUserID)
        print(temp)
        self.mModel.mProjectList = []
        for x in temp:
            self.mModel.mProjectList.append(x[0])
        # if self.mModel.mProjectList is None:
        #     self.mModel.mProjectList = []

    def projectClicked(self, instance):
        print("project clicked")
        region = self.mView.mProjectList.mTvProjectList.identify("region", instance.x, instance.y)
        item = self.mView.mProjectList.mTvProjectList.identify("item", instance.x, instance.y)
        if region == "heading":
            print("sort project name")
            # self.sort(instance)
        elif item:
            if len(self.mView.mProjectList.mTvProjectList.selection()) > 0:
                item = self.mView.mProjectList.mTvProjectList.selection()[0]
                # get task
                name = None
                for t in self.mModel.mProjectList:
                    # print(t)
                    # print(self.mView.mProjectList.mTvProjectList.item(item, "values")[0])
                    if t == self.mView.mProjectList.mTvProjectList.item(item, "values")[0]:
                        name = t
                        break
                # print(self.mModel.mProjectList)
                if name is not None:
                    if hasattr(self.mEditDeletePopup, "mTk") and hasattr(self.mEditDeletePopup.mTk, "destroy"):
                        self.destroyEditDeletePopup()
                    temp_root = tk.Toplevel(self.mView.mTk)
                    self.mEditDeletePopup = EditDeletePopup(temp_root, self.mView.mProjectList.mTk)
                    self.mEditDeletePopup.mBtnUpdate.config(command=lambda: self.createAndDestroyUpdateProject(name))
                    self.mEditDeletePopup.mBtnDelete.config(command=lambda: self.deleteProject(name))

    def createAndDestroyUpdateProject(self, name):
        self.destroyEditDeletePopup()
        # self.mView.updateTaskList()
        self.mView.createTaskList(name)
        self.setupTaskListFunctions()
        self.mModel.mProjectName = name

        # print(name, self.mModel.mUserID)
        self.mModel.mTaskList = []
        for x in selectTasks(name, self.mModel.mUserID):
            assignees = selectTasksAssignees(name, self.mModel.mUserID)
            print(assignees)
            # TODO assignees
            is_bug = x[4] == 1
            is_bonus = x[5] == 1
            is_done = x[10] == 1
            in_progress = x[9] == 1
            print(x[9], x[9] == 1, in_progress)
            self.mModel.mTaskList.append(Task(x[1], x[2], x[3], assignees, x[8], in_progress, str(x[6]).split()[0],
                                              str(x[7]).split()[0], is_bug, is_bonus, is_done))

        self.taskListUpdate()

    def deleteProject(self, name):
        print("delete" + str(name))
        deleteProject(name)
        # self.mModel.mProjectList.remove(name)
        self.getUserProjectList()
        self.projectListUpdate()
        self.destroyEditDeletePopup()

    def projectListUpdate(self):
        # delete all tasks in view
        self.mView.mProjectList.mTvProjectList.delete(*self.mView.mProjectList.mTvProjectList.get_children())

        # add all task in view
        for t in self.mModel.mProjectList:
            self.mView.mProjectList.mTvProjectList.insert("", "end", values=t)

    def logout(self):
        self.mView.mTk.destroy()
        self.mView = view.View()
        self.setupLogin()
        self.mModel.mUsername = ""
        self.mModel.mPassword = ""
        self.mModel.save(str(self.mPath.parent) + AUTO_LOGIN)

    def exit(self):
        self.mView.mTk.destroy()

    def createAddProject(self):
        print("new project")
        temp_root = tk.Toplevel(self.mView.mTk)
        pauseTaskList(temp_root)
        self.addProject = AddProject(temp_root)
        self.addProject.mBtnSubmit.config(command=self.createProject)
        self.addProject.mBtnCancel.config(command=self.cancelAddProject)

    def createProject(self):
        print("start project")
        # self.addProject.mTk.destroy()
        if self.addProject.mVarName.get() in self.mModel.mProjectList:
            messagebox.showwarning(title="Warning", message="Project name should be unique!")
        else:
            insertProject(self.mModel.mUsername, self.addProject.mVarName.get())
            self.mModel.mProjectName = self.addProject.mVarName.get()
            self.mView.createTaskList(self.addProject.mVarName.get())
            self.setupTaskListFunctions()

            insertMember(self.mModel.mUserID, self.mModel.mUsername, self.mModel.mProjectName)


    def cancelAddProject(self):
        print("cancel adding project")
        self.addProject.mTk.destroy()

    def register(self):
        print("register")
        temp_root = tk.Toplevel(self.mView.mTk)
        pauseTaskList(temp_root)
        self.mRegister = Register(temp_root)
        self.mRegister.mBtnRegister.config(command=self.registerUser)

    def registerUser(self):
        print("register user")
        if "" == self.mRegister.mVarUsername.get():
            messagebox.showwarning(title="Warning", message="Username cannot be blank")
        elif "" == self.mRegister.mVarPassword.get():
            messagebox.showwarning(title="Warning", message="Password cannot be blank")
        elif " " in self.mRegister.mVarUsername.get():
            messagebox.showwarning(title="Warning", message="Username should not have space!")
        elif len(selectUser(self.mRegister.mVarUsername.get())) != 0:
            messagebox.showwarning(title="Warning", message="Username is not unique")
        elif " " in self.mRegister.mVarPassword.get():
            messagebox.showwarning(title="Warning", message="Password should not have space!")
        elif len(self.mRegister.mVarPassword.get()) < 8:
            messagebox.showwarning(title="Warning", message="Password should have 8 characters!")
        elif self.mRegister.mVarPassword.get() != self.mRegister.mVarRePassword.get():
            messagebox.showwarning(title="Warning", message="Password and RePassword is not the same!")
        else:
            insertUser(self.mRegister.mVarUsername.get(), self.mRegister.mVarPassword.get())
        self.mRegister.mTk.destroy()

    def run(self):
        if path.exists(str(self.mPath.parent) + AUTO_LOGIN):
            try:
                self.mModel.load(str(self.mPath.parent) + AUTO_LOGIN)
                self.mView.mLogin.mVarUsername.set(self.mModel.mUsername)
                self.mView.mLogin.mVarPassword.set(self.mModel.mPassword)
                self.login()
            except _pickle.UnpicklingError:
                messagebox.showerror("Error", "There was an error on the auto_login.txt file loaded!")
        self.mView.mTk.mainloop()
        # self.mRoot.title("Login")
        # self.mRoot.deiconify()
        # if path.exists(str(self.mPath.parent) + AUTO_SAVE_PROJECT_TXT):
        #     try:
        #         self.mModel.load(str(self.mPath.parent) + AUTO_SAVE_PROJECT_TXT)
        #         self.taskListUpdate()
        #     except _pickle.UnpicklingError:
        #         messagebox.showerror("Error", "There was an error on the auto_save_project.txt file loaded!")
        # if path.exists(str(self.mPath.parent) + AUTO_SAVE_PATH_TXT):
        #     try:
        #         self.mModel.load_path(str(self.mPath.parent) + AUTO_SAVE_PATH_TXT)
        #         self.mRoot.title("Project Planner (" + self.mModel.mProjectName + ")")
        #     except _pickle.UnpicklingError:
        #         messagebox.showerror("Error", "There was an error on the auto_save_path.txt file loaded!")
        # center(self.mRoot)
        # self.mRoot.mainloop()

    def deleteTaskMode(self):
        self.mDeleteMode = not self.mDeleteMode
        if self.mDeleteMode:
            self.mView.mTaskList.mLblDelete.config(text=DELETE_ON)
        else:
            self.mView.mTaskList.mLblDelete.config(text=DELETE_OFF)

    def openFilter(self):
        temp_root = tk.Toplevel(self.mView.mTk)
        pauseTaskList(temp_root)
        self.mFilterTasks = FilterTasks(temp_root)
        self.mFilterTasks.mBtnSubmit.config(command=self.filterClicked)
        self.mFilterTasks.mBtnCancel.config(command=self.destroyFilter)

    def destroyFilter(self):
        self.mFilterTasks.mTk.destroy()

    def filterClicked(self):
        self.mIsNo = self.mFilterTasks.mIsNo
        self.mIsYes = self.mFilterTasks.mIsYes
        self.mDEInitialMin = self.mFilterTasks.mDEInitialMin.get_date()
        self.mDEInitialMax = self.mFilterTasks.mDEInitialMax.get_date()
        self.mDEDueMin = self.mFilterTasks.mDEDueMin.get_date()
        self.mDEDueMax = self.mFilterTasks.mDEDueMax.get_date()
        self.mScaleSeverityMin = self.mFilterTasks.mScaleSeverityMin.get()
        self.mScaleSeverityMax = self.mFilterTasks.mScaleSeverityMax.get()
        self.mIsBugOn = self.mFilterTasks.mIsBugOn
        self.mIsBonusOn = self.mFilterTasks.mIsBonusOn
        self.mIsBacklog = self.mFilterTasks.mIsBacklog
        self.mIsTodo = self.mFilterTasks.mIsTodo
        self.mIsTesting = self.mFilterTasks.mIsTesting
        self.mIsDoneOn = self.mFilterTasks.mIsDoneOn
        self.mIsDoneOff = self.mFilterTasks.mIsDoneOff
        self.mIsBugOff = self.mFilterTasks.mIsBugOff
        self.mIsBonusOff = self.mFilterTasks.mIsBonusOff
        self.filter()
        self.mFilterTasks.mTk.destroy()

    def filter(self):
        # delete all tasks in view
        self.mView.mTaskList.mTvTaskList.delete(*self.mView.mTaskList.mTvTaskList.get_children())

        # add all task in view
        for t in self.mModel.mTaskList:
            if ((self.mIsNo == t.mIsNo or self.mIsYes == t.mIsYes) and
                    (self.mDEInitialMin <= t.mInitialDate <= self.mDEInitialMax) and
                    (self.mDEDueMin <= t.mDueDate <= self.mDEDueMax) and
                    (self.mScaleSeverityMin <= t.mSeverity <= self.mScaleSeverityMax) and
                    ((self.mIsBugOn == t.mIsBugOn or self.mIsBugOff == t.mIsBugOff) and
                     (self.mIsBonusOn == t.mIsBonusOn or self.mIsBonusOff == t.mIsBonusOff)) and
                    ((self.mIsBacklog == t.mIsBacklog) or (self.mIsTodo == t.mIsTodo) or
                     (self.mIsTesting == t.mIsTesting)) and
                    (self.mIsDoneOn == t.mIsDoneOn or self.mIsDoneOff == t.mIsDoneOff)):
                self.mView.mTaskList.mTvTaskList.insert("", "end",
                                                        values=(t.mTitle, t.mMode, t.mSeverity, t.mIsYes,
                                                                t.mInitialDate, t.mDueDate, t.mIsBugOn, t.mIsBonusOn,
                                                                t.mIsDone))
        self.mView.mTaskList.mLblFilter.config(text=FILTER_ON)

    # def run(self):
    #     self.mRoot.title("Project Planner")
    #     self.mRoot.deiconify()
    #     if path.exists(str(self.mPath.parent) + AUTO_SAVE_PROJECT_TXT):
    #         try:
    #             self.mModel.load(str(self.mPath.parent) + AUTO_SAVE_PROJECT_TXT)
    #             self.taskListUpdate()
    #         except _pickle.UnpicklingError:
    #             messagebox.showerror("Error", "There was an error on the auto_save_project.txt file loaded!")
    #     if path.exists(str(self.mPath.parent) + AUTO_SAVE_PATH_TXT):
    #         try:
    #             self.mModel.load_path(str(self.mPath.parent) + AUTO_SAVE_PATH_TXT)
    #             self.mRoot.title("Project Planner (" + self.mModel.mProjectName + ")")
    #         except _pickle.UnpicklingError:
    #             messagebox.showerror("Error", "There was an error on the auto_save_path.txt file loaded!")
    #     self.mRoot.mainloop()

    # def quit_and_save(self):
    #     self.mModel.save(str(self.mPath.parent) + AUTO_SAVE_PROJECT_TXT)
    #     if messagebox.askyesno(""
    #                            "", "If you exit the application, any changes you have made will be lost. "
    #                                "Are you sure you wish to leave?"):
    #         self.mRoot.destroy()
    #
    # def newProject(self):
    #     # if messagebox.askyesno("Save before Exit", "Do you want to save the current project first?"):
    #     #     self.mModel.save_as_task_list()
    #     # else:
    #     self.createAddProject()
    #     self.mModel.mTaskList = []
    #     self.mModel.mProjectName = ""
    #     self.taskListUpdate()
    #     # os.remove(str(self.mPath.parent) + AUTO_SAVE_PATH_TXT)
    #     # self.mModel.mSavedPath = None
    #     self.mRoot.title("Project Planner")

    # def loadProject(self):
    #     if messagebox.askyesno("Save before Exit", "Do you want to save the current project first?"):
    #         self.mModel.save_as_task_list()
    #     else:
    #         try:
    #             if self.mModel.load_task_list():
    #                 self.taskListUpdate()
    #                 self.mRoot.title("Project Planner (" + self.mModel.mProjectName + ")")
    #         except _pickle.UnpicklingError:
    #             messagebox.showerror("Error", "There was an error on the file loaded!")

    # def saveProject(self):
    #     if hasattr(self.mModel, 'mSavedPath') and self.mModel.mSavedPath is None:
    #         self.saveAsProject()
    #     else:
    #         self.mModel.save_as_task_list()
    #
    # def saveAsProject(self):
    #     self.mModel.save_as_task_list()
    #     self.mRoot.title("Project Planner (" + self.mModel.mProjectName + ")")

    def addTask(self):
        temp_root = tk.Toplevel(self.mView.mTk)
        pauseTaskList(temp_root)
        self.mAddTask = AddTask(temp_root, self.mModel.mMemberList, self.mModel.getNames())
        self.mAddTask.mBtnSubmit.config(command=self.submitTask)
        self.mAddTask.mBtnCancel.config(command=self.destroyAddTask)

    def destroyAddTask(self):
        self.mAddTask.mTk.destroy()

    def taskListUpdate(self):
        # delete all tasks in view
        self.mView.mTaskList.mTvTaskList.delete(*self.mView.mTaskList.mTvTaskList.get_children())

        # add all task in view
        for t in self.mModel.mTaskList:
            self.mView.mTaskList.mTvTaskList.insert("", "end",
                                                    values=(t.mTitle, t.mMode, t.mSeverity, t.mIsYes,
                                                            t.mInitialDate, t.mDueDate, t.mIsBugOn, t.mIsBonusOn,
                                                            t.mIsDone))
        self.mView.mTaskList.mLblFilter.config(text=FILTER_OFF)

    def submitTask(self):
        if self.mAddTask.mVarTitle.get().strip() == "":  # empty title constraint
            messagebox.showwarning(title="Warning", message="No empty titles allowed!")
        elif self.isDuplicateTitle(True):  # unique constraint
            messagebox.showwarning(title="Warning", message="No duplicate titles allowed!")
        else:

            assignees = []
            for x in self.mAddTask.mLBAssignees.curselection():
                assignees.append(self.mAddTask.mLBAssignees.get(x))

            # add task
            t = task.Task(self.mAddTask.mVarTitle.get(), self.mAddTask.mTextDescription.get("1.0", "end"),
                          self.mAddTask.mVarMode.get(), assignees, self.mAddTask.mScaleSeverity.get(),
                          self.mAddTask.mVarInProgress.get(),
                          self.mAddTask.mDEInitial.get_date(), self.mAddTask.mDEDue.get_date(),
                          self.mAddTask.mIsBug, self.mAddTask.mIsBonus, False)
            self.mModel.mTaskList.append(t)
            t.insertTaskToProjectID(self.mModel.mProjectName, self.mModel.mUserID)
            self.taskListUpdate()  # update task list view
            self.destroyAddTask()

    def isDuplicateTitle(self, is_add):
        if is_add:  # for add task
            title = self.mAddTask.mVarTitle.get()
        else:  # for update task
            title = self.mUpdateTask.mVarTitle.get()
        for t in self.mModel.mTaskList:
            if t.mTitle == title:
                return True
        return False

    def closeOpenTask(self):
        self.mIsDoneUpdated = True
        self.editTaskView()

    def editTaskView(self):
        if self.mUpdateTask.mVarTitle.get().strip() == "":  # empty title constraint
            messagebox.showwarning(title="Warning", message="No empty titles allowed!")
        elif self.isDuplicateTitle(False) and self.mUpdateTask.mVarTitle.get() \
                != self.mUpdateTask.mOldTitle:  # unique constraint for edit
            messagebox.showwarning(title="Warning", message="No duplicate titles allowed!")
        else:
            old_t = self.deleteTaskOnUpdate()  # delete old task
            old_t.deleteTaskToProjectID(self.mModel.mProjectName, self.mModel.mUserID)

            if self.mIsDoneUpdated:
                temp_done = not old_t.mIsDone
            else:
                temp_done = old_t.mIsDone

            assignees = []
            for x in self.mUpdateTask.mLBAssignees.curselection():
                assignees.append(self.mUpdateTask.mLBAssignees.get(x))

            # add task
            t = task.Task(self.mUpdateTask.mVarTitle.get(), self.mUpdateTask.mTextDescription.get("1.0", "end"),
                          self.mUpdateTask.mVarMode.get(), self.mUpdateTask.mVarAssignees.get(),
                          self.mUpdateTask.mScaleSeverity.get(), self.mUpdateTask.mVarInProgress.get(),
                          self.mUpdateTask.mDEInitial.get_date(), self.mUpdateTask.mDEDue.get_date(),
                          self.mUpdateTask.mIsBug, self.mUpdateTask.mIsBonus, temp_done)
            t.insertTaskToProjectID(self.mModel.mProjectName, self.mModel.mUserID)
            self.mModel.mTaskList.append(t)

            self.taskListUpdate()  # update task list view
            self.destroyUpdateTask()
            self.mIsDoneUpdated = False

    def deleteTaskView(self):
        self.deleteTaskOnUpdate()
        self.destroyUpdateTask()

    def deleteTaskOnUpdate(self):
        # remove old task
        for t in self.mModel.mTaskList:
            if t.mTitle == self.mUpdateTask.mOldTitle:
                self.mModel.mTaskList.remove(t)
                return t

    def taskClicked(self, instance):
        region = self.mView.mTaskList.mTvTaskList.identify("region", instance.x, instance.y)
        item = self.mView.mTaskList.mTvTaskList.identify("item", instance.x, instance.y)
        if region == "heading":
            self.sort(instance)
        # elif self.mView.mTaskList.mLblDelete['text'] == DELETE_ON:
        #     if len(self.mView.mTaskList.mTvTaskList.selection()) > 0:
        #         item = self.mView.mTaskList.mTvTaskList.selection()[0]
        #         # get task
        #         tsk = None
        #         for t in self.mModel.mTaskList:
        #             if t.mTitle == self.mView.mTaskList.mTvTaskList.item(item, "values")[0]:
        #                 tsk = t
        #                 break
        #         self.deleteTask(tsk)
        elif item:
            if len(self.mView.mTaskList.mTvTaskList.selection()) > 0:
                item = self.mView.mTaskList.mTvTaskList.selection()[0]
                # get task
                tsk = None
                for t in self.mModel.mTaskList:
                    if t.mTitle == self.mView.mTaskList.mTvTaskList.item(item, "values")[0]:
                        tsk = t
                        break
                if tsk is not None:
                    if hasattr(self.mEditDeletePopup, "mTk"):
                        if hasattr(self.mEditDeletePopup.mTk, "destroy"):
                            self.destroyEditDeletePopup()
                    temp_root = tk.Toplevel(self.mView.mTk)
                    self.mEditDeletePopup = EditDeletePopup(temp_root, self.mView.mTaskList.mTk)
                    self.mEditDeletePopup.mBtnUpdate.config(command=lambda: self.createAndDestroyUpdateTask(tsk))
                    self.mEditDeletePopup.mBtnDelete.config(command=lambda: self.deleteTask(tsk))

    def deleteTask(self, tsk):
        self.mModel.mTaskList.remove(tsk)
        self.taskListUpdate()

    def destroyEditDeletePopup(self):
        self.mEditDeletePopup.mTk.destroy()
        self.mEditDeletePopup = None

    def createAndDestroyUpdateTask(self, tsk):
        self.destroyEditDeletePopup()
        new_root = tk.Toplevel(self.mView.mTk)
        self.createUpdateTask(new_root, tsk)

    def sort(self, instance):
        if self.mView.mTaskList.mTvTaskList.identify_column(instance.x) == "#1":
            if hasattr(self, 'mTLColumnClicked') and self.mTLColumnClicked == "#1" and self.mIsReverse:
                self.mModel.sort_by_title(False)
                self.mIsReverse = False
            else:
                self.mModel.sort_by_title(True)
                self.mIsReverse = True
        elif self.mView.mTaskList.mTvTaskList.identify_column(instance.x) == "#2":
            if hasattr(self, 'mTLColumnClicked') and self.mTLColumnClicked == "#2" and self.mIsReverse:
                self.mModel.sort_by_mode(False)
                self.mIsReverse = False
            else:
                self.mModel.sort_by_mode(True)
                self.mIsReverse = True
        elif self.mView.mTaskList.mTvTaskList.identify_column(instance.x) == "#3":
            if hasattr(self, 'mTLColumnClicked') and self.mTLColumnClicked == "#3" and self.mIsReverse:
                self.mModel.sort_by_severity(False)
                self.mIsReverse = False
            else:
                self.mModel.sort_by_severity(True)
                self.mIsReverse = True
        elif self.mView.mTaskList.mTvTaskList.identify_column(instance.x) == "#4":
            if hasattr(self, 'mTLColumnClicked') and self.mTLColumnClicked == "#4" and self.mIsReverse:
                self.mModel.sort_by_in_progress(False)
                self.mIsReverse = False
            else:
                self.mModel.sort_by_in_progress(True)
                self.mIsReverse = True
        elif self.mView.mTaskList.mTvTaskList.identify_column(instance.x) == "#5":
            if hasattr(self, 'mTLColumnClicked') and self.mTLColumnClicked == "#5" and self.mIsReverse:
                self.mModel.sort_by_initial_date(False)
                self.mIsReverse = False
            else:
                self.mModel.sort_by_initial_date(True)
                self.mIsReverse = True
        elif self.mView.mTaskList.mTvTaskList.identify_column(instance.x) == "#6":
            if hasattr(self, 'mTLColumnClicked') and self.mTLColumnClicked == "#6" and self.mIsReverse:
                self.mModel.sort_by_due_date(False)
                self.mIsReverse = False
            else:
                self.mModel.sort_by_due_date(True)
                self.mIsReverse = True
        if self.mView.mTaskList.mLblFilter['text'] == FILTER_ON:
            self.filter()
        else:
            self.taskListUpdate()
        self.mTLColumnClicked = self.mView.mTaskList.mTvTaskList.identify_column(instance.x)

    # def taskDoubleClicked(self, instance):
    #     self.taskClicked(instance)
    #     # region = self.mView.mTaskList.mTvTaskList.identify("region", instance.x, instance.y)
    #     # if region == "heading":
    #     #     self.sort(instance)
    #     # else:
    #     #     if len(self.mView.mTaskList.mTvTaskList.selection()) > 0:
    #     #         temp_root = tk.Tk()
    #     #         item = self.mView.mTaskList.mTvTaskList.selection()[0]
    #     #         # get task
    #     #         tsk = None
    #     #         for t in self.mModel.mTaskList:
    #     #             if t.mTitle == self.mView.mTaskList.mTvTaskList.item(item, "values")[0]:
    #     #                 tsk = t
    #     #                 break
    #     #         self.createUpdateTask(temp_root, tsk)

    def createUpdateTask(self, temp_root, tsk):
        pauseTaskList(temp_root)
        self.mUpdateTask = UpdateTask(temp_root, self.mModel.mMemberList, self.mModel.getNames(), tsk)
        self.mUpdateTask.mBtnSubmit.config(command=self.editTaskView)
        self.mUpdateTask.mCloseOpenBtn.config(command=self.closeOpenTask)
        self.mUpdateTask.mBtnDelete.config(command=self.deleteTaskView)
        self.mUpdateTask.mBtnCancel.config(command=self.destroyUpdateTask)

    def destroyUpdateTask(self):
        self.mUpdateTask.mTk.destroy()

    def updateMembers(self):
        temp_root = tk.Toplevel(self.mView.mTk)
        pauseTaskList(temp_root)
        # if len(self.mModel.mMemberList) == 0:
        #     self.mModel.mMemberList.append(Member(self.mModel.mUsername))
        self.mUpdateMembers = updateMembers.UpdateMembers(temp_root)
        self.mUpdateMembers.mBtnAddMember.config(command=self.addMembersClicked)
        self.mModel.mMemberList = []
        # print(selectMembers(self.mModel.mProjectName, self.mModel.mUserID))
        for x in selectMembers(self.mModel.mProjectName, self.mModel.mUserID):
            self.mModel.mMemberList.append(Member(x[0]))
        self.mUpdateMembers.mTvMemberList.bind("<Double-1>", self.memberClicked)  # taskDoubleClicked
        self.mUpdateMembers.mTvMemberList.bind("<Button-1>", self.memberClicked)
        self.memberListUpdate()

    def memberClicked(self, instance):
        # region = self.mUpdateMembers.mTvMemberList.identify("region", instance.x, instance.y)
        item = self.mUpdateMembers.mTvMemberList.identify("item", instance.x, instance.y)
        # if region == "heading":
        #     self.sort(instance)
        # elif item:
        if item:
            if len(self.mUpdateMembers.mTvMemberList.selection()) > 0:
                item = self.mUpdateMembers.mTvMemberList.selection()[0]
                # get task
                m = None
                for t in self.mModel.mMemberList:
                    if t.mName == self.mUpdateMembers.mTvMemberList.item(item, "values")[0]:
                        m = t
                        break
                if m is not None:
                    if hasattr(self.mEditDeletePopup, "mTk") and hasattr(self.mEditDeletePopup.mTk, "destroy"):
                        self.destroyEditDeletePopup()
                    temp_root = tk.Toplevel(self.mUpdateMembers.mTk)
                    self.mEditDeletePopup = editDeletePopup.EditDeletePopup(temp_root, self.mUpdateMembers.mTk)
                    # self.mEditDeletePopup.mBtnUpdate.config(command=lambda: self.createAndDestroyUpdateMember(m))
                    self.mEditDeletePopup.mBtnUpdate.destroy()
                    self.mEditDeletePopup.mBtnDelete.config(command=lambda: self.deleteMember(m))

    # def createAndDestroyUpdateMember(self, m):
    #     self.mEditDeletePopup.mTk.destroy()
    #     new_root = tk.Toplevel(self.mUpdateMembers.mTk)
    #     self.createUpdateMember(new_root, m)

    # def createUpdateMember(self, root, m):
    #     pauseTaskList(root)
    #     self.mUpdateMember = UpdateMember(root, m)
    #     self.mUpdateMember.mBtnSubmit.config(command=self.editMember)
    #     self.mUpdateMember.mBtnDelete.config(command=lambda: self.deleteMember(m))
    #     self.mUpdateMember.mBtnCancel.config(command=self.destroyUpdateMember)
    #     self.mUpdateMember.mTk.protocol('WM_DELETE_WINDOW', self.destroyUpdateMember)

    # def destroyUpdateMember(self):
    #     self.mUpdateMember.mTk.destroy()
    #     pauseTaskList(self.mUpdateMembers.mTk)

    # def editMember(self):
    #     if self.mUpdateMember.mVarName.get().strip() == "":  # empty title constraint
    #         messagebox.showwarning(title="Warning", message="No empty name allowed!")
    #     elif self.isDuplicateName(False) and self.mUpdateMember.mVarName.get() \
    #             != self.mUpdateMember.mOldName:  # unique constraint
    #         messagebox.showwarning(title="Warning", message="No duplicate name allowed!")
    #     else:
    #         for m in self.mModel.mMemberList:
    #             if m.mName == self.mUpdateMember.mOldName:
    #                 self.mModel.mMemberList.remove(m)
    #                 break
    #
    #         # add task
    #         t = member.Member(self.mUpdateMember.mVarName.get())
    #         self.mModel.mMemberList.append(t)
    #
    #         self.memberListUpdate()  # update task list view
    #
    #         self.destroyUpdateMember()
    #
    #         pauseTaskList(self.mUpdateMembers.mTk)

    def deleteMember(self, m):
        deleteMember(m, self.mModel.mProjectName, self.mModel.mUserID)
        self.mModel.mMemberList.remove(m)
        self.memberListUpdate()
        self.destroyEditDeletePopup()
        if hasattr(self.mUpdateMember, "mTk") and hasattr(self.mUpdateMember.mTk, "destroy"):
            self.mUpdateMember.mTk.destroy()
        pauseTaskList(self.mUpdateMembers.mTk)

    def addMembersClicked(self):
        temp_root = tk.Toplevel(self.mUpdateMembers.mTk)
        pauseTaskList(temp_root)
        self.mAddMember = AddMember(temp_root)
        self.mAddMember.mTk.protocol('WM_DELETE_WINDOW', self.destroyAddMember)
        self.mAddMember.mBtnSubmit.config(command=self.submitMember)
        self.mAddMember.mBtnCancel.config(command=self.destroyAddMember)

    def destroyAddMember(self):
        self.mAddMember.mTk.destroy()
        pauseTaskList(self.mUpdateMembers.mTk)

    def submitMember(self):
        if self.mAddMember.mVarName.get().strip() == "":  # empty title constraint
            messagebox.showwarning(title="Warning", message="No empty name allowed!")
        elif self.isDuplicateName(True):  # unique constraint
            messagebox.showwarning(title="Warning", message="No duplicate name allowed!")
        # elif self.mModel.mUserID == selectUser(self.mAddMember.mVarName.get())[0][0]:
        #     messagebox.showwarning(title="Warning", message="Don't add yourself as a member!")
        else:
            # add member
            if len(selectUser(self.mAddMember.mVarName.get())) != 0:
                insertMember(self.mModel.mUserID, self.mAddMember.mVarName.get(), self.mModel.mProjectName)
                t = Member(self.mAddMember.mVarName.get())
                self.mModel.mMemberList.append(t)

                self.memberListUpdate()  # update task list view
                self.destroyAddMember()

    def memberListUpdate(self):
        # delete all members in view
        self.mUpdateMembers.mTvMemberList.delete(*self.mUpdateMembers.mTvMemberList.get_children())

        # add all member in view

        for t in self.mModel.mMemberList:
            self.mUpdateMembers.mTvMemberList.insert("", "end",
                                                     values=t.mName)

    def isDuplicateName(self, is_add):
        if is_add:  # for add
            name = self.mAddMember.mVarName.get()
        else:  # for update
            name = self.mUpdateMember.mVarName.get()
        for t in self.mModel.mMemberList:
            if t.mName == name:
                return True
        return False


def about():
    messagebox.showinfo(title="About", message=ABOUT_MSG)


def helpTutorial():
    messagebox.showinfo(title="Help", message=HELP_MSG)


def helpProject():
    messagebox.showinfo(title="Help", message=PROJECT_MSG)


def pauseTaskList(window):
    window.grab_set()
