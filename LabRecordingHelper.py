# LabRecordingHelper.py contains all UI-related code.

# NOTE:
# graph using Matplotlib?
# UI using Tkinter

import tkinter as tk
from RecordingService import RecordingService

class Application():
    def __init__(self):
        root = tk.Tk()
        LabRecorder = RecordingService()

        message = tk.Label(root, text="LabRecordingHelper")
        message.pack()

        button = tk.Button(root, text="Do Stuff", command=LabRecorder.TestFunc)
        button.pack()

        root.mainloop()


app = Application()
