import os
import operator

INDEX = dict()
DICT = list()
QUERY_LIST = list()
SUG = dict()

# BUIDING THE INVERTED INDEX
def create_index_dict():
    paths = os.path.abspath(os.path.join(os.getcwd(), "../"))
    paths = os.path.join(paths, "Information-Retrieval")
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


    for key in INDEX.keys():
        print(key)
        DICT.append(key)

    index_file.close()


def get_query_terms():
    global QUERY_LIST
    paths = os.path.abspath(os.path.join(os.getcwd(), "ErrorQueries.txt"))
    path = open(paths, 'r', encoding='utf-8')
    content = path.read()
    path.close()
    queries = content.split("\n")
    queries = [q for q in queries if q != ""]
    for query in queries:
        query = query.split("||")
        t = (query[1].split())
        QUERY_LIST = QUERY_LIST + t
        print(QUERY_LIST)


def build_suggestions():
    global DICT, QUERY_LIST
    DICT = sorted(DICT)
    QUERY_LIST = sorted(QUERY_LIST)
    print(len(DICT))
    print(len(QUERY_LIST))
    for right in DICT:
        for wrong in QUERY_LIST:
            if wrong not in DICT and wrong[0] == right[0] and len(wrong) == len(right):
                long = len(right)
                if len(wrong) > len(right):
                    long = len(wrong)
                threshold = int((0.6 * long) + 0.5)

                # calculating number of common words:

                common = len(list(set([c for c in right if c in wrong])))
                if(common >= threshold):
                    res = [right, common]
                    if wrong in SUG:
                        temp = SUG[wrong]
                        temp.append(res)
                        SUG[wrong] = temp
                    else:
                        temp = []
                        temp.append(res)
                        SUG[wrong] = temp
                print(right, wrong, common)

    document_score = sorted(SUG.items(), key=operator.itemgetter(1), reverse=True)
    print(document_score)






create_index_dict()
get_query_terms()
build_suggestions()
