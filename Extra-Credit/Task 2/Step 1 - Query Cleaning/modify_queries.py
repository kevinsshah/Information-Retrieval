import os
# import os.path as path

QUERY_LIST = dict()
CORRECT = dict()
INCORRECT = []

def generate_query_dict():
    global QUERY_LIST
    paths = os.path.abspath(os.path.join(os.getcwd(), "SpellChecker"))
    paths = os.path.join(paths, "ErrorQueries.txt")
    path = open(paths, 'r')
    errors = path.read()
    path.close()
    queries = errors.split("\n")
    queries = [q for q in queries if q != ""]
    for query in queries:
        query = query.split("||")
        QUERY_LIST[query[0]] = query[1]

def generate_correction_dict():
    global INCORRECT
    paths = os.path.abspath(os.path.join(os.getcwd(), "SpellChecker"))
    paths = os.path.join(paths, "Replacements.txt")
    path = open(paths, 'r')
    content = path.read()
    for lines in content.split("\n"):
        words = lines.split()
        if words != []:
            CORRECT[words[0]] = words[1]
    print(CORRECT)
    INCORRECT = list(CORRECT.keys())


def replace_incorrect_terms():
    print(INCORRECT)
    output = open("CorrectQueries.txt", 'w')
    for key, value in QUERY_LIST.items():
        temp = ""
        for word in value.split(" "):
            # print(word)
            if word in INCORRECT:
                if 'NO' not in CORRECT[word]:
                    word = CORRECT[word]
            temp = temp + word + " "
        output.write(key + "||" + temp + "\n")
    output.close()





def main():
    generate_correction_dict()
    generate_query_dict()
    replace_incorrect_terms()

main()