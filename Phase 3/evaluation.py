import os
from collections import OrderedDict

queryId_top100Docs = dict() # dict containing query id as key and value as list of its top 100 docs
queryId_query = dict() # dict containing query id as key and its query as value
queryId_relevantDocs = dict() # dict containing query id as key and value as list of ots relevant docs

queryId_RR = dict() # dict containing query id as key and value as reciprocal rank of this query
queryId_averagePrecision = dict() # dict containing query id as the key and value as its average precision
precision_at_5 = dict() # dict for query id as the key and value as the precision value at rank 5 for this query
precision_at_20 = dict() #dict for query id as the key and value as the precision value at rank 20 for this query


# building the mapping queryId -> List of top 100 docs
def build_queryId_top100Docs():
    paths = os.path.abspath(os.path.join(os.getcwd(), "../")+inputpath)
    search_res = open(paths, 'r', encoding='utf-8')
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

                if key in queryId_top100Docs:
                    res = queryId_top100Docs[key]
                    res.append(value)
                else:
                    res = []
                    res.append(value)
                queryId_top100Docs[key] = res


# building the mapping queryId -> query
def build_queryId_query():
    # get all queries from file
    paths = os.path.abspath(os.path.join(os.getcwd(), "../Phase 1/Task 1/Step 3- Query Cleaning"))
    path = open(os.path.join(paths, "cleanQueries.txt"), 'r', encoding='utf-8')
    content = path.read()
    path.close()
    queries = content.split("\n")
    queries = [q for q in queries if q != ""]
    for query in queries:
        query = query.split("||")
        queryId_query[query[0]] = query[1]


# building the mapping queryId -> List of relevant docs
def build_queryId_relevantDocs():
    global queryId_relevantDocs
    rel_file = open("cacm.rel.txt","r",encoding='utf-8')
    rel_content = rel_file.read()
    rel_file.close()
    rel_content = rel_content.split("\n")
    rel_content = [w for w in rel_content if w!=""]
    for line in rel_content:
        row = line.split(" ")
        qid = row[0]
        rel_doc = row[2]
        if qid in queryId_relevantDocs.keys():
            queryId_relevantDocs[qid].append(rel_doc)
        else:
            queryId_relevantDocs[qid] = []
            queryId_relevantDocs[qid].append(rel_doc)


# function to compute reciprocal rank of each query
def calculate_reciprocal_rank(docName_R_N):
    R_N_list = list(docName_R_N.values()) # get list of R/N values from dict docName_R_N
    try:
        rank = R_N_list.index("R") + 1    # gets the first occurence of "R"
    except ValueError:
        rank = 0
    if rank == 0: # no relevant document
        reciprocal_rank = 0
    else:
        reciprocal_rank = 1/rank
    return reciprocal_rank


# function to compute the list of docs replaced by "R" if relevant and "N" if non-relevant
def calc_R_N_list(q):
    docName_R_N = {}                            # dictinary that has a document as it's key and it's corresponding
                                                # mapping to "R" or "N" for query q as it's value
    if q in queryId_relevantDocs:
        relevant_docs = queryId_relevantDocs[q]
        top_100_docs = queryId_top100Docs[q]
        for doc in top_100_docs:
            if doc in relevant_docs:
                docName_R_N[doc] = "R"             # "R" denotes the document is relevant
            else:
                docName_R_N[doc] = "N"             # "N" denotes the document is non-relevant
    return docName_R_N


# building precision and recall tables for each query and writing to output
def calculate_precision_and_recall():
    for qid in queryId_relevantDocs.keys():
        if qid in queryId_relevantDocs.keys(): # exclude queries with no relevance information
            rank = 1
            relevance_count = 0
            Relevant_precisions = []  # stores the precision value of the relevant documents
            no_of_rel_docs = len(queryId_relevantDocs[qid])
            docName_R_N = calc_R_N_list(qid)
            RR = calculate_reciprocal_rank(docName_R_N) # compute reciprocal rank
            f = open(newpath + "Precision_Recall_Table_for_" + qid + '.txt', 'w')
            f.write("Query "+qid +": %s\n\n" % queryId_query[qid])
            f.write("RANK \t R/N \tPrecision \t  Recall\n\n")
            for rel in docName_R_N:
                if docName_R_N[rel] == "R":
                    relevance_count += 1
                curr_precision = relevance_count/rank # formula for precision
                if docName_R_N[rel] == "R":
                    Relevant_precisions.append(curr_precision)

                if rank == 5: # store precision at rank 5
                    precision_at_5[qid] = curr_precision
                if rank == 20:# store precision at rank 20
                    precision_at_20[qid] = curr_precision

                recall = relevance_count / no_of_rel_docs # formula for recall
                # append a 0 to the single-digit numbers, example: make "1" as "01"
                if rank <= 9:
                    rank_str = "0" + str(rank)
                else:
                    rank_str = str(rank)
                f.write(rank_str + "  \t  " + docName_R_N[rel] + "  \t  %.3f" % curr_precision \
                        + "  \t  %.3f" % recall + "\n")

                if len(Relevant_precisions) == 0:
                    queryId_averagePrecision[qid] = 0
                else:
                    queryId_averagePrecision[qid] = sum(Relevant_precisions) / len(Relevant_precisions)

                rank += 1

            queryId_RR[qid] = RR
            f.close()


