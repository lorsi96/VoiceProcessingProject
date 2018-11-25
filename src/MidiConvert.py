import numpy as np
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


def to_midi2(ev_list):
    # MIDI note number
    track = 0
    channel = 0
    time = 0   # In beats
    duration = 1/16   # In beats
    tempo = 120.0  # In BPM
    volume = 100  # 0-127, as per the MIDI standard
    MyMIDI = MIDIFile(1, deinterleave=True)
    MyMIDI.addTempo(track, time, tempo)
    time = ev_list[0]['duration'] / 0.5
    for element in ev_list:
        duration = element['duration'] / 0.5
        MyMIDI.addNote(
            track, channel, element['pitch'], time, duration, volume)
        time += duration
    with open("./MIDIS/Somethin.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)


def yin_2_midi(freqs, samplesize=2048):
    # Prepare MIDI
    track = 0
    channel = 0
    time = 0   # In beats
    tempo = 60.0  # In BPM
    volume = 100  # 0-127, as per the MIDI standard
    MyMIDI = MIDIFile(1, deinterleave=True)
    MyMIDI.addTempo(track, time, tempo)

    # Parse
    midi_freqs = [int(round(12*np.log2(a/440) + 69))
                  if a > 0 else 0 for a in freqs]
    note_ringing = 0
    time_start = 0
    for ind, val in enumerate(midi_freqs):
        print(note_ringing)
        if note_ringing == 0:
            if val:
                note_ringing = val
                time_start = time
            else:
                pass
        else:
            if val:
                if val == note_ringing:
                    pass
                else:
                    pass
                    # MyMIDI.addNote(track, channel, note_ringing,
                    #               time, time-time_start, volume)
                    #note_ringing = val
                    #time_start = time
                    #note_ringing = val
                    #wheel = int(np.log2(val/note_ringing)*4096*12)
                    # if 0:  # np.abs(wheel) < 8192:
                    #    MyMIDI.addPitchWheelEvent(track, channel, time, wheel)
                    # else:
                    #    pass
            else:
                print(time-time_start)
                print(note_ringing)
                MyMIDI.addNote(track, channel, note_ringing,
                               time, time-time_start, volume)
                note_ringing = time_start = 0
        time = samplesize/48000*ind

    with open("./MIDIS/New.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
