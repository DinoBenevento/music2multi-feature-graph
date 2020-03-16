# A class for the Chord
class Chord:
    def __init__(self, notes, duration, beat, measure):
        # notes played in the chord
        self.notes = notes
        # duration of the chord
        self.duration = duration
        # beat in witch the chord is played
        self.beat = beat
        self.measure = measure

    def info_chord(self):
        info = []
        info.append(self.notes)
        info.append(self.duration)
        info.append(self.beat)
        info.append(self.measure)
        return info

