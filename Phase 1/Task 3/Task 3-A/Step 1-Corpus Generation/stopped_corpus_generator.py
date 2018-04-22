# Import libraries
import os

# File paths for Corpus and stop words
STOP_WORDS_REPO = "common_words"
INPUT_FOLDER = os.getcwd() + "/" + "Corpus"
OUTPUT_FOLDER = os.getcwd() + "/" + "Stop_Corpus"

def corpus_generator():
    # Populating the stop words and files from Un-stopped Corpus
    stop_words_list = open(STOP_WORDS_REPO, 'r').read().splitlines()
    file_list = os.listdir(INPUT_FOLDER)

    # Create the Corpus folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Parse the files to remove the stop words and write the reduced corpus to output folder
    for file in file_list:
        content = open(INPUT_FOLDER + "/" + file, "r").read().split()
        # Filtering out the non-stop words
        stopped_corpus_words = [x for x in content if x not in stop_words_list]
        fd = open(OUTPUT_FOLDER + "/" + file, "w")
        fd.write(" ".join(stopped_corpus_words))
        fd.close()

corpus_generator()