from tkinter import ttk


class EditDeletePopup:
    def __init__(self, t, win):
        self.mTk = t
        # buttons
        self.mBtnUpdate = ttk.Button(t, text="Edit")
        self.mBtnUpdate.pack(side="top", fill="x")
        self.mBtnDelete = ttk.Button(t, text="Delete")
        self.mBtnDelete.pack(side="top", fill="x")
        self.mBtnCancel = ttk.Button(t, text="Cancel", command=t.destroy)
        self.mBtnCancel.pack(side="top", fill="x")
        # remove title
        t.overrideredirect(True)
        # position near mouse
        t.update_idletasks()
        width = t.winfo_width()
        height = t.winfo_height()
        x = win.winfo_pointerx() + 20
        y = win.winfo_pointery() - 20
        t.geometry('{}x{}+{}+{}'.format(width, height, x, y))
