import math
import operator
import os
from collections import Counter

query_id_map = {} # dictionary for mapping query id with the actual query
query_top5_doc_map = {} # dictionary for qid with its top 5 documents
doc_top_freq_words_map = {}  # dictionary containing documents with its most frequent terms in sorted order
common_words = [] # list of common words
query_expansion_map = {} # dictionary containing qid as key and expanded query as the value

TOP_DOC_COUNT = 5 # no of top ranked documents to be considered for pseudo relevance feedback.
TOP_FREQ_WORD_COUNT = 5 # no of most frequent words in top ranked documents to be considered for expansion


# build the map that will contain expanded query against each qid
def create_query_expansion_map():
    for key,value in query_top5_doc_map.items():
        query = query_id_map[key] # fetch the original query
        expansion_list = [] # will contain the list of terms to be used for expanding query
        for item in value:
            counter = 0 # counter for TOP_FREQ_WORD_COUNT
            sorted_list = doc_top_freq_words_map[item] # get list of terms sorted by its tf in doc 'item'
            i = 0  # counter for index in sorted_list
            while counter!=TOP_FREQ_WORD_COUNT: # consider 5 top frequent words excluding stopwords or already
                                                #   present words in the query
                tuple = sorted_list[i]
                word = tuple[0]
                if (word not in common_words) and (word not in query) and (word not in expansion_list):
                    expansion_list.append(word)
                    counter+=1
                i+=1
        expansion_list = " ".join(expansion_list)
        query_expansion_map[key] = query + " " + expansion_list # form expanded query


# build the query_id_map which contains key as query id and value as the actual query
def create_query_id_map():
    # get all queries from file
    paths = os.path.abspath(os.path.join(os.getcwd(), "../Task 1/Step 3- Query Cleaning"))
    path = open(os.path.join(paths, "cleanQueries.txt"), 'r', encoding='utf-8')
    content = path.read()
    path.close()
    queries = content.split("\n")
    queries = [q for q in queries if q != ""]
    for query in queries:
        query = query.split("||")
        query_id_map[query[0]] = query[1]


# build the query_doc_map which contains key as query id and value as the list of top 5 ranked documents
#   from BM25 model for that query
def create_query_top5_doc_map():
    # read the file containing top BM25 scores
    paths = os.path.abspath(os.path.join(os.getcwd(), "../Task 1/Step 4 - Retrieval Models/BM25"))
    search_res = open(os.path.join(paths, "BM25Scores_NoRelevance.txt"), 'r', encoding='utf-8')
    data = search_res.read()
    search_res.close()
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

                if key in query_top5_doc_map:
                    if len(res) < TOP_DOC_COUNT:
                        res = query_top5_doc_map[key]
                        res.append(value)
                else:
                    res = []
                    res.append(value)
                query_top5_doc_map[key] = res


# build the dictionary containing docid as the key asn value as a list of tuples (term,tf) sorted in descending
#      order of tf
def create_doc_top_freq_words_map():
    for key,value in query_top5_doc_map.items():
        for item in value:
            f = open("../Task 1/Step 1-Corpus Generation/Corpus/"+item+".txt",'r',encoding='utf-8')
            content =f.read()
            content=content.split(" ")
            content=[w for w in content if w!=""]
            # get the most freq words in doc
            c = Counter(content)
            sorted_list = c.most_common()
            doc_top_freq_words_map[item] = sorted_list


# extracting the common words from a file to list
def get_common_words():
    global common_words
    f =open("common_words",'r',encoding='utf-8')
    content = f.read()
    f.close()
    content = content.split("\n")
    common_words = [w for w in content if w != ""]

# write expanded queries to file
def write_expanded_queries():
    f = open("expandedQueries.txt","w",encoding='utf-8')
    for key,value in query_expansion_map.items():
        f.write(key +"||"+value+"\n")
    f.close()

if __name__ == "__main__":
    get_common_words()
    create_query_id_map()
    create_query_top5_doc_map()
    create_doc_top_freq_words_map()
    create_query_expansion_map()
    write_expanded_queries()
