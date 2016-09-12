import sys, codecs, time, math
import regex as re

# Returns a tuple: The word_count dict and the normalized text
def tokenize(file_name):
    word_count = {}
    new_text = ""

    # Open the corpus
    with codecs.open(file_name, 'r', 'utf-8') as f:
        # Go through each sentence
        sentence_regex = re.compile('((\s)?+[^.!?]*[.!?])', re.IGNORECASE | re.U)
        for sentence in sentence_regex.finditer(f.read()):
            # Add sentence tags to new_text and word_count
            new_text += ''.join(["<s>", sentence.group(1).replace('\n', ' ').lower(), " </s>\n"])

            if "<s>" and "</s>" not in word_count:
                word_count["<s>"] = word_count["</s>"] = 1
            else:
                word_count["<s>"] += 1
                word_count["</s>"] += 1

            # Also go through the words in the sentence.
            word_regex = re.compile('(\p{L}+)', re.IGNORECASE | re.U)
            for word in word_regex.finditer(sentence.group(1)):
                if word.group(1).lower() in word_count: word_count[word.group(1).lower()] += 1
                else: word_count[word.group(1).lower()] = 1

        # Complete the normalization of new_text
        for punctuation in ['.', ',', '!', '?', ':', ';', '"', '\'']:
            new_text = new_text.replace(punctuation, '')
        new_text = new_text.replace('  ', ' ')

    return [word_count, new_text]

# Based on count_ngrams.py from https://github.com/pnugues/ilppp/tree/master/programs/ch05/python
def count_ngrams(words, n):
    ngrams = [tuple(words[inx:inx + n]) for inx in range(len(words) - n + 1)]
    frequencies = {}
    for ngram in ngrams:
        if ngram in frequencies: frequencies[ngram] += 1
        else: frequencies[ngram] = 1
    return frequencies

# Performs all calculations such as probabilty etc and prints it as a table
def print_analysis(sentence, word_count, bigrams):
    print(''.join(["\n--- Analysis of \"", sentence[4:-5], "\" ---"]))
    print("\nUnigrams")
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
    print('Prob. unigrams: %s Entropy rate: %s Perplexity: %s' % (prob_unigrams, entropy_unigrams, 2**entropy_unigrams))

    print("\nBigrams")
    print("====================================================================")
    print('%-12s%-12s%-12s%-12s%-12s' % ("wi", "wi+1", "Ci,i+1", "C(i)", "P(wi+1|wi)"))
    print("====================================================================")
    words = sentence.split()
    prob_bigrams = 1
    entropy_bigrams = 0
    index = 0
    for word in words[:-1]:
        if (word.lower(), words[index + 1].lower()) not in bigrams:
            prob_bigrams *= word_count[words[index+1].lower()] / sum(tok[0].values())
            entropy_bigrams += math.log2(word_count[words[index+1].lower()] / sum(tok[0].values()))
            print('%-12s%-12s%-12s%-12s*backoff:\t%-12s' % (word.lower(), words[index + 1].lower(), 0, word_count[word.lower()], word_count[words[index+1].lower()] / sum(tok[0].values())))
        else:
            prob_bigrams *= bigrams[word.lower(), words[index+1].lower()]/word_count[word.lower()]
            entropy_bigrams += math.log2(bigrams[word.lower(), words[index+1].lower()]/word_count[word.lower()])
            print('%-12s%-12s%-12s%-12s%-12s' % (word.lower(), words[index+1].lower(), bigrams[word.lower(), words[index+1].lower()], word_count[word.lower()], bigrams[word.lower(), words[index+1].lower()]/word_count[word.lower()]))

        index += 1
    entropy_bigrams *= -1/words[:-1].__len__()
    print("====================================================================")
    print('Prob. bigrams: %s Entropy rate: %s Perplexity: %s' % (prob_bigrams, entropy_bigrams, 2 ** entropy_bigrams))

# Run the program
start_time = time.time()

tok = tokenize(sys.argv[1])
frequency_bigrams = count_ngrams(tok[1].split(), 2)
frequency_fourgrams = count_ngrams(tok[1].split(), 4)

with open('result.txt', 'w') as f: f.write(tok[1])

print("--- Counting unigrams and bigrams ---")
print("Amount of bigrams: %s \t Possible amount of bigrams: %s" % (frequency_bigrams.__len__(), tok[0].__len__()**2))
print("Amount of 4-grams: %s \t Possible amount of 4-grams: %s" % (frequency_fourgrams.__len__(), tok[0].__len__()**4))

# Assignment example
print_analysis("<s> Det var en gång en katt som hette Nils </s>", tok[0], frequency_bigrams)

# My examples
#print_analysis("<s> Ett par dar senare tilldrog sig ännu en sådan där besynnerlig händelse </s>", tok[0], frequency_bigrams)
#print_analysis("<s> Akka gav därmed tecken till uppbrott </s>", tok[0], frequency_bigrams)
#print_analysis("<s> Det var den första regndagen under resan </s>", tok[0], frequency_bigrams)
#print_analysis("<s> Men på samma gång har det uppkommit en stor skillnad mellan de tre trappstegen </s>", tok[0], frequency_bigrams)
#print_analysis("<s> Han behövde inte berätta mer </s>", tok[0], frequency_bigrams)

print("\n--- Execution time: %s seconds ---" % (time.time() - start_time))