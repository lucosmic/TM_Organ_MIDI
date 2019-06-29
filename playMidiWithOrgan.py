
import mido
import rtmidi_python
import re
import os
import tkinter as tk
from tkinter.filedialog import askopenfilenames

class Application(tk.Frame):              
    def __init__(self, master=None):
        
        tk.Frame.__init__(self, master)   
        self.grid()                       
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit',
            command=self.quito)            
        self.quitButton.grid()
        self.aButton = tk.Button(self, text='zex',
            command=self.a)            
        self.aButton.grid()            
    
    def a(self):
        print("Why")
    
    def quito(self):
        print("Program Ended")
        port.panic()
        port.close()
        self.destroy()
        self.quit()

class MIDIPlayer:
    def __init__(self):
        self.midifile = mido.MidiFile(filename)
    

def playMidi(filename):
    global app, port

    midifile = mido.MidiFile(filename)
    
    print("Playing ",midifile)
    try:
        for msg in midifile.play():
            port.send(msg)
            app.update()
            
    except(KeyboardInterrupt,SystemExit):
        print("Program Ended")
        port.panic()
        port.close()
            



    port.close()
    
def midiFile_update(filename):
    global app, port

    midifile = mido.MidiFile(filename)
    
    print("Playing ",midifile)
    try:
        for msg in midifile.play():
            port.send(msg)
            app.update()
            
    except(KeyboardInterrupt,SystemExit):
        print("Program Ended")
        port.panic()
        port.close()
            



    port.close()
    
    
if __name__ == "__main__":
    root = tk.Tk()
    port = mido.open_ioport(mido.get_ioport_names()[1])
    
    app = Application()                       
    app.master.title('Sample application')    
    app.update()                   

    
    #Tk().withdraw()
    filenames = askopenfilenames(initialdir='/home/pi/MIDIMusic/MIDI_Files',
                                 filetypes = [('MIDI Files','*.mid*')])

    for fn in filenames:
        print(fn)
        playMidi(fn)