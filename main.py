import tkinter as tk
from tkinter import messagebox

def confirm_exit():
    if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
        root.quit()

root = tk.Tk()
btn_exit = tk.Button(root, text="Exit", command=confirm_exit)
btn_exit.pack(pady=20)

root.mainloop()