import math
import operator
import os
import os.path as path

# parameters given to compute bm25 score
k1 = 1.2
b = 0.75
k2 = 100
N = 3204
r = 0
R = 0

index = {} # dict for storing the index
K = {} # dicy for storing K value for each document
doc_length = {} # dict for storing number of terms in a document

# search if a given document is present in the inverted list of given term
def search(key,value,lst):
    for i in range(len(lst)):
        if lst[i][key] == value:
            return i
    return -1


# Use file generated from HW3 to build K and doc_length dicts
def populate_dicts():
    paths = os.path.abspath(os.path.join(os.getcwd(), "../../"))
    paths = os.path.join(paths, "Step 2-Index Generation")
    file = open(os.path.join(paths,"Document_lengths.txt"),'r',encoding='utf-8')
    content= file.read()
    content = content.split("\n")
    content = [c for c in content if c!=""] #remove the last line

    sum_of_dls = 0
    for item in content:
        item = item.split(" ")
        docid = item[0]
        dl = int(item[1])
        doc_length[docid] = dl
        sum_of_dls += dl
    # calculate average document length
    avgdl = sum_of_dls / N
    # calculate K for a document by the formula given
    for key,value in doc_length.items():
        ratio = value/avgdl
        K[key] = k1*((1-b) + (b*ratio))


# calculate score for a single query
def calculate_score(output,query):
    query = query.split("||") # separate query id and query
    qid = query[0]
    full_query = query[1]
    qterms = full_query.split(" ") # collect all query terms in array

    qf = {} # dict for storing frequency of term in query
    # initialize qf dict
    for q in qterms:
        qf[q] = 0
    # populate qf dict
    for q in qterms:
        qf[q] += 1

    bm_score = {} # dict for storing the bm scores of each document
    for key,value in K.items(): # iterate over all documents
        score = 0
        for term in qterms: # iterate over all terms in query
            if term in index:
                inverted_list = index[term] # fetch inverted list of current term
                n = len(inverted_list)
                f = 0 # initialize tf in a document to 0
                doc_index = search('docid',key,index[term])
                # if current doc contains current term, update f with tf
                #    from the index
                if doc_index != -1:
                    f = index[term][doc_index]['tf']
                # calculate bm25 score by formula
                a = ((r+0.5)/(R-r+0.5))/((n-r+0.5)/(N-n-R+r+0.5))
                first = math.log(a)
                second = ((k1+1)*f)/(value+f)
                third = ((k2+1)*qf[term])/(k2+qf[term])
                score += first*second*third
        # if the doc doesnt contain any of the query term , do not consider adding it
        #    into results
        if score!=0:
            bm_score[key] = score
    # sort the documents by bm25 scores
    bm_score = sorted(bm_score.items(), key=operator.itemgetter(1), reverse=True)

    # write results to query
    i=1
    output.write("\n\n"+full_query+"\n")
    for key,value in bm_score[:100]:
        output.write("\n"+qid+" Q0 "+key +" "+str(i)+" "+str(value)+" BM25NoStopNoStem")
        i+=1


# creating inverted index into a dictionary
def create_index_dict():
    paths = os.path.abspath(os.path.join(os.getcwd(), "../../"))
    paths = os.path.join(paths, "Step 2-Index Generation")
    index_file = open(os.path.join(paths,"Unigram_index.txt"),'r',encoding='utf-8')
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


# calculate scores for all the queries from cleanQueries.txt
def calculate_scores():
    # get all queries from file
    paths = os.path.abspath(os.path.join(os.getcwd(), "../../"))
    paths = os.path.join(paths, "Step 3- Query Cleaning")
    path = open(os.path.join(paths,"ErrorQueries.txt"),'r',encoding='utf-8')
    content = path.read()
    path.close()
    queries = content.split("\n")
    queries = [q for q in queries if q!=""]
    output = open("BM25Scores_NoRelevance.txt",'w',encoding='utf=8')
    # loop over all the queries
    for query in queries:
        calculate_score(output,query)
    output.close()


if __name__ == "__main__":
    create_index_dict() # retrieve index from file
    populate_dicts() # populate K and doc_length dicts
    calculate_scores()