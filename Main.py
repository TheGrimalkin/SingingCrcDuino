import mido
from mido import MidiFile, Message, tick2second


#Format for Crc songs {duration, NOTE_(note)}
#Note notes[] = { #{ 250, NOTE_B4 }, { 500, NOTE_F5 },# Note::END };

class NOTE:
    def __init__(self):
        self.noteType = "$$"
        self.time = 0 #in ms
        self.endSilence = 0

class TRACK:
    def __init__(self):
        self.name = "UNDEFINED"
        self.notes = []
        self.key = "C or UNDEFINED"
        self.starting_time = 0

midi_file = MidiFile()
name_of_file = "UNDEFINED"
while name_of_file == "UNDEFINED":
    name_of_file = str(input("Enter the name of the file: "))
    if name_of_file[-4:] != ".mid":
        name_of_file+= ".mid"
    try:
        midi_file = MidiFile(f'MidiFiles/{name_of_file}', clip=True)
    except:
        print("ERROR : file not found")
        name_of_file = "UNDEFINED"
        continue

tempo = 120     #baseValue, will get it later when cycling through msgs
ticks_per_beat = midi_file.ticks_per_beat
def tick_to_seconds(ticks):
   return  round(tick2second(ticks,ticks_per_beat,tempo)*1000)

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

# Will save all the different tracks and their notes
tracks_list = []

# Iterate through all the tracks
for track in midi_file.tracks:
    #print("NEWTRACK")
    newTRACK = TRACK()
    previousNOTE = NOTE()       #to add the EndSilence
    #print(len(newTRACK.notes))
    for msg in track:
        #print("1")
        # Filter different msg types
        if msg.type == 'set_tempo':
            tempo = msg.tempo
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0): #0 velocity = stop sound
            previousNOTE.time = tick_to_seconds(msg.time)
        elif msg.type == 'note_on':
            if len(newTRACK.notes) == 0:
                newTRACK.starting_time = tick_to_seconds(msg.time)
            newNOTE = NOTE()
            newNOTE.noteType = NoteType[msg.note]
            previousNOTE.endSilence = tick_to_seconds(msg.time)
            previousNOTE = newNOTE  #Est-ce que c'est un pointer ?
            newTRACK.notes.append(newNOTE) #Est-ce que c'est un pointer ?
        elif msg.type == 'track_name':
            newTRACK.name = msg.name
    tracks_list.append(newTRACK)


new_song_file = open("Songs/Testt.txt", mode='w')
new_song_file.write('\n'+ '**** New Song ****' + '\n\n' )
i = 0
for _track in tracks_list:
    new_song_file.write('Track number ' + str(i) + ' : ' + _track.name + '\n')
    new_song_file.write('Note notes[] = { ')
    if _track.starting_time != 0:
        new_song_file.write('{'+str(_track.starting_time) + ',NOTE_SILENCE},')
    for _note in _track.notes:
        new_song_file.write('{' + str(_note.time) + ',' + _note.noteType + '},')
        if _note.endSilence > 0:
            new_song_file.write('{' + str(_note.endSilence) + ',NOTE_SILENCE},')
    new_song_file.write(' Note::END };' +'\n')
    i+=1

midi_file.print_tracks()