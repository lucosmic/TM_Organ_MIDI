from playMidiOrgan import  *


class Application(tk.Frame):              
    def __init__(self, master=None):
        
        tk.Frame.__init__(self, master)   
        self.grid()                       
        self.createWidgets()
        self.m = MIDIPlayer()
        chanRt={0:0,4:1,5:2,6:3,7:1,8:2,9:3,10:10,11:2,12:3,13:1,14:2,15:3}
        self.m.setReroute(chanRoute=chanRt)
        self.play=False
        self.running=True

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit',
            command=self.quito)            
        self.quitButton.grid()
        self.lfButton = tk.Button(self, text='Load File',
            command=self.loadFile)            
        self.lfButton.grid()
        self.pauseButton = tk.Button(self, text='Pause File',
            command=self.pauseFile)            
        self.pauseButton.grid()  
    
    def loadFile(self):
        self.m.port.panic()
        try:
            self.m.openFile(askopenfilename(initialdir='/home/pi/MIDIMusic/MIDI_Files',
                                     filetypes = [('MIDI Files','*.mid*')] ))
            self.play=True
        except:
            return 1
        
        return 0
    
    def pauseFile(self):
        self.play=not self.play
        self.m.port.panic()
    
    def updateMidi(self):
        m=self.m
        m.midi_thru()
        if self.play:
            m.update_playfile()
    
    def quito(self):
        print("Program Ended")
        self.m.port.panic()
        self.m.port.close()
        self.destroy()
        self.quit()
        self.running=False
        
        
        
if __name__ == "__main__":
    app = Application()                       
    app.master.title('Sample application')    
    while app.running:
        app.update()
        app.updateMidi()
    
    print("PMOapp exited")
    