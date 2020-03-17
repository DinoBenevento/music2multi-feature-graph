

'''
Dictory settings mapping every notes, note's duration, note's octave.
'''

def create_notes_dictionary():
    dicts = []
    DictNotes = {'C': 1, 'C#': 2, 'D-': 3, 'D': 4, 'D#': 5, 'E-': 6, 'E': 7, 'F': 8, 'F#': 9, 'G-': 10, 'G': 11, 'G#': 12, 'A': 13, 'A-': 14, 'A#': 15, 'B-': 16, 'B': 17, 'Rest': 0, 'Mute': -1, 'E#': 18, 'B#': 19}
    DictDuration = {4.0: 1, 3.5: 2, 3.0: 3, 2.5: 4, 2.0: 5, 1.5: 6, 1.0: 7, 0.5: 8, 0.25: 9, 6.0: 10, 7.0: 11, 1.75: 12, 0.75: 13, 0.875: 14, 0.375: 15, 0.4375: 16}
    DictInterval = {'P1': 0, 'm2': 1, 'A1': 2, 'M2': 3, 'd3': -3, 'm3': 5, 'A2': 6, 'M3': 7, 'd4': 8, 'P4': 9, 'A3': 10, 'd5': 11, 'A4': 12, 'P5': 13, 'd6': 14, 'm6': 15, 'A5': 16, 'M6': 17, 'd7': 18, 'm7': 19, 'A6': 20, 'M7': 21, 'D8': 22, 'P8': 23, 'A7': 24, 'd1': -1}
    DictOctave = {0: 0.0, 1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4, 5: 0.5, 6: 0.6, 7: 0.7, 8: 0.8}
    dicts.append(DictNotes)
    dicts.append(DictDuration)
    dicts.append(DictInterval)
    dicts.append(DictOctave)
    return dicts