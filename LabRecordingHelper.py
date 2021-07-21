# LabRecordingHelper.py contains all UI-related code.

import tkinter as tk
from tkinter.constants import *
from tkinter import Button, filedialog

from matplotlib import figure
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

        findButton = tk.Button(root, text="Find Streams", command=self.FindStreams, width=10)
        findButton.place(x=20, y=40, anchor=NW)

        startButton = tk.Button(root, text="Start", command=self.StartRecording, width=10)
        startButton.place(x=20, y=80)

        stopButton = tk.Button(root, text="Stop", command=self.StopRecording, width=10)
        stopButton.place(x=20, y=120)

        saveButton = tk.Button(root, text="Save", command=self.SaveRecording, width=10)
        saveButton.place(x=20, y=160)

        self.statusMessage = tk.Label(root, text="No streams loaded.")
        self.statusMessage.place(x=20, y=10)

        self.fig = Figure(figsize=(11,10))
        

        self.numSubplots = 4
        self.ax1Active = True
        self.ax2Active = True
        self.ax3Active = True
        self.ax4Active = True

        self.ax1 = self.fig.add_subplot(self.numSubplots,1,1)
        self.ax2 = self.fig.add_subplot(self.numSubplots,1,2)
        self.ax3 = self.fig.add_subplot(self.numSubplots,1,3)
        self.ax4 = self.fig.add_subplot(self.numSubplots,1,4)
        self.ax1.grid()
        self.ax2.grid()
        self.ax3.grid()
        self.ax4.grid()
        self.ax1.set_title("TP9")
        self.ax2.set_title("AF7")
        self.ax3.set_title("AF8")
        self.ax4.set_title("TP10")
        self.fig.tight_layout(h_pad=2)
        self.dp1 = []
        self.dp2 = []
        self.dp3 = []
        self.dp4 = []
        self.prev1 = []
        self.prev2 = []
        self.prev3 = []
        self.prev4 = []
        self.stamps = []



        self.graph = FigureCanvasTkAgg(self.fig, master=root)
        self.graph.get_tk_widget().pack(side="right")
        # side="right",ipadx=220, ipady=400
        self.LabRecorder.SnapshotSubscribe(self.plotter)

    def plotter(self, dpts, timestamps):
        #Not sure what the fastest way to do this is 
        
        self.ax1.cla()
        self.ax1.grid()
        self.ax2.cla()
        self.ax2.grid()
        self.ax3.cla()
        self.ax3.grid()
        self.ax4.cla()
        self.ax4.grid()

        prev1temp = []
        prev2temp = []
        prev3temp = []
        prev4temp = []

        for pt in dpts:
            self.dp1.append(pt[0])
            self.dp2.append(pt[1])
            self.dp3.append(pt[2])
            self.dp4.append(pt[3])
        
        for stamp in timestamps:
            self.stamps.append(stamp)

        maxSamples = 4096
        if len(self.stamps) > maxSamples:
            self.stamps = self.stamps[len(self.stamps) - maxSamples:len(self.stamps)]
            self.dp1 = self.dp1[len(self.dp1) - maxSamples:len(self.dp1)]
            self.dp2 = self.dp2[len(self.dp2) - maxSamples:len(self.dp2)]
            self.dp3 = self.dp3[len(self.dp3) - maxSamples:len(self.dp3)]
            self.dp4 = self.dp4[len(self.dp4) - maxSamples:len(self.dp4)]
        
        # print(self.stamps[len(self.stamps) - 1] - self.stamps[0])
        countNeeded = len(self.dp1) - len(self.prev1)
        # print("needed: {}".format(countNeeded))

        prev1temp = [0] * countNeeded
        prev2temp = [0] * countNeeded
        prev3temp = [0] * countNeeded
        prev4temp = [0] * countNeeded
        prev1temp.extend(self.prev1)
        prev2temp.extend(self.prev2)
        prev3temp.extend(self.prev3)
        prev4temp.extend(self.prev4)

        # print("final {}".format(len(prev1temp)))
        # print("timestamps {}".format(len(self.stamps)))
        
        if len(prev1temp) > 0:
            self.ax1.plot(self.stamps, prev1temp)
            self.ax2.plot(self.stamps, prev2temp)
            self.ax3.plot(self.stamps, prev3temp)
            self.ax4.plot(self.stamps, prev4temp)
        self.ax1.plot(self.stamps, self.dp1)
        self.ax2.plot(self.stamps, self.dp2)
        self.ax3.plot(self.stamps, self.dp3)
        self.ax4.plot(self.stamps, self.dp4)

        self.graph.draw_idle()

        self.prev1 = []
        self.prev2 = []
        self.prev3 = []
        self.prev4 = []

        for pt in dpts:
            self.prev1.append(pt[0])
            self.prev2.append(pt[1])
            self.prev3.append(pt[2])
            self.prev4.append(pt[3])



    def FindStreams(self):
        self.foundStreams = self.LabRecorder.FindStreams()
        if self.foundStreams:
            self.statusMessage.config(text="Ready to record.")
        else:
            self.statusMessage.config(text="Streams not found.")


    def StartRecording(self):
        self.dp1 = []
        self.dp2 = []
        self.dp3 = []
        self.dp4 = []
        self.stamps = []
        if self.foundStreams:
            threading.Thread(target=self.LabRecorder.StartRecord, daemon=True).start()
            self.statusMessage.config(text="Recording started.")
        else:
            self.statusMessage.config(text="No available streams.")
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