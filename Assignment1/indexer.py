import sys
import pickle
import re
import os
import codecs

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

    for file_name in get_files(dir, 'txt'):
        # Import the file to index
        fi = dir + "/" + file_name
        with codecs.open(fi, 'r', 'utf-8') as f:
            pattern = '([åäöÅÄÖA-Za-z_]+)'
            regex = re.compile(pattern, re.IGNORECASE | re.U)
            for match in regex.finditer(f.read()):
                if match.group(1).lower() in master_index:
                    if file_name in master_index[match.group(1).lower()]:
                        master_index[match.group(1).lower()][file_name].append(match.start())
                    else:
                        master_index[match.group(1).lower()][file_name] = [match.start()]
                else:
                    master_index[match.group(1).lower()] = { file_name: [match.start()] }

            # Save the indexing to a idx file
            with open('file_name.idx', 'w') as f:
                f.write(str(master_index))
                # pickle.dump(str(master_index), f)

    # Test print
    print(master_index['samlar'])
    print(master_index['ände'])

# Run the indexing program
program(sys.argv[1])



