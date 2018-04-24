# Import libraries
import os
import re

# File paths for indexed corpus file and the output folder
INPUT_FILE = os.getcwd() + "/" + "cacm_stem.txt"
OUTPUT_FOLDER = os.getcwd() + "/" + "Stemmed_Corpus"

def corpus_generator():
    # Create the Stemmed Corpus folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Read the contents of the file based on regular expression
    corpus = open(INPUT_FILE, "r").read()
    files = re.split("# [\d]+",corpus)
    files = [w for w in files if w != ""]

    # Write the contents into separate files
    for ID,file_content in enumerate(files,1):
        #print("Creating Stemmed Corpus file for CACM-" + str(ID))
        id = str(ID)
        f = open(OUTPUT_FOLDER + "/" + 'CACM-' + id.rjust(4, '0') + '.txt', 'w', encoding='utf-8')
        result_text = file_content.strip()

        # ignoring random numbers at the end of document
        index_of_am = result_text.rfind("am")  # finds the last index of the term "am"
        index_of_pm = result_text.rfind("pm")  # finds the last index of the term "pm"

        # retain the text content until am or pm in the corpus documents
        if index_of_am > index_of_pm:
            greater_index = index_of_am
        else:
            greater_index = index_of_pm
        result = result_text[:(greater_index + 2)]

        f.write(result)
        f.close()

corpus_generator()