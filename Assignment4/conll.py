"""
CoNLL-X and CoNLL-U file readers and writers
"""
__author__ = "Pierre Nugues"

import os, time, codecs


def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    Recursive version
    :param dir:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        path = dir + '/' + file
        if os.path.isdir(path):
            files += get_files(path, suffix)
        elif os.path.isfile(path) and file.endswith(suffix):
            files.append(path)
    return files


def read_sentences(file):
    """
    Creates a list of sentences from the corpus
    Each sentence is a string
    :param file:
    :return:
    """
    with codecs.open(file, 'r', 'utf-8') as f:
        content = f.read().strip()
        sentences = content.split('\n\n')
    return sentences


def split_rows(sentences, column_names):
    """
    Creates a list of sentence where each sentence is a list of lines
    Each line is a dictionary of columns
    :param sentences:
    :param column_names:
    :return:
    """
    new_sentences = []
    root_values = ['0', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', '0', 'ROOT', '0', 'ROOT']
    start = [dict(zip(column_names, root_values))]
    for sentence in sentences:
        rows = sentence.split('\n')
        sentence = [dict(zip(column_names, row.split())) for row in rows if row[0] != '#']
        sentence = start + sentence
        new_sentences.append(sentence)
    return new_sentences


def save(file, formatted_corpus, column_names):
    f_out = open(file, 'w')
    for sentence in formatted_corpus:
        for row in sentence[1:]:
            # print(row, flush=True)
            for col in column_names[:-1]:
                if col in row:
                    f_out.write(row[col] + '\t')
                else:
                    f_out.write('_\t')
            col = column_names[-1]
            if col in row:
                f_out.write(row[col] + '\n')
            else:
                f_out.write('_\n')
        f_out.write('\n')
    f_out.close()

def find_ssvb_pairs(formatted_corpus):
    # Key: tuple of the pair, Value: how many times it occurs
    rep = {}

    for sentence in formatted_corpus:
        for word in sentence:
            if word['deprel'] == 'SS':
                subject = word['form'].lower()
                verb = sentence[int(word['head'])]['form'].lower()
                if (subject, verb) not in rep:
                    rep[(subject, verb)] = 1
                else:
                    rep[(subject, verb)] += 1
    return rep

def find_ssvbobj_triples(formatted_corpus):
    # Key: tuple of the triple, Value: how many times it occurs
    rep = {}

    for sentence in formatted_corpus:
        for word in sentence:
            if word['deprel'] == 'SS':
                subject = word['form'].lower()
                verb = sentence[int(word['head'])]['form'].lower()

                for pobj in sentence:
                    if pobj['deprel'] == 'OO' and pobj['head'] == word['head']:
                        object = pobj['form'].lower()
                        if (subject, verb, object) not in rep:
                            rep[(subject, verb, object)] = 1
                        else:
                            rep[(subject, verb, object)] += 1

    return rep



if __name__ == '__main__':
    start_time = time.time()
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']

    train_file = 'swedish_talbanken05_train.conll'
    # train_file = 'test_x'
    test_file = 'swedish_talbanken05_test.conll'

    sentences = read_sentences(train_file)
    formatted_corpus = split_rows(sentences, column_names_2006)
    print(train_file, len(formatted_corpus))
    print(formatted_corpus[15])

    ssvb_pairs = find_ssvb_pairs(formatted_corpus)
    print("\n--- Total amount of pairs ---")
    print(sum(ssvb_pairs.values()))

    print("\n--- Five most common subject-verb pairs ---")
    for pair in sorted(ssvb_pairs, key=ssvb_pairs.get, reverse=True)[:5]:
        print(ssvb_pairs[pair], "\t", pair[0], pair[1])

    ssvbobj_triples = find_ssvbobj_triples(formatted_corpus)
    print("\n--- Total amount of triples ---")
    print(sum(ssvbobj_triples.values()))

    print("\n--- Five most common subject-verb-object triples ---")
    for triple in sorted(ssvbobj_triples, key=ssvbobj_triples.get, reverse=True)[:5]:
        print(ssvbobj_triples[triple], "\t", triple[0], triple[1], triple[2])

    print("\n--- Execution time: %s seconds ---" % (time.time() - start_time))