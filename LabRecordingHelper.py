# LabRecordingHelper.py contains all UI-related code.

# NOTE:
# graph using Matplotlib?
# UI using Tkinter

import asyncio
import tkinter as tk
from RecordingService import RecordingService
import threading

class Application(tk.Frame):
    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.LabRecorder = RecordingService()

        button = tk.Button(root, text="Do Stuff", command=self.ThreadTest)
        button.pack()

    def ThreadTest(self):
        newThread = threading.Thread(target=self.LabRecorder.TestAsync)
        newThread.start()

root = tk.Tk()
root.title("LabRecordingHelper")
root.geometry("500x200")
app = Application(root)
root.mainloop()
