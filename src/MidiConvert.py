from midiutil import MIDIFile


def to_midi(midinotes):
    degrees = midinotes  # MIDI note number
    track = 0
    channel = 0
    time = 0   # In beats
    duration = 1/16   # In beats
    tempo = 190.0  # In BPM
    volume = 100  # 0-127, as per the MIDI standard

    # One track, defaults to format 1 (tempo track
    MyMIDI = MIDIFile(1, deinterleave=True)
    # automatically created)
    last_p = 0
    MyMIDI.addTempo(track, time, tempo)
    for index, pitch in enumerate(degrees):
        if 0:  # pitch == last_p:
            duration += 1/16
        else:
            MyMIDI.addNote(track, channel, pitch, time, duration, volume)
            time += duration
            duration = 1/16
        last_p = pitch

    with open("./MIDIS/Test.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
