import os
import os.path as path
import re
import operator

INDEX = dict()
QUERY_LIST = dict()
TOP_DOCUMENTS = dict()
RELEVANT_DOCUMENTS = dict()
DOCUMENT_SENTENCE_MAP = dict()
STOP_WORDS = []

query_doc_map = dict()

TOP_DOC_COUNT = 5
SNIPPETS = 2

# **********************************************************************************************************************
# *************************** METHODS TO GENERATE DICTIONARIES AND HELPER FUNCTIONS ************************************


# BUIDING THE INVERTED INDEX
def create_index_dict():
    paths = path.abspath(path.join(os.getcwd(), "../"))
    paths = os.path.join(paths, "Phase 1")
    paths = os.path.join(paths, "Task 1")
    paths = os.path.join(paths, "Step 2-Index Generation")

    index_file = open(os.path.join(paths, "Unigram_index.txt"),'r',encoding='utf-8')
    content = index_file.read()
    entries = content.split("\n")
    entries = [e for e in entries if e != ""] # remove the last line
    # building the index again from file
    for entry in entries:
        entry =entry.split(" -> ")
        term = entry[0]
        postings = entry[1]
        INDEX[term] = []
        # remove the formatting
        postings = postings.replace("(","").replace(")","").split(" ")
        for posting in postings:
            posting = posting.rsplit(",",1)
            docid = posting[0]
            tf = int(posting[1])
            INDEX[term].append({'docid':docid,'tf':tf})

    index_file.close()


# BUILDING THE QUERY MAPPING QUERY ID -> QUERY
def get_queries():
    paths = os.path.abspath(os.path.join(os.getcwd(), "../"))
    paths = os.path.join(paths, "Phase 1")
    paths = os.path.join(paths, "Task 1")
    paths = os.path.join(paths, "Step 3- Query Cleaning")

    # get all queries from file
    path = open(os.path.join(paths, "cleanQueries.txt"), 'r', encoding='utf-8')
    content = path.read()
    path.close()
    queries = content.split("\n")
    queries = [q for q in queries if q != ""]
    for query in queries:
        query = query.split("||")
        QUERY_LIST[query[0]] = query[1]


# HELPER FUNCTION TO GET THE DOCUMENT ID
def search(key,value,lst):
    for i in range(len(lst)):
        if lst[i][key] == value:
            return i
    return -1


# HELPER TO CLEAN A SENTENCE
def clean_sentence(result):
    result = result.lower()
    result = re.sub(r"[^0-9A-Za-z,-\.:\\$]", " ", str(result))  # retain alpha-numeric text along with ',',':' and '.'
    result = re.sub(r"(?!\d)[$,%,:.,-](?!\d)", " ", str(result), 0)  # retain '.', '-' or ',' between digits
    result = result.split()
    return result

# HELPER TO CLEAN A WORD
def clean(result):
    result = result.lower()
    result = re.sub(r"[^0-9A-Za-z,-\.:\\$]", " ", str(result))  # retain alpha-numeric text along with ',',':' and '.'
    result = re.sub(r"(?!\d)[$,%,:.,-](?!\d)", " ", str(result), 0)  # retain '.', '-' or ',' between digits
    return result

# ****************************** METHODS TO GENERATE SNIPPETS **********************************************************

# main function to generate snippets
def generate_snippets():
    global STOP_WORDS

    # file to write the snippets
    output = open("Snippets_Lucene.html", 'w', encoding='utf=8')

    for key, value in QUERY_LIST.items():
        output.write("\n<br>" + "<U>QUERY " + key + ") : " + value + "</U>\n<br>")

        for doc in query_doc_map[key]:

            # get significant words for every document
            sig_words = find_significant_words(doc, value)

            # get all sentences in a document
            sentences = DOCUMENT_SENTENCE_MAP[doc]
            # print(DOCUMENT_SENTENCE_MAP)
            score = dict() # stores the score of the sentence
            starts = dict() # stores the start index of the snippet
            ends = dict() # stores the end index of the snippet

            # calculate score, start and end for every sentence
            for sentence in sentences:
                vals = calculate_sentence_significance(sentence, sig_words)
                score[sentence] = vals[2]
                starts[sentence] = vals[0]
                ends[sentence] = vals[1]

            # writing to file after sorting documents based on score
            output.write("\n<br>DCOCUMENT: " + doc + "\n<br>")
            score = sorted(score.items(), key=operator.itemgetter(1), reverse=True)
            i = 0
            for items in score:
                if i < SNIPPETS:
                    line = "..."
                    sentence = items[0]
                    start = starts[sentence]
                    end = ends[sentence]
                    # sentence = sentence.split()
                    sentence = clean_sentence(sentence)
                    for word in sentence:
                        if word in clean_sentence(value) and word not in STOP_WORDS:

                            # bolding the query terms
                            line = line + "<b>" + word + "</b> "
                        else:
                            line = line + word + " "
                    output.write(line)
                    i += 1
            output.write("\n<br>")
        output.write("<br>----------------------------------------------------------------------------------------------------------------<br>")
    output.close()


