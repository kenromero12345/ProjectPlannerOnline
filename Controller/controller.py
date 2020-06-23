import _pickle
import os
import tkinter as tk
from os import path
from pathlib import Path
from tkinter import messagebox
from Model import model, member
from Model import task
from Model.member import Member
# from View import addTask, updateMembers, editDeletePopup, addMember
# from View import filterTasks
from View import view
from View.register import Register
from View.updateMember import UpdateMember
from View.updateTask import UpdateTask
from View.view import center

DELETE_OFF = "Delete: OFF"

DELETE_ON = "Delete: ON"

ABOUT_MSG = "A python application for project planning for programmers to use to be efficient in their tasks with " \
            "their team or their own.\n\nCreated by Ken Gil Romero, a master student of University of Washington"

HELP_MSG = "A little tutorial to help users use the application.\n\nTo Add a task, click the add task button or the " \
           "File menu then New...\n\tA new window will appear where the user will input information for a task "

FILTER_OFF = "Filter: OFF"
FILTER_ON = "Filter: ON"
AUTO_SAVE_PATH_TXT = "\\auto_save_path.txt"
AUTO_SAVE_PROJECT_TXT = "\\auto_save_project.txt"


class Controller:
    def __init__(self):
        # initialize variables
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
        self.mEditDeletePopup = False
        self.mRegister = None

        # # menu bar command
        # self.mView.mMenuFile.entryconfigure(0, command=self.newProject)
        # self.mView.mMenuFile.entryconfigure(3, command=self.loadProject)
        # self.mView.mMenuFile.entryconfigure(4, command=self.saveProject)
        # self.mView.mMenuFile.entryconfigure(5, command=self.saveAsProject)
        # self.mView.mMenuFile.entryconfigure(1, command=self.addTask)
        # self.mView.mMenuFile.entryconfigure(2, command=self.updateMembers)
        # self.mView.mMenuFile.entryconfigure(7, command=self.quit_and_save)
        # self.mView.mMenuHelp.entryconfigure(0, command=helpTutorial)
        # self.mView.mMenuHelp.entryconfigure(1, command=about)
        # self.mView.mMenuEdit.entryconfigure(0, command=self.openFilter)
        # self.mView.mMenuEdit.entryconfigure(1, command=self.taskListUpdate)

        # # Task list
        # self.mView.mTaskList.mBtnAddTask.config(command=self.addTask)
        # # self.mView.mTaskList.mBtnDeleteTask.config(command=self.deleteTaskMode)
        # self.mView.mTaskList.mBtnUpdateMember.config(command=self.updateMembers)
        # self.mView.mTaskList.mBtnFilter.config(command=self.openFilter)
        # self.mView.mTaskList.mBtnResetFilter.config(command=self.taskListUpdate)
        # self.mView.mTaskList.mTvTaskList.bind("<Double-1>", self.taskClicked)  # taskDoubleClicked
        # self.mView.mTaskList.mTvTaskList.bind("<Button-1>", self.taskClicked)
        self.mView.mLogin.mBtnLogin.config(command=self.login)
        self.mView.mLogin.mBtnRegister.config(command=self.register)

        # self.mRoot.protocol('WM_DELETE_WINDOW', self.quit_and_save)  # override close button

    def login(self):
        print("login")

    def register(self):
        print("register")
        temp_root = tk.Toplevel(self.mView.mTk)
        pauseTaskList(temp_root)
        self.mRegister = Register(temp_root)
        self.mRegister.mBtnRegister.config(command=self.register)

    def run(self):
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


