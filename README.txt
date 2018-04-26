Inorder to run this project, you will need:
1) Python (version >=3.0)
2) Java
3) BeautifulSoup pip install --upgrade --force-reinstall beautifulsoup4 
(there are other ways to install beautiful soup - can be found here: https://pypi.python.org/pypi/beautifulsoup4)
4) Lucene
5) Python Environment 
6) Java IDE like Eclipse/IntelliJ to import entire Lucene Folders as Java Projects


Steps for project execution:
Execute python file by:
> python file_name.py

Only Lucene model is implemented in Java. To execute it, just import the entire project into Eclipse/IntelliJ and add the required
three jar files required to run Lucene model.
> Run project as Java Application
1) Phase 1/Task 1/Step 4 - Retrieval Models/Lucene/src/Lucene.java
2) Phase 1/Task 3/Task 3-A/Step 4 - Retrieval Models/Lucene/src/Lucene.java
3) Phase 1/Task 3/Task 3-B/Step 4 - Retrieval Models/Lucene/src/Lucene.java


The folders in the repository are in the order in which you need to execute the files.

-)Phase 1 contains 3 tasks.
-)Each task has folders describing the tasks performed by the files present in it.
-)Execute Phase 1, followed by Phase 2, followed by Phase 3.
-)The repository also contains the extra credit folder which needs to be executed at the end.

NOTE:
Execute files in the order mentioned in the file structure.

Information about executable files:

----------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------------------

PHASE 1 (Indexing and retrieval):

	TASK 1:

	Folder structure:

	+---Task 1
|   |   +---Step 1-Corpus Generation
|   |   |   \---Corpus
|   |   +---Step 2-Index Generation
|   |   +---Step 3- Query Cleaning
|   |   \---Step 4 - Retrieval Models
|   |       +---BM25
|   |       +---Lucene
|   |       +---Query Likelihood
|   |       \---TF_IDF


	In Task 1, we have the following steps:

		Step 1: Corpus Generation
		File: Phase 1/Task 1/Step 1-Corpus Generation/corpus_generation.py
		- Generates the clean corpus generated from the raw html files given in htmldocs.


		Step 2: Index Generation
		File: Phase 1/Task 1/Step 2-Index Generation/indexer.py 
		- Generated the inverted index for the clean corpus.


		Step 3: Query Cleaning
		File: Phase 1/Task 1/Step 3- Query Cleaning/clean_query.py
		- Generates a file containing clean queries.

		Step 4: Retrieval Models
		The 4 retrieval models for ranking are as shown below:

			•	BM25:
			File: Phase 1/Task 1/Step 4 - Retrieval Models/BM25/bm25_NoRelevance.py
			- Generates a file containing a list of top 100 document IDs for the given 64 queries using BM25 without taking relevance into account.

			File: Phase 1/Task 1/Step 4 - Retrieval Models/BM25/bm25_Relevance.py
			- Generates a file containing a list of top 100 document IDs for the given 64 queries using BM25 taking relevance into account.
				

			•	Lucene:
			File: Phase 1/Task 1/Step 4 - Retrieval Models/Lucene/src/Lucene.java
			- Generates a file containing a list of top 100 document IDs for the given 64 queries using Lucene.

			•	Smoothed Query Likelihood
			File: Phase 1/Task 1/Step 4 - Retrieval Models/Lucene/src/Lucene.java
			- Generates a file containing a list of top 100 document IDs for the given 64 queries using Smoothed Query Likelihood model.

			•	TF-IDF
			File: Phase 1/Task 1/Step 4 - Retrieval Models/TF_IDF/tf-idf.py
			- Generates a file containing a list of top 100 document IDs for the given 64 queries using TF-IDF.


----------------------------------------------------------------------------------------------------------------------------------------------------------------------


	TASK 2(Query enrichment):

	Folder structure:

	+---Task 2
|   |   +---Step 1 - Query expansion
|   |   \---Step 2 - Retrieval PRF

	This task two has two steps:

		Step 1 - Query expansion
		File: Phase 1/Task 2/Step 1 - Query expansion/pseudoRelevance.py
		- Generates expanded queries using PseudoRelevance Feedback using top ranked documents from BM25 model(no relevance).

		Step 2 - Retrieval PRF
		File: Phase 1/Task 2/Step 2 - Retrieval PRF/bm25_NoRelevance_PRF.py
		- Generates a file containing a list of top 100 document IDs for the given 64 queries using BM25 No relevance but with queries generated in Step 1.


