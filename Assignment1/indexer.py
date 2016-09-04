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
    # Master index structure: word: { textfile: [pos1,pos2,...] }
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
        master_idf[word] = math.log10(master_tf.__len__()/master_index[word].__len__())


    # Calculate tf-idf and populate master_tfidf
    for f in master_tf:
        master_tfidf[f] = {}
        for word in master_tf[f]:
            master_tfidf[f][word] = (1/master_tf[f][word])*master_idf[word]

    # Test print
    # print(master_index['samlar'])
    # print(master_index['ände'])

    # print(master_tf['nils.txt']['samlar'])

    # print(master_tf.__len__(), master_index['hej'].__len__())
    # print(master_idf['hej'])

    files_to_check = ['bannlyst.txt', 'gosta.txt', 'herrgard.txt', 'jerusalem.txt', 'nils.txt']
    words_to_check = ['känna', 'gås', 'nils', 'et']
    for f in files_to_check:
        print(f)
        for word in words_to_check:
            if word in master_tfidf[f]:
                print("\t", word, master_tfidf[f][word])
            else:
                print("\t", word, 0.0)



# Run the indexing program
program(sys.argv[1])