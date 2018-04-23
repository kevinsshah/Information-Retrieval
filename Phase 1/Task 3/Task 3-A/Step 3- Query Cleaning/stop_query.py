# Repo for list of stop words
STOP_WORDS_REPO = "common_words"

def generate_query_list():

    stopped_query_dict = {}

    stop_words_list = open(STOP_WORDS_REPO, 'r').read().splitlines()
    # get all queries from file
    path = open("cleanQueries.txt",'r',encoding='utf-8')
    content = path.read()
    path.close()

    queries = content.split("\n")
    queries = [q for q in queries if q!=""]

    qID = 1
    # loop over all the queries
    for query in queries:
        query = query.split("||")  # separate query id and query
        full_query = query[1]
        per_query_split_list = full_query.split(" ")
        # Filter the stop words from the query
        stopped_query = [x for x in per_query_split_list if x not in stop_words_list]
        stopped_query_dict[qID] = (" ").join(stopped_query)
        qID += 1

    return stopped_query_dict

def write_queries_to_file(final_query):
    fname = "StoppedQueries.txt"
    ofile = open(fname, 'w')

    # Writing the Stopped queries into a file
    for key, value in final_query.items():
       line = str(key) + "||" + str(value) + "\n"
       ofile.write(line)

def main():
    # Read the contents of the cleaned query file for
    # performing stopping operation
    output_dict = generate_query_list()

    # Write the stopped queries into a file
    write_queries_to_file(output_dict)

main()