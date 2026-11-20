import csv
import xml.etree.ElementTree as ET

from Word import Word

LEVELS = ("a1", "a2", "b1", "b2", "c1")

def first_level(row):
    """Return the first CEFR level where the word appears"""
    for level in LEVELS:
        if float(row[f"level_freq@{level}"]) > 0:
            return level.upper()
    return None

def load_svalex(path):
    words = []
    pos_tags = set()
    empty_pos = 0

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="\t")

        for row in reader:
            tag = row["tag"]

            pos_tags.add(tag)

            if not tag:
                empty_pos += 1

            words.append(
                Word(
                    row["word"],
                    tag,
                    first_level(row),
                    row["total_freq@total"],
                )
            )

    return words, pos_tags, empty_pos


def load_folkets(path):
    translations = {}
    pos_tags = set()
    empty_pos = 0

    root = ET.parse(path).getroot()

    for word in root:
        lemma = word.get("value")
        pos = word.get("class")

        pos_tags.add(pos)

        if not pos:
            empty_pos += 1

        translations[lemma] = [
            child.get("value")
            for child in word
            if child.tag == "translation"
        ]

    return translations, pos_tags, empty_pos

def svalex_to_folkets(tag):
    """Convert SVALex POS tags to Folkets POS tags."""
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
    words, svalex_pos, svalex_empty = load_svalex("data/svalex.tsv")
    dictionary, folkets_pos, folkets_empty = load_folkets(
        "data/folkets_sv_en_public.xml"
    )

    missing = 0

    for word in words:
        translation = dictionary.get(word.dict_form)

        if translation:
            word.trans = translation
        else:
            missing += 1

    print(f"Loaded {len(words)} words.")
    print(f"Missing translations: {missing}")
    print(f"SVALex empty POS tags: {svalex_empty}")
    print(f"Folkets empty POS tags: {folkets_empty}")