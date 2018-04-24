import os.path as path
import os

# search if the doc(value) is already present in the inverted list(lst) of the term
def search(key,value,lst):
    for i in range(len(lst)):
        if lst[i][key] == value:
            return i
    return -1


def indexer(inp):
    index = {} # dictionary representing the index
    doc_length = {} # dictionary to store the document length
    paths = path.abspath(path.join(os.getcwd(), "../"))
    paths = os.path.join(paths, "Step 1-Corpus Generation\Corpus")
    # loop over every document in the corpus
    for file in os.listdir(paths):
        f = os.path.join(paths, file)
        f = open(f, "r",encoding='utf-8')
        content = f.read()
        content = content.replace("\n", "")
        content = ' '.join(content.split())
        content = content.split(" ")

        docid = file[:-4] # fetching the docid from the filename
        terms = [] # list containing all the terms of the document

        if (inp == 1): # for unigram terms[] will be same as content[]
            for item in content:
                terms.append(item)
        elif(inp==2): # generate bigram terms[] as below
            for i in range(len(content)-1):
                terms.append(content[i]+" "+content[i+1])
        elif(inp==3): # generate trigram terms[] as below.
            for i in range(len(content)-3):
                terms.append(content[i]+" "+content[i+1]+" "+content[i+2])

        doc_length[docid] = len(terms) # store the number of terms in a document

        # loop over every term in the document
        for term in terms:
            if term in index:
                # search if the docid is already present in the inverted list of the term
                doc_index = search('docid', docid, index[term])
                if doc_index == -1: # if not present, add a new posting to the list
                    index[term].append({'docid': docid, 'tf': 1})
                else: # if present, add one to the term frequency in that document
                    index[term][doc_index]['tf'] += 1
            # if term not present in the index create a new entry and a new posting in the inverted list
            # of that term
            else:
                index[term] = [{'docid': docid, 'tf': 1}]
        #print (file)

    # filename based on value of n in n-gram
    filename = "Unigram_index.txt"

    index_file = open(filename, "w",encoding='utf-8')

    # writing index to file
    for key, value in sorted(index.items()):
        index_file.write(key + " ->")
        for dic in value:
            flag = True
            for k, v in sorted(dic.items()):
                if flag:
                    index_file.write(" (" + str(v) + ",")
                    flag = False
                else:
                    index_file.write(str(v) + ")")
        index_file.write("\n")
    index_file.close()

    #writing document lengths to file
    doc_stats_file = open("Document_lengths.txt",'w',encoding='utf-8')
    for key,value in sorted(doc_length.items()):
        doc_stats_file.write(key + " " + str(value) + "\n")
    doc_stats_file.close

if __name__ == "__main__":
    # building the unigram index
    indexer(1)
