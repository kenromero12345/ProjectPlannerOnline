import tkinter as tk  # python 3
from View import taskList
from View.login import Login
from View.projectList import ProjectList
from View.taskList import TaskList


class View:
    def __init__(self):
        # initialize var
        self.mMenuFile = None
        self.mMenuHelp = None
        self.mMenuEdit = None
        self.mTaskList = None
        self.mProjectList = None

        self.mTk = tk.Tk()
        self.mTk.resizable(False, False)
        frame = tk.Frame(self.mTk)
        # self.menu_bar(root)
        # self.mTaskList = taskList.TaskList(frame)
        self.mLogin = Login(frame)
        self.mTk.wm_title("Login")
        frame.pack()
        center(self.mTk)

    def createProjectList(self, lst):
        print("project list")
        self.mTk.destroy()
        self.mTk = tk.Tk()
        self.mTk.resizable(False, False)
        # self.menuBar(self.mTk)
        self.menuBarProject(self.mTk)
        self.mProjectList = ProjectList(self.mTk)

        if lst is not None:
            for x in lst:
                self.mProjectList.mTvProjectList.insert("", "end", values=(x[0]))

        center(self.mTk)

    # def updateTaskList(self, name):
    #     print("update task list")
    #     self.mTk.destroy()
    #     self.mTk = tk.Tk()
    #     self.menuBar(self.mTk)
    #     self.mTaskList = TaskList(self.mTk, name)

    def createTaskList(self, name):
        print("create task list")
        self.mTk.destroy()
        self.mTk = tk.Tk()
        self.mTk.resizable(False, False)
        self.menuBar(self.mTk)
        self.mTaskList = TaskList(self.mTk, name)

    def menuBarProject(self, root):
        menu = tk.Menu(root)
        self.mMenuFile = tk.Menu(menu, tearoff=0)
        self.mMenuFile.add_command(label="New Project")
        self.mMenuFile.add_separator()
        self.mMenuFile.add_command(label="Logout")
        self.mMenuFile.add_command(label="Exit")
        menu.add_cascade(label="File", menu=self.mMenuFile)
        self.mMenuHelp = tk.Menu(menu, tearoff=0)
        self.mMenuHelp.add_command(label="Help")
        self.mMenuHelp.add_command(label="About")
        menu.add_cascade(label="Help", menu=self.mMenuHelp)
        root.config(menu=menu)

    def menuBar(self, root):
        menu = tk.Menu(root)
        self.mMenuFile = tk.Menu(menu, tearoff=0)
        self.mMenuFile.add_command(label="New Project")
        self.mMenuFile.add_command(label="New Task")
        self.mMenuFile.add_command(label="Update Members")
        self.mMenuFile.add_command(label="View Projects")
        # self.mMenuFile.add_command(label="Open...")
        # self.mMenuFile.add_command(label="Save...")
        # self.mMenuFile.add_command(label="Save As...")
        self.mMenuFile.add_separator()
        self.mMenuFile.add_command(label="Logout")
        self.mMenuFile.add_command(label="Exit")
        menu.add_cascade(label="File", menu=self.mMenuFile)
        self.mMenuEdit = tk.Menu(menu, tearoff=0)
        self.mMenuEdit.add_command(label="Filters")
        self.mMenuEdit.add_command(label="Reset Filter")
        menu.add_cascade(label="Edit", menu=self.mMenuEdit)
        self.mMenuHelp = tk.Menu(menu, tearoff=0)
        self.mMenuHelp.add_command(label="Help")
        self.mMenuHelp.add_command(label="About")
        menu.add_cascade(label="Help", menu=self.mMenuHelp)
        root.config(menu=menu)


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
