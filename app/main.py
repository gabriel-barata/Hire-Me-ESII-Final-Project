from tkinter import *
from tkinter import messagebox
from modules.login import *

from utils.variables import ELEMENTS_FOLDER

root = Tk()
root.geometry("1050x700")
root.title("Hire ME")
root.resizable(0, 0)
root.iconbitmap(str(ELEMENTS_FOLDER / "favicon.ico"))
log(root)
root.mainloop()
