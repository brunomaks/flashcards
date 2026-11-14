# Question: Is parsing strategy graded? What if I do this wrong?
import csv, xml.etree.ElementTree
from Word import Word

levels = ['a1', 'a2', 'b1', 'b2', 'c1']
with open('data/svalex.tsv', newline='') as csv_file:
    reader = csv.DictReader(csv_file, delimiter='\t')

    for row in reader:
        print("Word:", row['word'])
        # Total frequency across all books with different levels is taken
        print("Total_freq:", row['total_freq@total'])
        # Level is assigned based on the first appearance
        first_level = None
        for level in levels:
            if float(row[f'level_freq@{level}']) > 0:
                first_level = level.upper()
                break
        print("First_level:", first_level.upper())

word = Word('test', 'test', 'test', None)
