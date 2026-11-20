class Word:
    def __init__(self, dict_form, pos, level, freq, trans=None):
        self.dict_form = dict_form
        self.pos = pos
        self.level = level
        self.freq = freq
        self.trans = trans

    def __str__(self):
        return f"({self.level}) {self.pos} {self.dict_form}: {self.trans}"

