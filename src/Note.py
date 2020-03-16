class Note:

    def __init__(self, name, octave, duration, beat, interval, measure):
        # name of the note
        self.name = name
        self.octave = octave
        # duration of the note
        self.duration = duration
        # beat in witch the note is played
        self.beat = beat
        # interval of the note with the previuos one note
        self.interval = interval
        self.measure = measure

    def info_note(self):
        # a list with the info of the note
        info = []
        info.append(self.name)
        info.append(self.duration)
        info.append(self.beat)
        info.append(self.interval)
        info.append(self.measure)
        return info

