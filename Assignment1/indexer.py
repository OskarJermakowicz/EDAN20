import sys
import pickle
import re
import os

# Gets a list of all files with a certain suffix in a certain folder
def get_files(dir, suffix):
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files

# The program that will be run
def program(dir):
    for file_name in get_files(dir, 'txt'):
        # Dictionary where the indexing will be stored
        index_dict = {}

        # Import the file to index
        fi = dir + "/" + file_name
        with open(fi) as f:
            pattern = '([a-zA-Z]+\w+)'
            regex = re.compile(pattern, re.IGNORECASE)
            for match in regex.finditer(f.read()):
                if match.group(1).lower() in index_dict:
                    index_dict[match.group(1).lower()].append(match.start())
                else:
                    index_dict[match.group(1).lower()] = [match.start()]

            # Save the indexing to a idx file
            with open('file_name.idx', 'w') as f:
                f.write(str(index_dict))
                # pickle.dump(str(index_dict), f)

            # Test print
            print(index_dict)

# Run the indexing program
program(sys.argv[1])



