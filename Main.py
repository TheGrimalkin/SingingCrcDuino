import mido

from mido import MidiFile
from mido import Message

class Note:
    note = "$$"
    time = 500 #in ms
    endSilence = 25

megaTrack = MidiFile('MidiFiles/MegaTest.mid', clip=True)

#Create all the different notes possible and their translation to CrcDuino
NoteType = []
i = 0
octave = 0
while i < 127 :

    NoteType.append("NOTE_C"+ str(octave))
    NoteType.append("NOTE_CS" + str(octave))
    NoteType.append("NOTE_D" + str(octave))
    NoteType.append("NOTE_DS" + str(octave))
    NoteType.append("NOTE_E" + str(octave))
    NoteType.append("NOTE_F" + str(octave))
    NoteType.append("NOTE_FS" + str(octave))
    NoteType.append("NOTE_G" + str(octave))
    NoteType.append("NOTE_GS" + str(octave))
    NoteType.append("NOTE_A" + str(octave))
    NoteType.append("NOTE_AS" + str(octave))
    NoteType.append("NOTE_B" + str(octave))
    octave += 1
    i += 12

# Initialize a list to store notes
notes = []

# Iterate through the messages in all tracks
for track in megaTrack.tracks:
    for msg in megaTrack:
        # Filter for note_on and note_off messages
        if msg.type == 'note_on' or msg.type == 'note_off':
            if msg.velocity !=0 :
                notes.append(NoteType[int(msg.note)])

for note in notes:
    print(note)
