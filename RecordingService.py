from pylsl import StreamInlet, resolve_stream
import csv
import time
import sys

class RecordingService:

    def __init__(self):
        self.fields = ['TP9', 'AF7', 'AF8', 'TP10', 'RIGHT AUX']
        
        self.EEGStreams = any
        self.markerStreams = any
        self.isRecording = False

        # TODO: define class variables for EEG, timestamp, marker data



    # Record EEG and Marker data for a specified duration of time. Defaults to 30 seconds if no arguments are passed.
    def RecordEEG(self, recordDuration: float):
        
        print("Waiting for EEG stream...")
        self.EEGStreams = resolve_stream('type', 'EEG')
        print("Found EEG stream.")

        print("Waiting for marker stream...")
        self.markerStreams = resolve_stream('type', 'Markers')
        print("Found marker stream.")

        markerInlet = StreamInlet(self.markerStreams[0])
        EEGInlet = StreamInlet(self.EEGStreams[0])

        start = time.time()
        print("Recording started.")

        while time.time() - start < recordDuration:
            samples,timestamps = EEGInlet.pull_chunk()

            markerData,markerTimestamp = markerInlet.pull_sample()

    def StartRecord(self):
        # TODO: empty lists before recording

        if self.isRecording:
            print("Already recording.")
            return
        
        print("Waiting for EEG stream...")
        self.EEGStreams = resolve_stream('type', 'EEG')
        print("Found EEG stream.")

        print("Waiting for marker stream...")
        self.markerStreams = resolve_stream('type', 'Markers')
        print("Found marker stream.")
        
        self.isRecording = True

        markerInlet = StreamInlet(self.markerStreams[0])
        EEGInlet = StreamInlet(self.EEGStreams[0])

        print("Recording started.")

        while self.isRecording:
            # TODO: push data to class variable
            samples,timestamps = EEGInlet.pull_chunk()

            markerData,markerTimestamp = markerInlet.pull_sample()
    
    def StopRecord(self):
        if not self.isRecording:
            print("No active recordings.")
            return
        
        self.isRecording = False
        print("Recording stopped.")

    def PersistData(self):
        # TODO: save to a .csv
        pass

    def GenerateSnapshot(self):
        # TODO: provide chunk of data for UI to display
        pass
    
    def TestFunc(self):
        print("This works!")

    


