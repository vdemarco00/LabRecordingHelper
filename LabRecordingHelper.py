# LabRecordingHelper.py contains all UI-related code.

# NOTE:
# graph using Matplotlib?
# UI using Tkinter

import tkinter as tk
from tkinter.constants import *
from RecordingService import RecordingService
import threading

class Application(tk.Frame):
    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.LabRecorder = RecordingService()
        self.foundStreams = False

        findButton = tk.Button(root, text="Find Streams", command=self.FindStreams, width=10, height=2)
        findButton.place(x=20, y=10, anchor=NW)

        startButton = tk.Button(root, text="Start", command=self.StartRecording, width=10, height=2)
        startButton.place(x=20, y=50)

        stopButton = tk.Button(root, text="Stop", command=self.StopRecording, width=10, height=2)
        stopButton.place(x=20, y=90)

        self.statusMessage = tk.Label(root, text="No streams loaded.")
        self.statusMessage.place(x=130, y=15)


    def ThreadTest(self):
        newThread = threading.Thread(target=self.LabRecorder.TestAsync)
        newThread.start()

    def FindStreams(self):
        self.foundStreams = self.LabRecorder.FindStreams()
        if self.foundStreams:
            self.statusMessage.config(text="Found streams. Ready to record.")
        else:
            self.statusMessage.config(text="Could not find streams. Try again.")


    def StartRecording(self):
        if self.foundStreams:
            threading.Thread(target=self.LabRecorder.StartRecord).start()
        else:
            print("No available streams.")
    
    def StopRecording(self):
        if self.foundStreams:
            threading.Thread(target=self.LabRecorder.StopRecord).start()
        else:
            print("No available streams.")

root = tk.Tk()
root.title("LabRecordingHelper")
root.geometry("600x300")
app = Application(root)
root.mainloop()
