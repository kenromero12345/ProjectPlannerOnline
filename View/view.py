import tkinter as tk  # python 3
from View import taskList
from View.login import Login


class View:
    def __init__(self):
        # initialize var
        # self.mMenuFile = None
        # self.mMenuHelp = None
        # self.mMenuEdit = None
        self.mTk = tk.Tk()
        frame = tk.Frame(self.mTk)
        # self.menu_bar(root)
        # self.mTaskList = taskList.TaskList(frame)
        self.mLogin = Login(frame)
        self.mTk.wm_title("Login")
        frame.pack()
        center(self.mTk)

    # def menu_bar(self, root):
    #     menu = tk.Menu(root)
    #     self.mMenuFile = tk.Menu(menu, tearoff=0)
    #     self.mMenuFile.add_command(label="New Project")
    #     self.mMenuFile.add_command(label="New Task")
    #     self.mMenuFile.add_command(label="Update Member...")
    #     self.mMenuFile.add_command(label="Open...")
    #     self.mMenuFile.add_command(label="Save...")
    #     self.mMenuFile.add_command(label="Save As...")
    #     self.mMenuFile.add_separator()
    #     self.mMenuFile.add_command(label="Exit")
    #     menu.add_cascade(label="File", menu=self.mMenuFile)
    #     self.mMenuEdit = tk.Menu(menu, tearoff=0)
    #     self.mMenuEdit.add_command(label="Filter...")
    #     self.mMenuEdit.add_command(label="Reset Filter")
    #     menu.add_cascade(label="Edit", menu=self.mMenuEdit)
    #     self.mMenuHelp = tk.Menu(menu, tearoff=0)
    #     self.mMenuHelp.add_command(label="Help")
    #     self.mMenuHelp.add_command(label="About")
    #     menu.add_cascade(label="Help", menu=self.mMenuHelp)
    #     root.config(menu=menu)


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
