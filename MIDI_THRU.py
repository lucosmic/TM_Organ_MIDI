'''
Run MIDI from keyboard console to RPi to Organ


'''
import mido
import re

def open_midi_io():
    port_num = 0;
    for i,name in enumerate(mido.get_ioport_names()):
        usb_match = re.search("USB",name)
        if usb_match:
            port_num = i
            break
        
    port = mido.open_ioport(mido.get_ioport_names()[port_num])
    return port

if __name__ == '__main__':
    port = open_midi_io()
    
    while True:
        for msg in port.iter_pending():
            print(msg)
            port.send(msg)
        
        #app.update()
        #midifile.play_dude()
    
    
    port.close()