
'''
A program that extracts the first lines of a midi file 
'''

import mido
import rtmidi_python
import re
from tkinter.filedialog import askopenfilename

def getOrganProgs(origMidiFile): 


    origMidi = mido.MidiFile(origMidiFile)
    print('Listing Tracks in original file:')
    for i,tr in enumerate(origMidi.tracks): print(i,tr)
    try:
        trackNum = int(input('Which track do you want?\n>>>'))
        tr = origMidi.tracks[trackNum]
    except:
        print("Error")
        
    print('Using track ',trackNum, repr(tr))
    print('First lines:')
    for i,msg in enumerate(tr[1:100]): print(i,msg) 
    msgLine = int(input('Which line do you want to save up to?\n-2 selects tracks again. \n>>>'))+1
    
    if msgLine==-1: return 0
    
    print('\nThe file was '+ origMidiFile+ ' track name '+ tr.name)
    newMidiFile = input('What do you want to save the new file as?\n>>>')

    prgm = mido.MidiFile()
    track = mido.MidiTrack()
    prgm.tracks.append(track)

    for i in range(msgLine):
        track.append(origMidi.tracks[1][i])

    prgm.save(newMidiFile)
    return 1

if __name__ == "__main__":
    file = askopenfilename(initialdir='/home/pi/MIDIMusic/MIDI_Files',
                                 filetypes = [('MIDI Files','*.mid*')])
    ret=0
    while ret==0:
        getOrganProgs(file)