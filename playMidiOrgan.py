
import mido
import rtmidi_python
import re
import os, time
import tkinter as tk
from tkinter.filedialog import askopenfilename


class MIDIPlayer:
    CC_ON=81
    CC_OFF=80
    INSTRUMENTS_CC={"Bourdon16":51,"Diapason8":32,"Flute8":48,"Dulciana8":16,"Principal4":33,
                    "Salicianal8":0,"Flute4":49,"Nazard2 2/3":55,"Flute2":50,"Dulcet4":17,
                    "Twelfth2 2/3":39,"Fifteenth2":34,"Oboe8":40}
    #"Quint8":[55,48]
    #"Oboe8":[55,40]
    
    def __init__(self,filename='', port_num = None):
        self.midifile = None
        #self.openFile(filename)
        self.port = self.open_midi_io()
        
        self.UP_now = None
        
    
    def __del__(self):
        self.port.panic()
        self.port.close()
        
    def open_midi_io(self,port_num = None):
        ''' Open first USB Midi IO port available. Use port_num = # to specify a number.'''
        if port_num == None:
            for i,name in enumerate(mido.get_ioport_names()):
                usb_match = re.search("USB",name)
                if usb_match:
                    port_num = i
                    break
            
        port = mido.open_ioport(mido.get_ioport_names()[port_num])
        return port
    
    def openFile(self,filename):
        
        try:
            self.midifile=mido.MidiFile(filename)
            self.__fileiter = iter(self.midifile)
            self.msg = next(self.__fileiter)
            
            #Default tempo is 50k microseconds, or 120BPM
            self.fileTempoScale=1
            
        except:
            self.midifile=None
            print("Error occured while attempting file open.")
            raise Exception
        
    def update_playfile(self,debug=False):
        msg=self.msg
        if not self.midifile: return 
        
        #Start/Update Timer
        if self.UP_now:
            self.UP_B4 = self.UP_now
            self.UP_now= time.time()
        else:
            #Set both prev. time and current time equal
            self.UP_now= time.time()
            self.UP_B4 = self.UP_now
            self.UP_lastNote = self.UP_now
            print('start play: ',self.midifile)
        
        #Check whether enough time has elapsed since the last note was played to play the next note. 
        while msg.time == 0 or self.UP_now - self.UP_lastNote >= msg.time*self.fileTempoScale:
            if msg.type not in ['sysex'] and not msg.is_meta:
                #If playable message
                if debug:
                    print(msg)
                else:
                    msg = self.rerouteNotes(msg)
                    self.port.send(msg)
                
                #Iterate to next message. 
                self.msg = next(self.__fileiter)
                self.UP_lastNote=self.UP_now
            elif msg.type == 'set_tempo':
                #Scale Tempo
                self.fileTempoScale = 1    #msg.tempo/500000.0 *1
                #Iterate to next message. 
                self.msg = next(self.__fileiter)
                self.UP_lastNote=self.UP_now
            else:
                #Iterate thru the messages until the song is finished. 
                try:
                    self.msg = next(self.__fileiter)
                except: StopIteration
                return 1
                
                self.UP_lastNote=self.UP_now
                
            return 0
        
    
    def midi_thru(self):
        for msg in self.port.iter_pending():
                print(msg)
                self.port.send(msg)
    
    def playNote(self,msg):
        '''playNote(mido.Message('note_on',note=100,velocity=127,time=1)'''
        if msg.type=='note_on':
            self.port.send(msg)
            time.sleep(msg.time)
            msg.velocity=0
            self.port.send(msg)
            
    def setReroute(self, chanRoute={0:0,1:1,2:2,3:3},CCR={16:16}):
        '''Route old:new. Available Instruments:0,16,17,32,33,34,39,40,48,49,50,51,55
        Channel:
        0 piano(other)
        1 Great
        2 Swell (Top keys)
        3 Pedal
        9 Air Swell
        (10 perc)
        
        CC Value <> Instrument
        Piano: 1-8
        Chromatic Percussion: 16 Dulcimer > GSP Dulciana8
        Organ: 17 Drawbar Organ > Dullcet4
        Guitar: 32 Guitar harmonics > Diapason8
        Bass: 33 Acoustic Bass > Principal4
              34 Electric Bass (finger) > Fifteenth2
              39 Synth Bass 1 > Twelfth2-2/3
              40 Synth Bass 2 
        Strings: 48 Timpani > Flute8
        Strings (cont):
            49 String Ensemble 1 > Flute4
            50 String Ensemble 2 > Flute2
            51 Synth Strings 1 > Bourdoin16
            55 Synth Voice > Nazard2-2/3
            '''
        self.channelRoute = chanRoute
        self.InstRoute = CCR
        
    def rerouteNotes(self, msg):
        try:
            msg.channel = self.channelRoute[msg.channel]
        except KeyError:
            pass
        except AttributeError:
            #Likely a sysex msg. 
            pass
        return msg
            
        
    
if __name__ == "__main__":
    m = MIDIPlayer()
    while True:
        try:
            m.openFile(askopenfilename(initialdir='/home/pi/MIDIMusic/MIDI_Files',
                                     filetypes = [('MIDI Files','*.mid*')] ))
        except:
            break
        chanRt={0:1,4:1,5:2,6:3,7:1,8:2,9:3,10:10,11:2,12:3,13:1,14:2,15:3}
        m.setReroute(chanRoute=chanRt)
        while True:
            try:
                m.midi_thru()
                
                #m.update_playfile()
            except(KeyboardInterrupt,SystemExit):
                
                del m
                break
            
    print("Program Ended")
            
