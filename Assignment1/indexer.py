import sys
import pickle
import re
import os
import codecs
import math

# Gets a list of all files with a certain suffix in a certain folder
def get_files(dir, suffix):
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files

# The program that will be run
def program(dir):
    master_index = {}
    master_tf = {}
    master_idf = {}
    master_tfidf = {}

    for file_name in get_files(dir, 'txt'):
        # Import the file to index
        fi = dir + "/" + file_name
        with codecs.open(fi, 'r', 'utf-8') as f:
            pattern = '([åäöÅÄÖA-Za-z_]+)'
            regex = re.compile(pattern, re.IGNORECASE | re.U)
            for match in regex.finditer(f.read()):
                # Populate master_index
                if match.group(1).lower() in master_index:
                    if file_name in master_index[match.group(1).lower()]:
                        master_index[match.group(1).lower()][file_name].append(match.start())
                    else:
                        master_index[match.group(1).lower()][file_name] = [match.start()]
                else:
                    master_index[match.group(1).lower()] = { file_name: [match.start()] }

                # Populate master_tf
                if file_name in master_tf:
                    if match.group(1).lower() in master_tf[file_name]:
                        master_tf[file_name][match.group(1).lower()] += 1
                    else:
                        master_tf[file_name][match.group(1).lower()] = 1
                else:
                    master_tf[file_name] = { match.group(1).lower(): 1 }

            # Save the indexing to an .idx file
            with open('file_name.idx', 'w') as f:
                f.write(str(master_index))
                # pickle.dump(str(master_index), f)

    # Calculate idf
    for word in master_index:
        master_idf[word] = math.log(master_tf.__len__()/master_index[word].__len__(), math.e)

    # Calculate tf-idf and populate master_tfidf
    for f in master_tf:
        master_tfidf[f] = {}
        for word in master_index:
            if word in master_tf[f]:
                master_tfidf[f][word] = (1/master_tf[f][word])*master_idf[word]
            else:
                master_tfidf[f][word] = 0.0

    # Compare similarity of documents, using cosine similarity
    cos_matrix = {}
    for f in master_tfidf:
        for f_compare in master_tfidf:
            dot_product = 0
            abs_doc1 = 0
            abs_doc2 = 0

            for word in master_tfidf[f]:
                dot_product += master_tfidf[f][word] * master_tfidf[f_compare][word]
                abs_doc1 += master_tfidf[f][word]**2
                abs_doc2 += master_tfidf[f_compare][word]**2

            cos_matrix[f, f_compare] = dot_product/(math.sqrt(abs_doc1) * math.sqrt(abs_doc2))

    ###### Test print ######
    # print(master_index['samlar'])
    # print(master_index['ände'])

    # print(master_tf['nils.txt']['samlar'])

    # print(master_tf.__len__(), master_index['hej'].__len__())
    # print(master_idf['hej'])

    # Prints the document representation of tf-idf
    files_to_check = ['bannlyst.txt', 'gosta.txt', 'herrgard.txt', 'jerusalem.txt', 'nils.txt']
    words_to_check = ['känna', 'gås', 'nils', 'et']
    for f in files_to_check:
        print(f)
        for word in words_to_check:
            print("\t", word, master_tfidf[f][word])

    # Prints the cosine simliarity matrix
    print("\n-- Similarities between two documents: --")
    for f in master_tfidf:
        for f_compare in master_tfidf:
            print(f, "\t\t", f_compare, "\t\t", cos_matrix[f,f_compare])
        print()

    print(cos_matrix)

# Run the indexing program
program(sys.argv[1])