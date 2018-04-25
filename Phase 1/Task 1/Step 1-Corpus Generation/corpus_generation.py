import os.path as path
import os
from bs4 import BeautifulSoup
import re


# remove punctuations from text and unnecessary ones from digit sequences
def handle_punctuations(content):
    result = re.sub(r"[^0-9A-Za-z,-\.:\\$]"," ",str(content))  # retain alpha-numeric text along with ',',':' and '.'
    result = re.sub(r"(?!\d)[$,%,:.,-](?!\d)", " ", str(result), 0)  # retain '.', '-' or ',' between digits
    result = result.split()
    result_text = ' '.join(result)
    # ignoring random numbers at the end of document
    index_of_am = result_text.rfind("am")  # finds the last index of the term "am"
    index_of_pm = result_text.rfind("pm")  # finds the last index of the term "pm"

    # retain the text content until am or pm in the corpus documents
    if index_of_am > index_of_pm:
        greater_index = index_of_am
    else:
        greater_index = index_of_pm
    result = result_text[:(greater_index + 2)]

    return result


# handle case folding and punctuations
def cleanup(content, case_folding, punc_handling):
    result = content
    # perform case folding if wanted by the user
    if case_folding:
        result = result.lower()
    # handle punctuations if wanted by the user
    if punc_handling:
        result = handle_punctuations(result)
    return result


def generate_corpus(case_folding,punc_handling):
    # loop for every file in the folder
    paths = path.abspath(path.join(os.getcwd(), "../../../"))
    paths = os.path.join(paths, "htmldocs")
    for file in os.listdir(paths):
        filename = os.path.join(paths,file)
        f = open(filename, 'r', encoding='utf-8')
        html = f.read()
        f.close()
        # fetching the soup object
        soup = BeautifulSoup(html, "html.parser")
        # fetching the content from html tag as there are only tags html and pre
        content = soup.find("html")
        # fetching the html text
        content = content.text
        # casefold and handle punctuations if asked by the user.
        final_content = cleanup(content, case_folding, punc_handling)

        # writing cleaned up text to file
        name = open("Corpus/" + file[:-5] + ".txt", "w",encoding='utf-8')
        name.write(final_content)
        name.close()


if __name__ == "__main__":
    # generate "Corpus" folder if not existing
    newpath = r'Corpus'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # by default perform case folding and removing punctuations
    generate_corpus(True,True)

