# The RecordingService class contains all logic related to receiving and persisting
# data gathered from the Lab Streaming Layer (LSL). Currently only supports the Muse headband,
# but functionality may be extended for other devices.

from pylsl import StreamInlet, resolve_stream
import csv
import time
import sys

from pylsl.pylsl import resolve_byprop

class RecordingService:

    def __init__(self):
        self.fields = ['TIMESTAMP', 'TP9', 'AF7', 'AF8', 'TP10', 'RIGHT AUX', 'MARKER']
        
        self.EEGStreams = any
        self.markerStreams = any
        self.isRecording = False

        # TODO: define class variables for EEG, timestamp, marker data

        self.EEGDataList = []
        self.EEGTimestampList = []
        self.markerList = []

    def FindStreams(self):
        print("Waiting for EEG stream...")

        self.EEGStreams = resolve_byprop('type', 'EEG', timeout=10)
        if len(self.EEGStreams) > 0:
            print("Found EEG stream.")
        else:
            print("EEG stream timed out.")
            return False
        
        self.markerStreams = resolve_byprop('type', 'Markers', timeout=10)
        if len(self.markerStreams) > 0:
            print("Found marker stream.")
        else:
            print("Marker stream timed out.")
            return False
        
        return True


    # Record EEG and Marker data for a specified duration of time. Defaults to 30 seconds if no arguments are passed.
    def RecordEEG(self, recordDuration: float):

        markerInlet = StreamInlet(self.markerStreams[0])
        EEGInlet = StreamInlet(self.EEGStreams[0])

        start = time.time()
        print("Recording started.")

        while time.time() - start < recordDuration:
            samples,timestamps = EEGInlet.pull_chunk()

            markerData,markerTimestamp = markerInlet.pull_sample()

            self.EEGDataList.append(samples)

            self.EEGTimestampList.append(timestamps)

            self.markerList.append([markerTimestamp, markerData])
        
        self.PersistData()
        print("Recording ended.")

    def StartRecord(self):
        # TODO: empty lists before recording

        if self.isRecording:
            print("Already recording.")
            return
        
        self.isRecording = True

        markerInlet = StreamInlet(self.markerStreams[0])
        EEGInlet = StreamInlet(self.EEGStreams[0])

        print("Recording started.")

        while self.isRecording:
            samples,timestamps = EEGInlet.pull_chunk()

            markerData,markerTimestamp = markerInlet.pull_sample()

            self.EEGDataList.append(samples)
            self.EEGTimestampList.append(timestamps)
            self.markerList.append([markerTimestamp, markerData])
    
    def StopRecord(self):
        if not self.isRecording:
            print("No active recordings.")
            return
        
        self.isRecording = False
        print("Recording stopped.")

    def PersistData(self):
        # TODO: save to a .csv
        finalDataList = []
        currentIndex = 0
        for i in range(0, len(self.EEGDataList)):
            for j in range(0, len(self.EEGDataList[i])):
                finalDataList.append(self.EEGDataList[i][j])
                finalDataList[currentIndex].insert(0, self.EEGTimestampList[i][j])
                currentIndex += 1
        
        with open('testSave.csv', 'w') as saveFile:
            writer = csv.writer(saveFile)

            writer.writerow(self.fields)
            writer.writerows(finalDataList)

    def GenerateSnapshot(self):
        # TODO: provide chunk of data for UI to display
        pass

    def TestAsync(self):
        time.sleep(3)
        print("Hello")
        


if __name__ == "__main__":
    service = RecordingService()
    service.RecordEEG(10)
