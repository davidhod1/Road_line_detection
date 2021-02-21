import tkinter as tk
from Application import LineApp


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1200x700")
    root.resizable(False, False)
    app = LineApp(master=root)