----------------------------------------------------------------------------------------------------------------------------------------------------------------------


	TASK 3(Stopping and Stemming):

	This task has two parts:

		TASK 3-A:

		Folder structure:

|       +---Task 3-A
|       |   +---Step 1-Corpus Generation
|       |   |   \---Stop_Corpus
|       |   +---Step 2-Index Generation
|       |   +---Step 3- Query Cleaning
|       |   \---Step 4 - Retrieval Models
|       |       +---BM25
|       |       +---Lucene
|       |       \---Query Likelihood

			Step 1: Corpus Generation
			File: Phase 1/Task 3/Task 3-A/Step 1-Corpus Generation/stopped_corpus_generator.py
			- Generates the clean corpus generated from the raw html files given in htmldocs after removing stopwords


			Step 2: Index Generation
			File: Phase 1/Task 3/Task 3-A/Step 2-Index Generation/indexer.py
			- Generates index using the corpus generated after removing stop words.


			Step 3: Query Cleaning
			File: Phase 1/Task 3/Task 3-A/Step 3- Query Cleaning/stop_query.py
			- Generates a file containing clean queries and removing stop words.


			Step 4: Retrieval Models
			The 3 baseline runs used for this task are as shown below:

				•	BM25:
				Files: Phase 1/Task 3/Task 3-A/Step 4 - Retrieval Models/BM25/bm25_NoRelevance.py
				- Uses BM25 model without relevance same as Task 1 but using the corpus and queries generated after removing stop words.

				•	Lucene:
				Files: Phase 1/Task 3/Task 3-A/Step 4 - Retrieval Models/Lucene/src/Lucene.java
				- Uses Lucene same as Task 1 but using queries generated after removing stop words.

				•	Smoothed Query Likelihood
				Files: Phase 1/Task 3/Task 3-A/Step 4 - Retrieval Models/Query Likelihood/Stop_smoothed_query_likelihood.py
				- Uses Smoothed Query Likelihood model same as Task 1 but using the corpus and queries generated after removing stop words.


		TASK 3-B:

		Folder structure:

			\---Task 3-B
|           +---Step 1-Corpus Generation
|           |   \---Stemmed_Corpus
|           +---Step 2-Index Generation
|           +---Step 3- Query Cleaning
|           \---Step 4 - Retrieval Models
|               +---BM25
|               +---Lucene
|               \---Query Likelihood


			Step 1: Corpus Generation
			File: Phase 1/Task 3/Task 3-B/Step 1-Corpus Generation/stemmed_corpus_generator.py
			- Generates the clean corpus generated from the raw html files given in htmldocs using stemming

			Step 2: Index Generation
			File: Phase 1/Task 3/Task 3-B/Step 2-Index Generation/indexer.py
			- Generates index using the corpus generated using stemming.


			Step 3: Query Cleaning
			File: Phase 1/Task 3/Task 3-B/Step 3- Query Cleaning/cleanQueries.txt
			- GContains a file containing clean queries and using stemming.(given to us)

			Step 4: Retrieval Models
			The 3 baseline runs used for this task are as shown below:

				•	BM25:
				Files: Phase 1/Task 3/Task 3-B/Step 4 - Retrieval Models/BM25/bm25_NoRelevance.py
				- Uses BM25 model without relevance same as Task 1 but using the corpus and queries generated using stemming.

				•	Lucene:
				Files: Phase 1/Task 3/Task 3-B/Step 4 - Retrieval Models/Lucene/src/Lucene.java
				- Uses Lucene same as Task 1 but using queries generated using stemming.

				•	Smoothed Query Likelihood
				Files: Phase 1/Task 3/Task 3-B/Step 4 - Retrieval Models/Query Likelihood/Stop_smoothed_query_likelihood.py
				- Uses Smoothed Query Likelihood model same as Task 1 but using the corpus and queries generated using stemming.



----------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------------------


PHASE 2 (Displaying results):

	Folder structure:

	+---Phase 2

	File: Phase 2/generate_snippets.py
	Generates snippets and highlights query terms in the snippets of top 5 documents for all the queries. 


----------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------------------


