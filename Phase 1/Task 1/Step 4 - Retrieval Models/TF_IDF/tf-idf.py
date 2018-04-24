# Import libraries
import math
import operator
import os
import os.path as path

# Containers for storing the data
index = {}
doc_length = {}
tf_idf = {}
per_query_split_list = []
original_query_list = []

def generateDocLenCount():
    paths = os.path.abspath(os.path.join(os.getcwd(), "../../"))
    paths = os.path.join(paths, "Step 2-Index Generation")
    file = open(os.path.join(paths,"Document_lengths.txt"),'r',encoding='utf-8')
    content= file.read()
    # Split query in each line
    content = content.split("\n")
    # remove the last line
    content = [c for c in content if c!=""]

    for item in content:
        item = item.split(" ")
        docid = item[0]
        dl = int(item[1])
        doc_length[docid] = dl

def create_index_dict():
    paths = os.path.abspath(os.path.join(os.getcwd(), "../../"))
    paths = os.path.join(paths, "Step 2-Index Generation")
    index_file = open(os.path.join(paths,"Unigram_index.txt"),'r',encoding='utf-8')
    content = index_file.read()
    entries = content.split("\n")

    # remove the last line
    entries = [e for e in entries if e != ""]

    # building the index again from file
    for entry in entries:
        entry =entry.split(" -> ")
        term = entry[0]
        postings = entry[1]
        index[term] = {}
        # remove the formatting
        postings = postings.replace("(","").replace(")","").split(" ")
        for posting in postings:
            posting = posting.rsplit(",",1)
            docid = posting[0]
            tf = int(posting[1])
            index[term].update({docid:tf})

    index_file.close()
    # Calculate the length of each document in Corpus
    generateDocLenCount()

def calculate_TFIDF_Score():
     # Number of docs in Corpus
     N = 3204
     # Calculate score for each term in inverted index
     for word in index:
        tf_idf[word] = {}
        for docID in index[word]:
            tf = index[word][docID] / doc_length[docID]
            idf = 1.0 + (math.log(N / (len(index[word].keys()) + 1.0)))
            tf_idf[word][docID] = tf*idf

def generate_query_list():
    # get all queries from file
    paths = os.path.abspath(os.path.join(os.getcwd(), "../../"))
    paths = os.path.join(paths, "Step 3- Query Cleaning")
    path = open(os.path.join(paths,"cleanQueries.txt"),'r',encoding='utf-8')
    content = path.read()
    path.close()
    queries = content.split("\n")
    queries = [q for q in queries if q!=""]
    # loop over all the queries
    for query in queries:
        query = query.split("||")  # separate query id and query
        full_query = query[1]
        original_query_list.append(full_query)
        per_query_split_list.append(full_query.split())

def calc_score_per_query(per_query):
    score_list = {}
    query_list = {}

    # Retrieve the essential index list based on query words
    for per_word in per_query:
        if per_word not in tf_idf:
            query_list[per_word] = {}
        else:
            query_list[per_word] = tf_idf[per_word]

    # Calculate the overall score of each document in which the query terms are present
    for item in query_list:
        for docID in query_list[item]:
            if docID not in score_list.keys():
                docID_weight = 0
                for word in query_list:
                    if docID in query_list[word].keys():
                        docID_weight += query_list[word][docID]
                score_list[docID] = docID_weight
    return score_list


def export_score_list(fd, generated_score_list, id_num):
    # To sort the list in decreasing order of TF_IDF values
    final_ranked_list = sorted(generated_score_list.items(), key=lambda x: x[1], reverse=True)

    search_term = str(original_query_list[id_num - 1])

    fd.write("\n\n" + search_term + "\n")

    # The top 100 rankings is written in "query_id Q0 doc_id rank TF_IDF_score system_name" format
    for RANKING in range(100):
        try:
            text = "\n" + str(id_num) + " Q0 " + str(final_ranked_list[RANKING][0]) + " " + str(RANKING + 1) + " " \
               + str(final_ranked_list[RANKING][1]) + " RM_TF_IDF"
            fd.write(text)
        except IndexError:
            return


def calculate_query_score():
    id_num = 1

    fd = open("TF_IDF_SCORE.txt", "w", encoding='utf=8')

    # Calculate the rankings for each query and export the result into a file
    for query_line in per_query_split_list:
        generated_score_list = calc_score_per_query(query_line)
        export_score_list(fd, generated_score_list, id_num)
        id_num += 1

    fd.close()

def main():
    # Generate the inverted index from index file
    create_index_dict()

    # Calculate the TF_IDF score for each term in the index
    calculate_TFIDF_Score()

    # Generate the query list from the cleaned query file
    generate_query_list()

    # Calculate and export the rankings of each query into a file
    calculate_query_score()

main()