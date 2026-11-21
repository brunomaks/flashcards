class Word:
    def __init__(self, dict_form, level, freq, trans=None, pos=None):
        self.dict_form = dict_form
        self.level = level
        self.freq = freq
        self.trans = trans
        self.pos = pos

    def serialize(self):
        return f"{self.dict_form}\t{self.level}\t{self.freq}\t{self.trans}"

    @staticmethod
    def deserialize(line):
        dict_form, level, freq, trans = line.rstrip().split("\t")
        return Word(dict_form, level, float(freq), trans)

    def __str__(self):
        return f"{self.dict_form}\t{self.level}\t{self.freq}\t{self.trans}"

