import os.path as path
import os
import re

# removing tags from queries
def read_file_initialize_queries():
    final_query = dict()
    file = open("cacm.query.txt", "r")
    queries = file.read()
    queries = queries.replace('<DOC>', '').replace('\n', ' ').replace('\t', ' ').replace('<DOCNO>', '')
    query_array = queries.split("</DOC>")
    del query_array[-1]
    for query in query_array:
        temp = query.split('</DOCNO>')
        key = temp[0].replace(' ', '')
        value = temp[1].strip()
        value = cleanup(value, True, True)
        final_query[key] = value
    write_queries_to_file(final_query)


# writing to file
def write_queries_to_file(final_query):
    fname = "cleanQueries.txt"
    ofile = open(fname, 'w')
    for key, value in final_query.items():
       line = key + "||" + value + "\n"
       ofile.write(line)


def handle_punctuations(content):
    result = re.sub(r"[^0-9A-Za-z,-\.:\\$]"," ",str(content))  # retain alpha-numeric text along with ',',':' and '.'
    result = re.sub(r"(?!\d)[$,%,:.,-](?!\d)", " ", str(result), 0)  # retain '.', '-' or ',' between digits
    result = result.split()

    result_text = ' '.join(result)
    return result_text


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


# calling the main function
def main():
    read_file_initialize_queries()


main()