#     def deleteTaskMode(self):
#         self.mDeleteMode = not self.mDeleteMode
#         if self.mDeleteMode:
#             self.mView.mTaskList.mLblDelete.config(text=DELETE_ON)
#         else:
#             self.mView.mTaskList.mLblDelete.config(text=DELETE_OFF)
#
#     def openFilter(self):
#         temp_root = tk.Toplevel(self.mView.mTk)
#         pauseTaskList(temp_root)
#         self.mFilterTasks = filterTasks.FilterTasks(temp_root)
#         self.mFilterTasks.mBtnSubmit.config(command=self.filterClicked)
#         self.mFilterTasks.mBtnCancel.config(command=self.destroyFilter)
#
#     def destroyFilter(self):
#         self.mFilterTasks.mTk.destroy()
#
#     def filterClicked(self):
#         self.mIsNo = self.mFilterTasks.mIsNo
#         self.mIsYes = self.mFilterTasks.mIsYes
#         self.mDEInitialMin = self.mFilterTasks.mDEInitialMin.get_date()
#         self.mDEInitialMax = self.mFilterTasks.mDEInitialMax.get_date()
#         self.mDEDueMin = self.mFilterTasks.mDEDueMin.get_date()
#         self.mDEDueMax = self.mFilterTasks.mDEDueMax.get_date()
#         self.mScaleSeverityMin = self.mFilterTasks.mScaleSeverityMin.get()
#         self.mScaleSeverityMax = self.mFilterTasks.mScaleSeverityMax.get()
#         self.mIsBugOn = self.mFilterTasks.mIsBugOn
#         self.mIsBonusOn = self.mFilterTasks.mIsBonusOn
#         self.mIsBacklog = self.mFilterTasks.mIsBacklog
#         self.mIsTodo = self.mFilterTasks.mIsTodo
#         self.mIsTesting = self.mFilterTasks.mIsTesting
#         self.mIsDoneOn = self.mFilterTasks.mIsDoneOn
#         self.mIsDoneOff = self.mFilterTasks.mIsDoneOff
#         self.mIsBugOff = self.mFilterTasks.mIsBugOff
#         self.mIsBonusOff = self.mFilterTasks.mIsBonusOff
#         self.filter()
#         self.mFilterTasks.mTk.destroy()
#
#     def filter(self):
#         # delete all tasks in view
#         self.mView.mTaskList.mTvTaskList.delete(*self.mView.mTaskList.mTvTaskList.get_children())
#
#         # add all task in view
#         for t in self.mModel.mTaskList:
#             if ((self.mIsNo == t.mIsNo or self.mIsYes == t.mIsYes) and
#                     (self.mDEInitialMin <= t.mInitialDate <= self.mDEInitialMax) and
#                     (self.mDEDueMin <= t.mDueDate <= self.mDEDueMax) and
#                     (self.mScaleSeverityMin <= t.mSeverity <= self.mScaleSeverityMax) and
#                     ((self.mIsBugOn == t.mIsBugOn or self.mIsBugOff == t.mIsBugOff) and
#                      (self.mIsBonusOn == t.mIsBonusOn or self.mIsBonusOff == t.mIsBonusOff)) and
#                     ((self.mIsBacklog == t.mIsBacklog) or (self.mIsTodo == t.mIsTodo) or
#                      (self.mIsTesting == t.mIsTesting)) and
#                     (self.mIsDoneOn == t.mIsDoneOn or self.mIsDoneOff == t.mIsDoneOff)):
#                 self.mView.mTaskList.mTvTaskList.insert("", "end",
#                                                         values=(t.mTitle, t.mMode, t.mSeverity, t.mInProgress,
#                                                                 t.mInitialDate, t.mDueDate, t.mIsBugOn, t.mIsBonusOn,
#                                                                 t.mIsDone))
#         self.mView.mTaskList.mLblFilter.config(text=FILTER_ON)
#
#     def run(self):
#         self.mRoot.title("Project Planner")
#         self.mRoot.deiconify()
#         if path.exists(str(self.mPath.parent) + AUTO_SAVE_PROJECT_TXT):
#             try:
#                 self.mModel.load(str(self.mPath.parent) + AUTO_SAVE_PROJECT_TXT)
#                 self.taskListUpdate()
#             except _pickle.UnpicklingError:
#                 messagebox.showerror("Error", "There was an error on the auto_save_project.txt file loaded!")
#         if path.exists(str(self.mPath.parent) + AUTO_SAVE_PATH_TXT):
#             try:
#                 self.mModel.load_path(str(self.mPath.parent) + AUTO_SAVE_PATH_TXT)
#                 self.mRoot.title("Project Planner (" + self.mModel.mProjectName + ")")
#             except _pickle.UnpicklingError:
#                 messagebox.showerror("Error", "There was an error on the auto_save_path.txt file loaded!")
#         self.mRoot.mainloop()
#
#     def quit_and_save(self):
#         # TODO could be better, maybe ask to save when exiting
#         self.mModel.save(str(self.mPath.parent) + AUTO_SAVE_PROJECT_TXT)
#         if messagebox.askyesno("Exit", "If you exit the application, any changes you have made will be lost. "
#                                        "Are you sure you wish to leave?"):
#             self.mRoot.destroy()
#
#     def newProject(self):
#         if messagebox.askyesno("Save before Exit", "Do you want to save the current project first?"):
#             self.mModel.save_as_task_list()
#         else:
#             self.mModel.mTaskList = []
#             self.mModel.mProjectName = ""
#             self.taskListUpdate()
#             os.remove(str(self.mPath.parent) + AUTO_SAVE_PATH_TXT)
#             self.mModel.mSavedPath = None
#             self.mRoot.title("Project Planner")
#
#     def loadProject(self):
#         if messagebox.askyesno("Save before Exit", "Do you want to save the current project first?"):
#             self.mModel.save_as_task_list()
#         else:
#             try:
#                 if self.mModel.load_task_list():
#                     self.taskListUpdate()
#                     self.mRoot.title("Project Planner (" + self.mModel.mProjectName + ")")
#             except _pickle.UnpicklingError:
#                 messagebox.showerror("Error", "There was an error on the file loaded!")
#
#     def saveProject(self):
#         if hasattr(self.mModel, 'mSavedPath') and self.mModel.mSavedPath is None:
#             self.saveAsProject()
#         else:
#             self.mModel.save_as_task_list()
#
#     def saveAsProject(self):
#         self.mModel.save_as_task_list()
#         self.mRoot.title("Project Planner (" + self.mModel.mProjectName + ")")
#
#     def addTask(self):
#         temp_root = tk.Toplevel(self.mView.mTk)
#         pauseTaskList(temp_root)
#         self.mAddTask = addTask.AddTask(temp_root, self.mModel.mMemberList, self.mModel.getNames())
#         self.mAddTask.mBtnSubmit.config(command=self.submitTask)
#         self.mAddTask.mBtnCancel.config(command=self.destroyAddTask)
#
#     def destroyAddTask(self):
#         self.mAddTask.mTk.destroy()
#
#     def taskListUpdate(self):
#         # delete all tasks in view
#         self.mView.mTaskList.mTvTaskList.delete(*self.mView.mTaskList.mTvTaskList.get_children())
#
#         # add all task in view
#         for t in self.mModel.mTaskList:
#             self.mView.mTaskList.mTvTaskList.insert("", "end",
#                                                     values=(t.mTitle, t.mMode, t.mSeverity, t.mInProgress,
#                                                             t.mInitialDate, t.mDueDate, t.mIsBugOn, t.mIsBonusOn,
#                                                             t.mIsDone))
#         self.mView.mTaskList.mLblFilter.config(text=FILTER_OFF)
#
#     def submitTask(self):
#         if self.mAddTask.mVarTitle.get().strip() == "":  # empty title constraint
#             messagebox.showwarning(title="Warning", message="No empty titles allowed!")
#         elif self.isDuplicateTitle(True):  # unique constraint
#             messagebox.showwarning(title="Warning", message="No duplicate titles allowed!")
#         else:
#
#             assignees = []
#             for x in self.mAddTask.mLBAssignees.curselection():
#                 assignees.append(self.mAddTask.mLBAssignees.get(x))
#
#             # add task
#             t = task.Task(self.mAddTask.mVarTitle.get(), self.mAddTask.mTextDescription.get("1.0", "end"),
#                           self.mAddTask.mVarMode.get(), assignees, self.mAddTask.mScaleSeverity.get(),
#                           self.mAddTask.mVarInProgress.get(),
#                           self.mAddTask.mDEInitial.get_date(), self.mAddTask.mDEDue.get_date(),
#                           self.mAddTask.mIsBug, self.mAddTask.mIsBonus, False)
#             self.mModel.mTaskList.append(t)
#
#             self.taskListUpdate()  # update task list view
#             self.destroyAddTask()
#
#     def isDuplicateTitle(self, is_add):
#         if is_add:  # for add task
#             title = self.mAddTask.mVarTitle.get()
#         else:  # for update task
#             title = self.mUpdateTask.mVarTitle.get()
#         for t in self.mModel.mTaskList:
#             if t.mTitle == title:
#                 return True
#         return False
#
#     def closeOpenTask(self):
#         self.mIsDoneUpdated = True
#         self.editTaskView()
#
#     def editTaskView(self):
#         if self.mUpdateTask.mVarTitle.get().strip() == "":  # empty title constraint
#             messagebox.showwarning(title="Warning", message="No empty titles allowed!")
#         elif self.isDuplicateTitle(False) and self.mUpdateTask.mVarTitle.get() \
#                 != self.mUpdateTask.mOldTitle:  # unique constraint for edit
#             messagebox.showwarning(title="Warning", message="No duplicate titles allowed!")
#         else:
#             old_t = self.deleteTaskOnUpdate()  # delete old task
#
#             if self.mIsDoneUpdated:
#                 temp_done = not old_t.mIsDone
#             else:
#                 temp_done = old_t.mIsDone
#
#             assignees = []
#             for x in self.mUpdateTask.mLBAssignees.curselection():
#                 assignees.append(self.mUpdateTask.mLBAssignees.get(x))
#
#             # add task
#             t = task.Task(self.mUpdateTask.mVarTitle.get(), self.mUpdateTask.mTextDescription.get("1.0", "end"),
#                           self.mUpdateTask.mVarMode.get(), self.mUpdateTask.mVarAssignees.get(),
#                           self.mUpdateTask.mScaleSeverity.get(), self.mUpdateTask.mVarInProgress.get(),
#                           self.mUpdateTask.mDEInitial.get_date(), self.mUpdateTask.mDEDue.get_date(),
#                           self.mUpdateTask.mIsBug, self.mUpdateTask.mIsBonus, temp_done)
#
#             self.mModel.mTaskList.append(t)
#
#             self.taskListUpdate()  # update task list view
#             self.destroyUpdateTask()
#             self.mIsDoneUpdated = False
#
#     def deleteTaskView(self):
#         self.deleteTaskOnUpdate()
#         self.destroyUpdateTask()
#
#     def deleteTaskOnUpdate(self):
#         # remove old task
#         for t in self.mModel.mTaskList:
#             if t.mTitle == self.mUpdateTask.mOldTitle:
#                 self.mModel.mTaskList.remove(t)
#                 return t
#
#     def taskClicked(self, instance):
#         region = self.mView.mTaskList.mTvTaskList.identify("region", instance.x, instance.y)
#         item = self.mView.mTaskList.mTvTaskList.identify("item", instance.x, instance.y)
#         if region == "heading":
#             self.sort(instance)
#         # elif self.mView.mTaskList.mLblDelete['text'] == DELETE_ON:
#         #     if len(self.mView.mTaskList.mTvTaskList.selection()) > 0:
#         #         item = self.mView.mTaskList.mTvTaskList.selection()[0]
#         #         # get task
#         #         tsk = None
#         #         for t in self.mModel.mTaskList:
#         #             if t.mTitle == self.mView.mTaskList.mTvTaskList.item(item, "values")[0]:
#         #                 tsk = t
#         #                 break
#         #         self.deleteTask(tsk)
#         elif item:
#             if len(self.mView.mTaskList.mTvTaskList.selection()) > 0:
#                 item = self.mView.mTaskList.mTvTaskList.selection()[0]
#                 # get task
#                 tsk = None
#                 for t in self.mModel.mTaskList:
#                     if t.mTitle == self.mView.mTaskList.mTvTaskList.item(item, "values")[0]:
#                         tsk = t
#                         break
#                 if tsk is not None:
#                     if hasattr(self.mEditDeletePopup, "mTk"):
#                         self.mEditDeletePopup.mTk.destroy()
#                     temp_root = tk.Toplevel(self.mView.mTk)
#                     self.mEditDeletePopup = editDeletePopup.EditDeletePopup(temp_root, self.mView.mTaskList.mTk)
#                     self.mEditDeletePopup.mBtnUpdate.config(command=lambda: self.createAndDestroyUpdateTask(tsk))
#                     self.mEditDeletePopup.mBtnDelete.config(command=lambda: self.deleteTask(tsk))
#
#     def deleteTask(self, tsk):
#         self.mModel.mTaskList.remove(tsk)
#         self.taskListUpdate()
#         self.mEditDeletePopup.mTk.destroy()
#
#     def createAndDestroyUpdateTask(self, tsk):
#         self.mEditDeletePopup.mTk.destroy()
#         new_root = tk.Toplevel(self.mView.mTk)
#         self.createUpdateTask(new_root, tsk)
#
#     def sort(self, instance):
#         if self.mView.mTaskList.mTvTaskList.identify_column(instance.x) == "#1":
#             if hasattr(self, 'mTLColumnClicked') and self.mTLColumnClicked == "#1" and self.mIsReverse:
#                 self.mModel.sort_by_title(False)
#                 self.mIsReverse = False
#             else:
#                 self.mModel.sort_by_title(True)
#                 self.mIsReverse = True
#         elif self.mView.mTaskList.mTvTaskList.identify_column(instance.x) == "#2":
#             if hasattr(self, 'mTLColumnClicked') and self.mTLColumnClicked == "#2" and self.mIsReverse:
#                 self.mModel.sort_by_mode(False)
#                 self.mIsReverse = False
#             else:
#                 self.mModel.sort_by_mode(True)
#                 self.mIsReverse = True
#         elif self.mView.mTaskList.mTvTaskList.identify_column(instance.x) == "#3":
#             if hasattr(self, 'mTLColumnClicked') and self.mTLColumnClicked == "#3" and self.mIsReverse:
#                 self.mModel.sort_by_severity(False)
#                 self.mIsReverse = False
#             else:
#                 self.mModel.sort_by_severity(True)
#                 self.mIsReverse = True
#         elif self.mView.mTaskList.mTvTaskList.identify_column(instance.x) == "#4":
#             if hasattr(self, 'mTLColumnClicked') and self.mTLColumnClicked == "#4" and self.mIsReverse:
#                 self.mModel.sort_by_in_progress(False)
#                 self.mIsReverse = False
#             else:
#                 self.mModel.sort_by_in_progress(True)
#                 self.mIsReverse = True
#         elif self.mView.mTaskList.mTvTaskList.identify_column(instance.x) == "#5":
#             if hasattr(self, 'mTLColumnClicked') and self.mTLColumnClicked == "#5" and self.mIsReverse:
#                 self.mModel.sort_by_initial_date(False)
#                 self.mIsReverse = False
#             else:
#                 self.mModel.sort_by_initial_date(True)
#                 self.mIsReverse = True
#         elif self.mView.mTaskList.mTvTaskList.identify_column(instance.x) == "#6":
#             if hasattr(self, 'mTLColumnClicked') and self.mTLColumnClicked == "#6" and self.mIsReverse:
#                 self.mModel.sort_by_due_date(False)
#                 self.mIsReverse = False
#             else:
#                 self.mModel.sort_by_due_date(True)
#                 self.mIsReverse = True
#         if self.mView.mTaskList.mLblFilter['text'] == FILTER_ON:
#             self.filter()
#         else:
#             self.taskListUpdate()
#         self.mTLColumnClicked = self.mView.mTaskList.mTvTaskList.identify_column(instance.x)
#
#     # def taskDoubleClicked(self, instance):
#     #     self.taskClicked(instance)
#     #     # region = self.mView.mTaskList.mTvTaskList.identify("region", instance.x, instance.y)
#     #     # if region == "heading":
#     #     #     self.sort(instance)
#     #     # else:
#     #     #     if len(self.mView.mTaskList.mTvTaskList.selection()) > 0:
#     #     #         temp_root = tk.Tk()
#     #     #         item = self.mView.mTaskList.mTvTaskList.selection()[0]
#     #     #         # get task
#     #     #         tsk = None
#     #     #         for t in self.mModel.mTaskList:
#     #     #             if t.mTitle == self.mView.mTaskList.mTvTaskList.item(item, "values")[0]:
#     #     #                 tsk = t
#     #     #                 break
#     #     #         self.createUpdateTask(temp_root, tsk)
#
#     def createUpdateTask(self, temp_root, tsk):
#         pauseTaskList(temp_root)
#         self.mUpdateTask = UpdateTask(temp_root, self.mModel.mMemberList, self.mModel.getNames(), tsk)
#         self.mUpdateTask.mBtnSubmit.config(command=self.editTaskView)
#         self.mUpdateTask.mCloseOpenBtn.config(command=self.closeOpenTask)
#         self.mUpdateTask.mBtnDelete.config(command=self.deleteTaskView)
#         self.mUpdateTask.mBtnCancel.config(command=self.destroyUpdateTask)
#
#     def destroyUpdateTask(self):
#         self.mUpdateTask.mTk.destroy()
#
#     def updateMembers(self):
#         temp_root = tk.Toplevel(self.mView.mTk)
#         pauseTaskList(temp_root)
#         if len(self.mModel.mMemberList) == 0:
#             self.mModel.mMemberList.append(Member("Me"))
#         self.mUpdateMembers = updateMembers.UpdateMembers(temp_root)
#         self.mUpdateMembers.mBtnAddMember.config(command=self.addMembersClicked)
#         self.mUpdateMembers.mTvMemberList.bind("<Double-1>", self.memberClicked)  # taskDoubleClicked
#         self.mUpdateMembers.mTvMemberList.bind("<Button-1>", self.memberClicked)
#         self.memberListUpdate()
#
#     def memberClicked(self, instance):
#         # region = self.mUpdateMembers.mTvMemberList.identify("region", instance.x, instance.y)
#         item = self.mUpdateMembers.mTvMemberList.identify("item", instance.x, instance.y)
#         # if region == "heading":
#         #     self.sort(instance)
#         # elif item:
#         if item:
#             if len(self.mUpdateMembers.mTvMemberList.selection()) > 0:
#                 item = self.mUpdateMembers.mTvMemberList.selection()[0]
#                 # get task
#                 m = None
#                 for t in self.mModel.mMemberList:
#                     if t.mName == self.mUpdateMembers.mTvMemberList.item(item, "values")[0]:
#                         m = t
#                         break
#                 if m is not None:
#                     if hasattr(self.mEditDeletePopup, "mTk"):
#                         self.mEditDeletePopup.mTk.destroy()
#                     temp_root = tk.Toplevel(self.mUpdateMembers.mTk)
#                     self.mEditDeletePopup = editDeletePopup.EditDeletePopup(temp_root, self.mUpdateMembers.mTk)
#                     self.mEditDeletePopup.mBtnUpdate.config(command=lambda: self.createAndDestroyUpdateMember(m))
#                     self.mEditDeletePopup.mBtnDelete.config(command=lambda: self.deleteMember(m))
#
#     def createAndDestroyUpdateMember(self, m):
#         self.mEditDeletePopup.mTk.destroy()
#         new_root = tk.Toplevel(self.mUpdateMembers.mTk)
#         self.createUpdateMember(new_root, m)
#
#     def createUpdateMember(self, root, m):
#         pauseTaskList(root)
#         self.mUpdateMember = UpdateMember(root, m)
#         self.mUpdateMember.mBtnSubmit.config(command=self.editMember)
#         self.mUpdateMember.mBtnDelete.config(command=lambda: self.deleteMember(m))
#         self.mUpdateMember.mBtnCancel.config(command=self.destroyUpdateMember)
#         self.mUpdateMember.mTk.protocol('WM_DELETE_WINDOW', self.destroyUpdateMember)
#
#     def destroyUpdateMember(self):
#         self.mUpdateMember.mTk.destroy()
#         pauseTaskList(self.mUpdateMembers.mTk)
#
#     def editMember(self):
#         if self.mUpdateMember.mVarName.get().strip() == "":  # empty title constraint
#             messagebox.showwarning(title="Warning", message="No empty name allowed!")
#         elif self.isDuplicateName(False) and self.mUpdateMember.mVarName.get() \
#                 != self.mUpdateMember.mOldName:  # unique constraint
#             messagebox.showwarning(title="Warning", message="No duplicate name allowed!")
#         else:
#             for m in self.mModel.mMemberList:
#                 if m.mName == self.mUpdateMember.mOldName:
#                     self.mModel.mMemberList.remove(m)
#                     break
#
#             # add task
#             t = member.Member(self.mUpdateMember.mVarName.get())
#             self.mModel.mMemberList.append(t)
#
#             self.memberListUpdate()  # update task list view
#
#             self.destroyUpdateMember()
#
#             pauseTaskList(self.mUpdateMembers.mTk)
#
#     def deleteMember(self, m):
#         self.mModel.mMemberList.remove(m)
#         self.memberListUpdate()
#         self.mEditDeletePopup.mTk.destroy()
#         if hasattr(self.mUpdateMember, "mTk") and hasattr(self.mUpdateMember.mTk, "destroy"):
#             self.mUpdateMember.mTk.destroy()
#         pauseTaskList(self.mUpdateMembers.mTk)
#
#     def addMembersClicked(self):
#         temp_root = tk.Toplevel(self.mUpdateMembers.mTk)
#         pauseTaskList(temp_root)
#         self.mAddMember = addMember.AddMember(temp_root)
#         self.mAddMember.mTk.protocol('WM_DELETE_WINDOW', self.destroyAddMember)
#         self.mAddMember.mBtnSubmit.config(command=self.submitMember)
#         self.mAddMember.mBtnCancel.config(command=self.destroyAddMember)
#
#     def destroyAddMember(self):
#         self.mAddMember.mTk.destroy()
#         pauseTaskList(self.mUpdateMembers.mTk)
#
#     def submitMember(self):
#         if self.mAddMember.mVarName.get().strip() == "":  # empty title constraint
#             messagebox.showwarning(title="Warning", message="No empty name allowed!")
#         elif self.isDuplicateName(True):  # unique constraint
#             messagebox.showwarning(title="Warning", message="No duplicate name allowed!")
#         else:
#             # add task
#             t = member.Member(self.mAddMember.mVarName.get())
#             self.mModel.mMemberList.append(t)
#
#             self.memberListUpdate()  # update task list view
#             self.destroyAddMember()
#
#     def memberListUpdate(self):
#         # delete all members in view
#         self.mUpdateMembers.mTvMemberList.delete(*self.mUpdateMembers.mTvMemberList.get_children())
#
#         # add all member in view
#         for t in self.mModel.mMemberList:
#             self.mUpdateMembers.mTvMemberList.insert("", "end",
#                                                      values=(t.mName))
#
#     def isDuplicateName(self, is_add):
#         if is_add:  # for add
#             name = self.mAddMember.mVarName.get()
#         else:  # for update
#             name = self.mUpdateMember.mVarName.get()
#         for t in self.mModel.mMemberList:
#             if t.mName == name:
#                 return True
#         return False
#
#
# def about():
#     messagebox.showinfo(title="About", message=ABOUT_MSG)
#
#
# def helpTutorial():
#     messagebox.showinfo(title="Help", message=HELP_MSG)
#
#
def pauseTaskList(window):
    window.grab_set()
