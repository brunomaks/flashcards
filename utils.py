from Word import Word

def serialize(words, path):
    with open(path, "w", encoding="utf-8") as f:
        for word in words:
            f.write(word.serialize() + '\n')

def deserialize(path):
    words = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            words.append(Word.deserialize(line))

    return words
