import csv
import xml.etree.ElementTree as ET

from Word import Word
import utils

LEVELS = ("a1", "a2", "b1", "b2", "c1")

def first_level(row):
    """Return the first CEFR level where the word appears"""
    for level in LEVELS:
        if float(row[f"level_freq@{level}"]) > 0:
            return level.upper()
    return None

def load_svalex(path):
    words = []
    empty_pos = 0

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="\t")

        for row in reader:
            tag = row["tag"]

            if not tag:
                empty_pos += 1

            words.append(
                Word(
                    dict_form=row["word"],
                    pos=tag,
                    level=first_level(row),
                    freq=row["total_freq@total"],
                )
            )

    return words, empty_pos


def load_folkets(path):
    translations = {}
    empty_pos = 0

    root = ET.parse(path).getroot()

    for word in root:
        lemma = word.get("value")
        pos = word.get("class")

        if not pos:
            empty_pos += 1

        translation = None

        for child in word:
            if child.tag == "translation":
                translation = child.get("value")
                break

        translations[lemma] = (translation, pos)

    return translations, empty_pos

def svalex_to_folkets(tag):
    if not tag:
        return None

    tag = tag.removesuffix("_MWE")

    mapping = {
        "NN": "nn",
        "NN_UTR": "nn",
        "NN_NEU": "nn",
        "NNM_UTR": "nn",
        "VB": "vb",
        "VBM": "vb",
        "vB": "vb",
        "JJ": "jj",
        "JJM": "jj",
        "AB": "ab",
        "ABM": "ab",
        "PN": "pn",
        "PNM": "pn",
        "PP": "pp",
        "PPM": "pp",
        "KN": "kn",
        "KNM": "kn",
        "SN": "sn",
        "SNM": "sn",
        "RG": "rg",
        "IE": "ie",
        "PMM": "pm",
        "HP": "hp",
    }

    return mapping.get(tag)


if __name__ == "__main__":
    words, svalex_empty = load_svalex("data/svalex.tsv")

    # Remove words with no level
    words = [w for w in words if w.level]

    dictionary, folkets_empty = load_folkets(
        "data/folkets_sv_en_public.xml"
    )

    missing = 0
    pos_mismatches = 0

    # Step 1: Add translations to words
    for word in words:
        # folkets has words like 'akta sig' while svalex 'akta_sig'
        df_no_underscore = word.dict_form.replace("_", " ")
        dict_entry = dictionary.get(df_no_underscore)

        if dict_entry:
            translation, translation_pos = dict_entry
            if svalex_to_folkets(word.pos) == translation_pos:
                word.trans = translation
            else:
                pos_mismatches += 1
        else:
            missing += 1

    print(f"Loaded {len(words)} words")
    print(f"Missing translations: {missing}")
    print(f"POS mismatches: {pos_mismatches}")
    print(f"SVALex empty POS tags: {svalex_empty}")
    print(f"Folkets empty POS tags: {folkets_empty}")

    # Step 2: Remove words with no translations
    unknown_word_indices = []
    for i in range(len(words)):
        translation = words[i].trans
        if not translation:
            unknown_word_indices.append(i)

    for index in reversed(unknown_word_indices):
        words.pop(index)

    print(f"Words with no translation removed: {len(unknown_word_indices)}")

    # Step 3: Remove the same words that appear at different levels
    words_dict = {}
    for i in range(len(words)):
        # Key must account for translation 
        # otherwise we risk removing different words with the same spelling
        key = (words[i].dict_form, words[i].trans)
        words_dict.setdefault(key, []).append(i)

    duplicates = {
        word: indices 
        for word, indices in words_dict.items() 
        if len(indices) > 1
    }

    # Keep the lowest level at which the word appears
    def level2num(level):
        levels = {
            "A1": 1,
            "A2": 2,
            "B1": 3,
            "B2": 4,
            "C1": 5,
        }
        return levels[level]

    remove_indices = []

    for word, indices in duplicates.items():
        # Find the index with the lowest CEFR level
        keep_index = min(
            indices,
            key=lambda i: level2num(words[i].level)
        )

        # Mark all others for removal
        for index in indices:
            if index != keep_index:
                remove_indices.append(index)

    # Remove from the end so indices stay valid
    for index in sorted(remove_indices, reverse=True):
        words.pop(index)

    print(f"Duplicates removed: {len(remove_indices)}")

    print(f"Valid words left in total: {len(words)}")

    utils.serialize(words, "words.tsv")

    new_words = utils.deserialize("words.tsv")
    for word in new_words:
        print(word)

    print(len(new_words))
