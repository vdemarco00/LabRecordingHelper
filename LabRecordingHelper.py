# UI stuff
# graph Matplotlib?
# UI using Tkinter or Qt

import tkinter as tk
from RecordingService import RecordingService

root = tk.Tk()
LabRecorder = RecordingService()

# place a label on the root window
message = tk.Label(root, text="Hello, World!")
message.pack()

button = tk.Button(root, text="Do Stuff", command=LabRecorder.TestFunc)
button.pack()
# keep the window displaying
root.mainloop()