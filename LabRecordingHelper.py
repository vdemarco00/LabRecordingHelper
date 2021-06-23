# LabRecordingHelper.py contains all UI-related code.

# NOTE:
# graph using Matplotlib?
# UI using Tkinter

import tkinter as tk
from tkinter.constants import *
from tkinter import Button, filedialog
from RecordingService import RecordingService
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.figure import Figure 

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

        saveButton = tk.Button(root, text="Save", command=self.SaveRecording, width=10, height=2)
        saveButton.place(x=20, y=130)

        self.statusMessage = tk.Label(root, text="No streams loaded.")
        self.statusMessage.place(x=130, y=15)

        self.fig = Figure()

        self.ax = self.fig.add_subplot(111)
        self.ax.grid()

        self.graph = FigureCanvasTkAgg(self.fig, master=root)
        self.graph.get_tk_widget().pack()

        self.LabRecorder.SnapshotSubscribe(self.plotter)

    def plotter(self, dpts, timestamps):
        self.ax.cla()
        self.ax.grid()

        self.ax.plot(dpts, timestamps)
        self.graph.draw_idle()

    def FindStreams(self):
        self.foundStreams = self.LabRecorder.FindStreams()
        if self.foundStreams:
            self.statusMessage.config(text="Found streams. Ready to record.")
        else:
            self.statusMessage.config(text="Could not find streams. Try again.")


    def StartRecording(self):
        if self.foundStreams:
            threading.Thread(target=self.LabRecorder.StartRecord, daemon=True).start()
            self.statusMessage.config(text="Recording started.")
        else:
            self.statusMessage.config(text="No streams available. Unable to record.")
            print("No available streams.")
    
    def StopRecording(self):
        if self.foundStreams:
            threading.Thread(target=self.LabRecorder.StopRecord, daemon=True).start()
            self.statusMessage.config(text="Recording stopped.")
        else:
            print("No available streams.")
    
    def SaveRecording(self):
        if len(self.LabRecorder.EEGDataList) == 0:
            print("No data to save.")
            return
        savePath = filedialog.asksaveasfilename(defaultextension='.csv')
        if not savePath == '':
            self.LabRecorder.PersistData(savePath)


root = tk.Tk()
root.title("LabRecordingHelper")
root.geometry("1280x720")
app = Application(root)
root.mainloop()