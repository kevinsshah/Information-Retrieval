import os

query_doc_map = dict()
QUERY_LIST = dict()
RELEVANT = dict()


# getting ids of top documents obtained using BM25 for every query
def get_top_document_ids():
    paths = os.path.abspath(os.path.join(os.getcwd(), "../"))
    paths = os.path.join(paths, "Phase 1")
    paths = os.path.join(paths, "Task 1")
    search_res_path = os.path.join(paths, "Step 4 - Retrieval Models")
    search_res_path = os.path.join(search_res_path, "BM25")
    search_res = open(os.path.join(search_res_path, "BM25Scores.txt"), 'r', encoding='utf-8')
    data = search_res.read()
    lines = data.split("\n")
    lines = lines[1:]

    for i in range(0, len(lines)):
        if i < len(lines) - 2 and lines[i] == '' and lines[i+2] == '':
           continue
        else:
            if i < len(lines) - 1 and lines[i+1] != '':
                temp = lines[i+1].split(' ')
                key = temp[0]
                value = temp[2]

                if key in query_doc_map:
                    res = query_doc_map[key]
                    res.append(value)
                else:
                    res = []
                    res.append(value)
                query_doc_map[key] = res
    print(query_doc_map)

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

    print(QUERY_LIST)

# Use file cacm.rel.txt to build the relevance information dictionary
def populate_R_dict():
    global QUERY_LIST
    rel_file = open("cacm.rel.txt","r",encoding='utf-8')
    rel_content = rel_file.read()
    rel_file.close()
    rel_content = rel_content.split("\n")
    rel_content = [w for w in rel_content if w!=""]
    for line in rel_content:
        row = line.split(" ")
        qid = row[0]
        rel_doc = row[2]
        if qid in RELEVANT.keys():
            RELEVANT[qid].append(rel_doc)
        else:
            RELEVANT[qid] = []
            RELEVANT[qid].append(rel_doc)

    for id, val in QUERY_LIST.items():
        if id not in RELEVANT.keys():
            RELEVANT[id] = []

    print(RELEVANT)


def calculate_precision_and_recall():
    output = open("EVALUATION.txt", 'w', encoding='utf=8')

    for id, query in QUERY_LIST.items():
        print()




get_top_document_ids()
populate_R_dict()