
import operator
import os
import os.path as path

C = 0
lmdba = 0.35

index = {} # dict for storing the index
K = {} # dicy for storing K value for each document
doc_length = {} # dict for storing number of terms in a document
term_collection = dict() # dict for storing the count of query terms in the collection
final_scores = dict() # dict for storing the mapping query -> (document -> score)


# search if a given document is present in the inverted list of given term
def search(key,value,lst):
    for i in range(len(lst)):
        if lst[i][key] == value:
            return i
    return -1


# Use file generated from HW3 to build  K and doc_length dicts
def populate_dicts():
    paths = path.abspath(path.join(os.getcwd(), "../../"))
    paths = os.path.join(paths, "Step 2-Index Generation")

    file = open(os.path.join(paths, "Document_lengths.txt"),'r',encoding='utf-8')
    content= file.read()
    content = content.split("\n")
    content = [c for c in content if c!=""] #remove the last line

    sum_of_dls = 0
    for item in content:
        item = item.split(" ")
        docid = item[0]
        dl = int(item[1])
        doc_length[docid] = dl


# calculating |C| and filling up term_collection dictionary
def calculate_collection_data(allterms):

    C = 0
    for key, value in doc_length:
        C = C + value

    for term in allterms:
        inverted_list = index[term]
        for key, value in doc_length.items():
            value = term_collection[term]
            value += inverted_list[key]['tf']
            term_collection[term] = value


# Calculating P(qi|D)
def calculate_intermediate_score(f, d, cq):
    a = (1 - lmdba) * (f/d)
    b = lmdba * (cq / C)
    return a + b


def calculate_score(output,query):
    query = query.split("||") # separate query id and query
    qid = query[0]
    q = query[1]
    qterms = q.split(" ") # collect all query terms in array
    document_score = dict()

    for key,value in doc_length.items():
        d = value
        score = 1

        for term in qterms:

            f = 0  # initialize tf in a document to 0
            doc_index = search('docid', key, index[term])
            # if current doc contains current term, update f with tf
            # from the index
            if doc_index != -1:
                f = index[term][doc_index]['tf']
            cq = term_collection[term]

            intermediate = calculate_intermediate_score(f, d, cq)
            score = score * intermediate
        document_score[key] = score

    # sort the documents by scores
    document_score = sorted(document_score.items(), key=operator.itemgetter(1), reverse=True)

    # write results to query
    i = 1
    output.write("\n\n" + q + "\n")
    for key, value in document_score[:100]:
        output.write("\n" + qid + " Q0 " + key + " " + str(i) + " " + str(value) + "smoothedQueryLiklihood")
        i += 1


    final_scores[query] = document_score


def create_index_dict():
    paths = path.abspath(path.join(os.getcwd(), "../../"))
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
        index[term] = []
        # remove the formatting
        postings = postings.replace("(","").replace(")","").split(" ")
        for posting in postings:
            posting = posting.rsplit(",",1)
            docid = posting[0]
            tf = int(posting[1])
            index[term].append({'docid':docid,'tf':tf})

    index_file.close()


def calculate_scores():
    paths = os.path.abspath(os.path.join(os.getcwd(), "../../"))
    paths = os.path.join(paths, "Step 3- Query Cleaning")

    # get all queries from file
    path = open(os.path.join(paths, "cleanQueries.txt"),'r',encoding='utf-8')
    content = path.read()
    path.close()
    queries = content.split("\n")
    queries = [q for q in queries if q!=""]
    output = open("QueryLiklihoodScores.txt",'w',encoding='utf=8')

    allterms = []
    for query in queries:
        query = query.split("||")  # separate query id and query
        q = query[1]
        allterms.append(q.split(" "))  # collect all query terms in array

    # calculating cq and |C|
    calculate_collection_data(allterms)

    # loop over all the queries
    for query in queries:
        calculate_score(output,query)
    output.close()


if __name__ == "__main__":
    create_index_dict() # retrieve index from file
    populate_dicts() # populate K and doc_length dicts
    calculate_scores()