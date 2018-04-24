import math
import operator
import os
import os.path as path
import random

# Containers for storing the data
per_query_split_list = []

# Error rate
ERROR_RATE = 0.40

def generate_query_list():
    # get all queries from file
    path = open("cleanQueries.txt",'r',encoding='utf-8')
    content = path.read()
    path.close()

    queries = content.split("\n")
    queries = [q for q in queries if q!=""]
    # loop over all the queries
    for query in queries:
        query = query.split("||")  # separate query id and query
        full_query = query[1]
        per_query_split_list.append(full_query.split())

def shuffle_query_terms():

    # Container to store the output query list
    shuffled_query_list = []

    # Iterate through each query and introduce error to 40% of the query terms
    for query in per_query_split_list:
        temp = []
        total_words = len(query)
        words_affect = int(total_words * ERROR_RATE)

        # Create a dictionary in the form of index : term
        index = dict(enumerate(query))

        # Sort the dictionary based on the term length and get the top 40% of terms that need to be shuffled
        sortedKeyList = sorted(index.keys(), key=lambda s: len(index.get(s)), reverse=True)[:words_affect]

        # Shuffle the words that need to be affected
        for pos in sortedKeyList:
            term = index[pos]
            if len(term) == 4:
                new_term = term[0] + term[2] + term[1] + term[3]
                index[pos] = new_term
            elif len(term) > 4:
                # Taking care of non-boundary characters
                start = term[0]
                end = term[-1]
                mid = list(term[1:-1])
                # Shuffle the non-boundary characters
                random.shuffle(mid)
                new_mid = "".join(mid)
                # Append the boundary characters
                new_term = start + new_mid + end

                index[pos] = new_term

        # Sort the dictionary to preserve the original query order
        for key in sorted(index):
            temp.append(index[key])

        shuffled_query_list.append(" ".join(temp))
    return shuffled_query_list

# writing to a file
def write_queries_to_file(final_query):
    fname = "ErrorQueries.txt"
    ofile = open(fname, 'w')
    qID = 1
    for query in final_query:
       line = str(qID) + "||" + query + "\n"
       ofile.write(line)
       qID +=1

def main():
    # Generate the query list from the cleaned query file
    generate_query_list()

    # Calculate and export the rankings of each query into a file
    output = shuffle_query_terms()

    # export the queries into a file
    write_queries_to_file(output)

main()