PHASE 3 (Evaluation):

	Folder structure:

	\---Phase 3
    \---Precision Recall Tables
        +---Baseline Lucene
        +---Baseline Smoothed Query Likelihood
        +---Baseline TF-IDF
        +---BM25 (No-Relevance)
        +---BM25 Pseudo-relevance Feedback
        +---Stopped BM25
        +---Stopped Lucene
        \---Stopped Smoothed Query Likelihood

	File: Phase 3/evaluation.py
	- Performs the following operations:
		1-­‐ MAP 
		2-­‐ MRR 
		3-­‐ P@K, K = 5 and 20 
		4-­‐ Precision & Recall

	Input the model to evaluate when prompted the following:

		"Decide the model on which you want to perform evaluation:
		Enter 1 for Baseline BM25
		Enter 2 Baseline Lucene
		Enter 3 Baseline Smoothed Query Likelihood
		Enter 4 Baseline TF-IDF
		Enter 5 BM25 Pseudo-relevance Feedback 
		Enter 6 Stopped BM25
		Enter 7 Stopped Smoothed Query Likelihood
		Enter 8 Stopped Lucene"



----------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------------------


Extra-Credit:


TASK 1 (Spelling error generator): 

	+---Task 1
|   +---Step 1-Corpus Generation
|   |   \---Corpus
|   +---Step 2-Index Generation
|   +---Step 3- Query Cleaning
|   +---Step 4 - Retrieval Models
|   |   \---BM25
|   \---Step 5 - Evaluation
|       \---Precision Recall Tables
|           \---BM25 (No-Relevance)


	Step 1: Corpus Generation
	File: Extra-Credit/Task 1/Step 1-Corpus Generation/corpus_generation.py
	- Generates the clean corpus generated from the raw html files. (same as Phase 1, Task 1)


	Step 2: Index Generation
	File: Extra-Credit/Task 1/Step 2-Index Generation/indexer.py
	- Generates index for the clean corpus (same as Phase 1, Task 2)


	Step 3: Query Cleaning
	File: Extra-Credit/Task 1/Step 3- Query Cleaning/query_error_generator.py
	- Generates a query file with spelling errors in the query as per the specification of the question.


	Step 4: Retrieval Models
	The 3 baseline runs used for this task are as shown below:

		•	BM25:
		Files: Extra-Credit/Task 1/Step 4 - Retrieval Models/BM25/bm25_NoRelevance.py
		- Uses BM25 model without relevance same as Task 1 but using the corpus and queries generated in step 1 and step 2 above.

	Step 5: Evaluation
	Files:
	File: Extra-Credit/Task 1/Step 5 - Evaluation/evaluation.py
	- Performs the following operations:
		1-­‐ MAP 
		2-­‐ MRR 
		3-­‐ P@K, K = 5 and 20 
		4-­‐ Precision & Recall

	Input the model to evaluate when prompted the following:

		"Decide the model on which you want to perform evaluation:
		Enter 1 for Baseline BM25"



TASK 2:
\---Task 2
    +---Step 1 - Query Cleaning
    |   \---SpellChecker
    +---Step 2 - Retrieval Models
    |   \---BM25
    \---Step 3 - Evaluation
        \---Precision Recall Tables
            \---BM25 (No-Relevance)


    Note: Use python 2.7 to run spellchecker.py in Step 1: Query Cleaning 
	Step 1: Query Cleaning
	File: Extra-Credit/Task 2/Step 1 - Query Cleaning/SpellChecker/spellchecker.py
	File: Extra-Credit/Task 2/Step 1 - Query Cleaning/modify_queries.py
	- Generates a query file with replacing spelling errors with correct words in the query as per the specification of the question.


	Step 2: Retrieval Models
	The 3 baseline runs used for this task are as shown below:

		•	BM25:
		Files: Extra-Credit/Task 2/Step 2 - Retrieval Models/BM25/bm25_NoRelevance.py
		- Uses BM25 model without relevance same as Task 1 but using the corpus and queries generated in step 1 and step 2 above.

	Step 3: Evaluation
	Files:
	File: Extra-Credit/Task 2/Step 3 - Evaluation/evaluation.py
	- Performs the following operations:
		1-­‐ MAP 
		2-­‐ MRR 
		3-­‐ P@K, K = 5 and 20 
		4-­‐ Precision & Recall

	Input the model to evaluate when prompted the following:

		"Decide the model on which you want to perform evaluation:
		Enter 1 for Baseline BM25"




