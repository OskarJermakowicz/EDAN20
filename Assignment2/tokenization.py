"""
Usage: python3 tokenization.py file_name.txt
"""

import sys
import codecs
import time
import regex as re

# The program that will be run
def program(file_name):
    word_count = 0
    new_text = ""

    # Open the corpus
    with codecs.open(file_name, 'r', 'utf-8') as f:
        # Go through each sentence
        pattern = '((\s)?+[^.!?]*[.!?])'
        regex = re.compile(pattern, re.IGNORECASE | re.U)
        for sentence_match in regex.finditer(f.read()):
            new_text += "<s>"
            new_text += sentence_match.group(1).replace('.', ' ').replace('\n', '').lower()
            new_text += "</s>\n"

            # Also go through the words in the sentence.
            pattern = '(\p{L}+)'
            regex = re.compile(pattern, re.IGNORECASE | re.U)
            for word_match in regex.finditer(sentence_match.group(1)):
                word_count += 1



    # Print new text to a file
    with open('result.txt', 'w') as f:
        f.write(new_text)

    """ Test prints """
    print("\n--- Number of words ---")
    print(word_count)

# Run the indexing program
start_time = time.time()
program(sys.argv[1])
print("\n--- Execution time: %s seconds ---" % (time.time() - start_time))