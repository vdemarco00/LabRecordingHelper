# LabRecordingHelper.py contains all UI-related code.

# NOTE:
# graph using Matplotlib?
# UI using Tkinter

import tkinter as tk
from RecordingService import RecordingService

class Application(tk.Frame):
    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        LabRecorder = RecordingService()

        button = tk.Button(root, text="Do Stuff", command=LabRecorder.TestFunc)
        button.pack()

root = tk.Tk()
root.title("LabRecordingHelper")
root.geometry("500x200")
app = Application(root)
root.mainloop()