# getting ids of top documents obtained using BM25 for every query
def get_top_document_ids():
    paths = os.path.abspath(os.path.join(os.getcwd(), "../"))
    paths = os.path.join(paths, "Phase 1")
    paths = os.path.join(paths, "Task 1")
    search_res_path = os.path.join(paths, "Step 4 - Retrieval Models")
    search_res_path = os.path.join(search_res_path, "Lucene")
    search_res = open(os.path.join(search_res_path, "Lucene_Scores.txt"), 'r', encoding='utf-8')
    data = search_res.read()
    lines = data.split("\n")
    lines = lines[1:]

    # reading the output file to get the top relevant documents
    for i in range(0, len(lines)):
        if i < len(lines) - 2 and lines[i] == '' and lines[i+2] == '':
           continue
        else:
            if i < len(lines) - 1 and lines[i+1] != '':
                temp = lines[i+1].split(' ')
                key = temp[0]
                value = temp[2]

                if key in query_doc_map:
                    if len(res) < TOP_DOC_COUNT:
                        res = query_doc_map[key]
                        res.append(value)
                else:
                    res = []
                    res.append(value)
                query_doc_map[key] = res


# get all sentences for calculated relevant documents
def get_relevant_document_sentences():
    paths = path.abspath(path.join(os.getcwd(), "../"))
    paths = os.path.join(paths, "htmldocs")
    for key, value in query_doc_map.items():
        for req_file in value:
            for file in os.listdir(paths):
                name = (file[:-5])
                if req_file == name:
                    filename = os.path.join(paths, file)
                    f = open(filename, 'r', encoding='utf-8')
                    html = f.read()
                    f.close()
                    # removing tags and generating sentences
                    html = html.replace("<html>", "").replace("</html>", "").replace("<pre>", "").replace("</pre>", "")
                    create_sentence_dict(html, name)
                    f.close()


# break into sentences given an entire chunk of document after removing tags
def create_sentence_dict(html, name):
    if name in DOCUMENT_SENTENCE_MAP:
        return

    # removing redundant data
    index_of_am = html.rfind("AM")  # finds the last index of the term "am"
    index_of_pm = html.rfind("PM")  # finds the last index of the term "pm"

    # retain the text content until am or pm in the corpus documents
    if index_of_am > index_of_pm:
        greater_index = index_of_am
    else:
        greater_index = index_of_pm
    html = html[:(greater_index + 2)]

    # breaking into sentences
    strings = ""

    # not breaking on "." if "." is in a digit
    for word in html.split(" "):
        if "." in word:
            if not word[0].isdigit():
                word = word.replace('.', '\n\n')
        strings += word + " "
    html = strings

    sentences = html.split("\n\n")
    final_sentences = []
    for sentence in sentences:
        sentence = sentence.replace('\n', ' ')
        if sentence !=  '':
            sentence = clean_sentence(sentence)
            sentence = ' '.join(sentence)
            final_sentences.append(sentence)
    DOCUMENT_SENTENCE_MAP[name] = final_sentences


# calculate the significance factor of a sentence
def calculate_sentence_significance(sentence, sig_words):
    start_index = 0
    end_index = 0

    words = sentence.split()
    flag = True

    # getting the start and end indices
    # for word in words:
    #     if flag and word in sig_words:
    #         start_index = words.index(word)
    #         flag = False
    #
    #     if word in sig_words:
    #         end_index = words.index(word)

    start_index = 0
    for word in words:

        if word in sig_words:  # word_in_query(word,query_terms):
            start_index = words.index(word)
            break

    # find the end of span
        end_index = 0
    for i in range(len(words) - 1, 0, -1):
        if words[i] in sig_words:  # word_in_query(words[i],query_terms):
            end_index = i
            break

    count = 0
    for word in words[start_index:end_index]:
        if word in sig_words:
            count += 1

    # calculating the significance factor
    number = (end_index - start_index + 1)
    factor = (count * count) / number

    if start_index == 0 and end_index == 0:
        start_index = 0
        end_index = len(sentence) - 1
    elif start_index == end_index:
         start_index = 0

    return [start_index, end_index, factor]


def find_significant_words(doc, query):
    c = clean_sentence(query)
    return c

# finding the significant words in the document
def find_significant_words_invalid(doc):
    global STOP_WORDS
    sig_words = []

    sentences = DOCUMENT_SENTENCE_MAP[doc]
    sd = len(sentences)

    for sentence in sentences:
        words = clean_sentence(sentence)
        for word in words:
            if word not in STOP_WORDS:
                clean_word = clean(word)
                if True:
                    doc_index = search('docid', doc, INDEX[clean_word])
                # if current doc contains current term, update f with tf
                # from the index
                    fdw = 0
                    if doc_index != -1:
                        fdw = INDEX[clean_word][doc_index]['tf']

                    threshold = calc_threshold(sd)

                    # forming the significant words dict
                    if fdw >= threshold and word not in sig_words:
                        sig_words.append(word)

    return sig_words


# calculating the threshold
def calc_threshold(sd):
    if sd < 25:
        threshold = 7 - float(0.1) * float(25 - sd)
    elif (sd <= 40 and sd >= 25):
        threshold = 7
    else:
        threshold = 7 + float(0.1) * float(sd - 40)
    return threshold


# main function to start execution
def main():
    global  STOP_WORDS
    with open('common_words') as f:
        STOP_WORDS = f.read().splitlines()
    create_index_dict()
    get_queries()
    get_top_document_ids()
    get_relevant_document_sentences()
    generate_snippets()



main()