#Class for the Rest
class Rest:
    def __init__(self, name, octave, duration, beat, measure):
        self.name = name
        #duration of the Rest
        self.octave = octave
        self.duration = duration
        self.beat = beat
        self.measure = measure

    def info_rest(self):
        info = []
        info.append(self.name)
        info.append(self.duration)
        info.append(self.beat)
        info.append(self.measure)
        return info

