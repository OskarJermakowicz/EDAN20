import sys, codecs, time, math
import regex as re

# Returns a list of 3 elements: The word_count dict, the normalized text and list of words
def tokenize(file_name):
    result = []
    # word_count is essentially a representation of unigrams
    word_count = {}
    new_text = ""

    # Open the corpus
    with codecs.open(file_name, 'r', 'utf-8') as f:
        text = f.read()
        # Go through each sentence
        pattern = '((\s)?+[^.!?]*[.!?])'
        regex = re.compile(pattern, re.IGNORECASE | re.U)
        for sentence in regex.finditer(text):
            new_text += "<s> "
            new_text += sentence.group(1).replace('.', ' ').replace('\n', '').lower()
            new_text += " </s>\n"

            # Also add sentence tags to word_count
            if "<s>" and "</s>" not in word_count:
                word_count["<s>"] = 1
                word_count["</s>"] = 1
            else:
                word_count["<s>"] += 1
                word_count["</s>"] += 1

            # Also go through the words in the sentence.
            pattern = '(\p{L}+)'
            regex = re.compile(pattern, re.IGNORECASE | re.U)
            for word in regex.finditer(sentence.group(1)):
                if word.group(1).lower() in word_count:
                    word_count[word.group(1).lower()] += 1
                else:
                    word_count[word.group(1).lower()] = 1
        result.append(word_count)
        result.append(new_text)
        result.append(new_text.split())

    return result

# Based on count_bigrams.py from https://github.com/pnugues/ilppp/tree/master/programs/ch05/python
def count_bigrams(words):
    bigrams = [tuple(words[inx:inx + 2])
               for inx in range(len(words) - 1)]
    frequencies = {}
    for bigram in bigrams:
        if bigram in frequencies:
            frequencies[bigram] += 1
        else:
            frequencies[bigram] = 1
    return frequencies

# Based on count_ngrams.py from https://github.com/pnugues/ilppp/tree/master/programs/ch05/python
def count_ngrams(words, n):
    ngrams = [tuple(words[inx:inx + n])
              for inx in range(len(words) - n + 1)]
    # "\t".join(words[inx:inx + n])
    frequencies = {}
    for ngram in ngrams:
        if ngram in frequencies:
            frequencies[ngram] += 1
        else:
            frequencies[ngram] = 1
    return frequencies

# Performs all calculations such as probabilty etc and prints it as a table
def print_analysis(sentence, word_count, bigrams):
    print("\n--- Analysis of \"", sentence, "\" ---")
    print("Unigrams")
    print("====================================================================")
    print('%-12s%-12s%-12s%-12s' % ("wi", "C(wi)", "#words", "P(wi)"))
    print("====================================================================")
    words = sentence.split()
    prob_unigrams = 1
    entropy_unigrams = 0
    for word in words[1:]:
        prob_unigrams *= word_count[word.lower()] / sum(tok[0].values())
        entropy_unigrams += math.log2(word_count[word.lower()] / sum(tok[0].values()))
        print('%-12s%-12s%-12s%-12s' % (word.lower(), word_count[word.lower()], sum(tok[0].values()), word_count[word.lower()] / sum(tok[0].values())))
    entropy_unigrams *= -1/words[1:].__len__()
    print("====================================================================")
    print("Prob. unigrams:", prob_unigrams, "Entropy rate:", entropy_unigrams, "Perplexity:", "n/a")


    print("\nBigrams")
    print("====================================================================")
    print('%-12s%-12s%-12s%-12s%-12s' % ("wi", "wi+1", "Ci,i+1", "C(i)", "P(wi+1|wi)"))
    print("====================================================================")
    words = sentence.split()
    prob_bigrams = 1
    entropy_bigrams = 0
    index = 0
    for word in words[:-1]:
        bigram_count = 0
        if (word.lower(), words[index + 1].lower()) in bigrams: bigram_count += bigrams[(word.lower(),words[index+1].lower())]
        if (words[index + 1].lower(), word.lower()) in bigrams: bigram_count += bigrams[(words[index+1].lower(),word.lower())]

        if bigram_count == 0:
            prob_bigrams *= word_count[words[index+1].lower()] / sum(tok[0].values())
            entropy_bigrams += math.log2(word_count[words[index+1].lower()] / sum(tok[0].values()))
            print('%-12s%-12s%-12s%-12s*backoff:\t%-12s' % (word.lower(), words[index + 1].lower(), bigram_count, word_count[word.lower()], word_count[words[index+1].lower()] / sum(tok[0].values())))
        else:
            prob_bigrams *= bigram_count/word_count[word.lower()]
            entropy_bigrams += math.log2(bigram_count/word_count[word.lower()])
            print('%-12s%-12s%-12s%-12s%-12s' % (word.lower(), words[index+1].lower(), bigram_count, word_count[word.lower()], bigram_count/word_count[word.lower()]))

        index += 1
    entropy_bigrams *= -1/words[:-1].__len__()
    print("====================================================================")
    print("Prob. bigrams:", prob_bigrams, "Entropy rate:", entropy_bigrams, "Perplexity:", "n/a")

# Prints a certain text to a certain file
def print_to_file(file_name, text):
    with open(file_name, 'w') as f:
        f.write(text)

# Run the program
start_time = time.time()

tok = tokenize(sys.argv[1])
frequency_bigrams = count_bigrams(tok[2])
frequency_fourgrams = count_ngrams(tok[2], 4)

print_to_file('result.txt', tok[1])

print("--- Counting unigrams and bigrams ---")
print("Possible bigrams: ", frequency_bigrams.__len__(), "\tReal number: ", sum(frequency_bigrams.values()))
print("Possible 4-grams: ", frequency_fourgrams.__len__(), "\tReal number: ", sum(frequency_fourgrams.values()))

print_analysis("<s> Det var en gång en katt som hette Nils </s>", tok[0], frequency_bigrams)

print("\n--- Execution time: %s seconds ---" % (time.time() - start_time))