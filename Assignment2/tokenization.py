"""
Usage: python3 tokenization.py file_name.txt
"""

import sys
import codecs
import time
import regex as re

def tokenize(file_name):
    word_count = {}
    new_text = ""

    # Open the corpus
    with codecs.open(file_name, 'r', 'utf-8') as f:
        # Go through each sentence
        pattern = '((\s)?+[^.!?]*[.!?])'
        regex = re.compile(pattern, re.IGNORECASE | re.U)
        for sentence in regex.finditer(f.read()):
            new_text += "<s>"
            new_text += sentence.group(1).replace('.', ' ').replace('\n', '').lower()
            new_text += "</s>\n"

            # Also go through the words in the sentence.
            pattern = '(\p{L}+)'
            regex = re.compile(pattern, re.IGNORECASE | re.U)
            for word in regex.finditer(sentence.group(1)):
                if word.group(1).lower() in word_count:
                    word_count[word.group(1).lower()] += 1
                else:
                    word_count[word.group(1).lower()] = 1

    return [word_count, new_text]

def print_analysis(sentence, word_count):
    print("\nUnigrams - \"", sentence, "\"")
    print("====================================================================")
    print('%-12s%-12s%-12s%-12s' % ("wi", "C(wi)", "#words", "P(wi)"))
    print("====================================================================")
    pattern = '(\p{L}+)'
    regex = re.compile(pattern, re.IGNORECASE | re.U)
    for word in regex.finditer(sentence):
        print('%-12s%-12s%-12s%-12s' % (word.group(1).lower(), word_count[word.group(1).lower()], sum(tok[0].values()), "P(wi)"))
    print("====================================================================")
    print("Prob. unigrams:", "n/a", "Entropy rate:", "n/a", "Perplexity:", "n/a")


    print("\nBigrams - \"", sentence, "\"")
    print("====================================================================")
    print('%-12s%-12s%-12s%-12s%-12s' % ("wi", "wi+1", "Ci,i+1", "C(i)", "P(wi+1|wi)"))
    print("====================================================================")
    pattern = '(\p{L}+)'
    regex = re.compile(pattern, re.IGNORECASE | re.U)
    for word in regex.finditer(sentence):
        print('%-12s%-12s%-12s%-12s%-12s' % (word.group(1).lower(), "wi+1", "Ci,i+1", "C(i)", "P(wi+1|wi)"))
    print("====================================================================")
    print("Prob. bigrams:", "n/a", "Entropy rate:", "n/a", "Perplexity:", "n/a")

# Run the indexing program
start_time = time.time()

tok = tokenize(sys.argv[1])
# Print new text to a file
with open('result.txt', 'w') as f:
    f.write(tok[1])

print("\n--- Number of words in", sys.argv[1], "---")
print(sum(tok[0].values()))

print_analysis("Det var en gång en katt som hette Nils </s>", tok[0])

print("\n--- Execution time: %s seconds ---" % (time.time() - start_time))