def calculate_MAP_MRR_PatK():
    # Write the final evaluation, which contains the MAP and MRR values for the retrieval model, to a file
    f1 = open(newpath + "Final Evaluation.txt", 'w')
    MAP = sum(queryId_averagePrecision.values()) / len(queryId_averagePrecision.keys())
    f1.write("Mean Average Precision = %f\n\n" % MAP)

    MRR = sum(queryId_RR.values()) / len(queryId_RR.keys())
    f1.write("Mean Reciprocal Rank = %f\n\n" % MRR)
    f1.close()

    # Write the P@K values, which contains the Precision at rank "k" values for the retrieval model, to a file
    f2 = open(newpath + "P@KValuesForAllQueries.txt", 'w')
    for qID in queryId_relevantDocs:
        if qID in precision_at_5.keys():
            f2.write("For query "+ qID+": %s\n\n" % queryId_query[qID])
            f2.write("Precision at rank 5: %f\n" % precision_at_5[qID])
            f2.write("Precision at rank 20: %f\n\n" % precision_at_20[qID])
            f2.write("\n-----------------------------------------------------------------------------"
                     "----------------------------------------------------------------\n")
    f2.close()


# set paths based on user input
def set_paths():
    global newpath
    global inputpath

    inp = input("Decide the model on which you want to perform evaluation:\n"
                + "Enter 1 for Baseline BM25\n" +
                "Enter 2 for Baseline Lucene\n" +
                "Enter 3 for Baseline Smoothed Query Likelihood\n" +
                "Enter 4 for Baseline TF-IDF\n" +
                "Enter 5 for BM25 Pseudo-relevance Feedback \n" +
                "Enter 6 for Stopped BM25\n" +
                "Enter 7 for Stopped Smoothed Query Likelihood\n" +
                "Enter 8 for Stopped Lucene\n")

    newpath = r'Precision Recall Tables/'
    if int(inp) == 1:
        newpath = newpath +'/BM25 (No-Relevance)/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        inputpath = r"Phase 1/Task 1/Step 4 - Retrieval Models/BM25/BM25Scores_NoRelevance.txt"
    elif int(inp) == 2:
        newpath = newpath + '/Baseline Lucene/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        inputpath = r"Phase 1/Task 1/Step 4 - Retrieval Models/Lucene/Lucene_Scores.txt"
    elif int(inp) == 3:
        newpath = newpath + '/Baseline Smoothed Query Likelihood/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        inputpath = r"Phase 1/Task 1/Step 4 - Retrieval Models/Query Likelihood/QueryLikelihoodScores.txt"
    elif int(inp) == 4:
        newpath = newpath + '/Baseline TF-IDF/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        inputpath = r"Phase 1/Task 1/Step 4 - Retrieval Models/TF_IDF/TF_IDF_SCORE.txt"
    elif int(inp) == 5:
        newpath = newpath + '/BM25 Pseudo-relevance Feedback/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        inputpath = r"Phase 1/Task 2/Step 2 - Retrieval PRF/BM25Scores_NoRelevance_PRF.txt"
    elif int(inp) == 6:
        newpath = newpath + '/Stopped BM25/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        inputpath = r"Phase 1/Task 3/Task 3-A/Step 4 - Retrieval Models/BM25/Stop_BM25Scores_NoRelevance.txt"
    elif int(inp) == 7:
        newpath = newpath + '/Stopped Smoothed Query Likelihood/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        inputpath = r"Phase 1/Task 3/Task 3-A/Step 4 - Retrieval Models/Query Likelihood/StopQueryLikelihoodScores.txt"
    elif int(inp) == 8:
        newpath = newpath + '/Stopped Lucene/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        inputpath = r"Phase 1/Task 3/Task 3-A/Step 4 - Retrieval Models/Lucene/Stop_Lucene_Scores.txt"
    else:
        print("Incorrect Choice. Try again!")
        exit()


if __name__ == "__main__":
    set_paths()
    build_queryId_query()
    build_queryId_top100Docs()
    build_queryId_relevantDocs()
    calculate_precision_and_recall()
    calculate_MAP_MRR_PatK()

