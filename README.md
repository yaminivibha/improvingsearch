# CS6111 Advanced Databases Project 1
###### Yamini Ananth yva2002, Erin Liang ell2147
Implementation of an information retrieval system that explicitly prompts the user for relevance feedback of search results in order to provide more relevant search results. Project uses the [Google Custom Search API](http://www.cs.columbia.edu/~gravano/cs6111/proj1.html#:~:text=Google%20Custom%20Search%20API%20(https%3A//developers.google.com/custom%2Dsearch/)) for the actual retrieval of results. Our main contribution is implementing the query expansion mechanism, the details of which are in this README.

This project was completed as part of the Spring 2023 version of Columbia University’s Advanced Database Systems course (COMS 6111) taught by Professor Luis Gravano at Columbia University.

## File Structure
~~~
├── proj1
│   ├── lib
│   │   ├── nlp_utils.py
│   ├── main.py
│   ├── QueryExpander.py
│   ├── QueryExecutor.py
├── requirements.txt
├── README.md
├── setup.sh
└── query_transcript.txt
~~~

| Filename           | Description                                                                                        |
|--------------------|----------------------------------------------------------------------------------------------------|
| `requirements.txt` | List of packages to install                                                                        |
| `setup.sh`         | Bash script for setting up environment                                                             |
| `QueryExpander.py` | Creates class for query expansion using Rocchio's algorithm; sorts query terms using n-gram counts |
| `QueryExecutor.py` | Creates class for query execution, response handling, and input processing                         |
| `main.py`          | Main function that handles the control flow of the information retrieval system                    |
| `nlp_utils.py`     | Utilities for processing documents + urls                                                          |


## How To Run
1. Navigate to the repository
```cd <your/path/to/improvingsearch>```
2. Make sure the setup script is executable by changing the file permissions:
```chmod +x setup.sh```
3. From the top level repository, install all the requirements with:
```bash setup.sh```
4. Navigate to the src folder:
```cd src```
5. Then run the project with:
```python3 main.py <google api key> <google engine id> <precision> <query>```
6. Example command with query “6111 databases” and desired precision of 0.9
```python3 main.py <google api key> <google engine id> 0.9 "6111 databases"```

## Credentials
Below are the credentials needed to test the information retrieval system. These credentials were generated following [these instructions](http://www.cs.columbia.edu/~gravano/cs6111/proj1.html#:~:text=As%20a%20second%20step%2C%20you%20will%20have%20to%20sign%20up%20for%20the%20Programmable%20Search%20Engine%20service%20(https%3A//programmablesearchengine.google.com/about/)%3A).

- Google Custom Search Engine JSON API Key
```AIzaSyDQTz-AzhWHv-Qbk3ADyPG4hFb3Z6PkLHM ```
- Google Engine ID:
```45add40315937647f```

        
### High-Level Control Flow and Components
A code trace for an expected program execution is as follows:

- User inputs API credentials,search query and desired precision when invoking `main.py`. 
- A `QueryExecutor` object is created to handle the query execution. It sends the query to Google’s Customized Search Engine (as specified by the Engine ID)
- The user annotates the top 10 documents retrieved, one-by-one, with relevance feedback
- The `QueryExecutor` stores the relevant documents and irrelevant documents’ URLs, titles, and snippets as strings and computes the precision of the query. If the precision is as desired or greater, then the program provides feedback summary and terminates. Otherwise, a `QueryExpander` object is initialized with the current query, relevant and irrelevant documents, and current precision.
    - If fewer than 10 documents are returned, the program terminates. If all documents are marked irrelevant, the program also terminates (since no augmented query can be constructed).
- The `QueryExpander` creates tf-idf matrices for all documents and the query and executes Rocchio’s algorithm to augment the query with two additional terms. Then, the augmented query is re-ordered using a term proximity strategy. The program continues expanding the query and iterating until the desired precision is reached.

- Notable differences from reference implementation:
    - More [robust input handling](https://github.com/yaminivibha/improvingsearch/blob/66587f1886b61b76405fffdba661f7a790ddd07e/proj1/QueryExecutor.py#L102-L108):
        - This program continually re-prompts the user for a “Y”, ”y”, “n”, or ”n”. It does not accept any other input.
        - In contrast, the reference implementation accepts “Y”, ”y” and classifies any other input as a no.
    - Expected behavior when there are less than 10 docs returned:
        - This program terminates elegantly with “Less than 10 results returned, Terminating…”
        - Reference implementation ends with a `NullPointerError`
        - We tested this by using a keyboard smash as the query, e.g. “kasjdfaksjdf;kaldf”

### External Packages
|         Library/Package         | Use case                                                                                                                                                                                                                                    |
|:-------------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| nltk.tokenize.word_tokenize     | Generates token strings from a single, long document string. For example, “I am a student in 6111 Databases!” → [”I”, “am”, “a”, “student”, “in”, “6111”, “Databases”]                                                                      |
| sklearn.feature_extraction.text | Sklearn’s native list of English stopwords, used to filter out stopwords in nlp_utils.py. For example,  [”I”, “am”, “a”, “student”, “in”, “6111”, “Databases”] →  [“student”, “6111”, “Databases”]                                          |
| googleapiclient.discovery.build | Used to interact with the Google Custom Search API                                                                                                                                                                                          |
| nltk.util.everygrams            | Creates n-grams from the retrieved documents. For example, creating trigrams: “i am a student in 6111 databases” → [(”I”, “am”, “a”), (”am”, “a”, “student), (”a”, “student”, “in”), (”student”, “in”, “6111”), (”in”, “6111”, “databases)] |
| sklearn.TfIdfVectorizer         | Creates TF-IDF matrices from lists of documents, using either a fixed vocabulary or generating vocabulary from the given document.                                                                                                          |

## TODO: Query-Modification Method

### Collecting Document Information
- We used three pieces of information for each search result: the title, the snippet, and the URL. From the URL, we took the path and tokenized each item in the path as separated by punctuation. For example, we would parse the url `[http://www.wikipedia.org/wiki/Sergey_Brin/](http://www.wikipedia.org/Sergey_Brin/)` as  `wiki sergey brin`. Highly relevant associated query terms were often located in URLs, and because we only use snippets and not the full text of the documents, the search terms found in the URLs were useful.
- We found that the query results we achieved using just the snippets were quite effective, and that adding the full text of web pages did not often increase the search precision. Therefore, we determined that there was no need to spend extra resources downloading web pages.
- Since we are not downloading pages, only titles and snippets which are universal across document types, we do not implement any specific non-HTML handling. 

### Pre-Processing

Two types of pre-processing were implemented:  (1) the sklearn native pre-processing, when we used sklearn native Vectorizers , (2) a pre-processor we wrote by hand in nlp_utils.py. This was used when we processed documents in order to compute n-grams for query ordering. Different pre-procesors had different impacts on query expansion which we will discuss in later sections. 


Here, we will give some justifications regarding specific parts of this pre-processing workflow and what we chose to include or exclude. 

- Universally, standard preprocessing techniques were performed on the retrieved documents, including putting everything in lowercase, stripping punctuation, and tokenizing.  

- Stopword elimination (filtering out common words that don’t lend context, like “as”, “and”, “or”, “for”, and ”a”) was then performed. 
    - We removed all words from the standard sklearn English stopwords list. This was necessary, because when we did not filter stopwords, they would be augmented into our expanded search query. These words, since they are so generic, did not help with increasing search precision.
    - We note that this didn’t yield the best results for every query— e.g. in “per se”, per is a stopword. When we were trying to sort the query by searching for the phrase “per se” in the relevant documents, we didn’t find any instances since we had removed the word “per” from the text during pre-processing. However, despite the non-optimal ordering, the query still terminated after only one augmented round. 
    - Ultimately, including stopwords tended to reduce precision per round more often than it was useful, so we decided to remove them. 

- Stemming (adding other morphological forms of the query terms) was not performed. 
    - Stemming user’s query terms would match more documents since the alternate word forms for the user’s query term are matched too.
    - This would increase recall, but reduces precision [5], and this system’s primary goal is to increase precision. Thus, we chose not to include it here. 

### Query Expansion technique

## Ordering the Terms in the Expanded Query
- The main algorithm used is the modified Rocchio’s algorithm, which is a vector space information retrieval model where text documents are represented as vectors. At a high-level, Rocchio’s algorithm computes the score for a particular candidate query expansion term with the goal of minimizing the cosine similarity between the query matrix and matrix representing the irrelevant docs, while maximizing the cosine similarity between the query matrix and relevant docs matrix.
- Rocchio’s Algorithm is as follows:
$$Q_1 = \alpha Q_0 + \frac{\beta}{|D_r|} \sum_{d_j \in D_r} d_j - \frac{\gamma}{|D_n|}\sum_{d_j\in D_n} d_j$$

    - In this situation $Q_1$ represents the “Rocchio score” of each word as represented in the document and query matrices after one more iteration of search.
    - Alpha, beta, and gamma are empirically set constants. We consider the cardinality of the sets of relevant and irrelevant documents ($|D_r|, |D_n|$), along with the sum of tf-idf vectors for each document in the relevant and irrelevant documents ($d_j \in D_r, d_j \in D_n$).
    - For an example of how Rocchio’s algorithm would work, see this [video explanation of the algorithm](https://youtu.be/yPd3vHCG7N4) from the University of Edinburgh.

- For each query expansion, we perform the classic algorithm. The constants alpha, beta, gamma of Rocchio algorithm are  "accepted settings" taken from the literature: alpha = 1, beta = 0.75, gamma = 0.15 [1]*.* When we are choosing which words to augment the query with, this gives positive weight to the relevant documents and negative weight the non-relevant documents in order to maximize the similarity of the query to the relevant documents and minimize the similarity with the irrelevant documents. In literature, the gamma term (corresponding to the irrelevant documents term we want to minimize) is lower than the beta term in order to give more importance to maximizing similarity between the query and relevant documents set.
- When creating tf-idf matrices for all of the retrieved documents, we used default sklearn utilities and build-in english stopwords and tokenizers. First, we created a fixed vocabulary covering all retrieved documents and the query string. Then, we used that to create separate tf-idf matrices for the relevant documents, irrelevant documents, and query string. It was important to create a unified vocabulary used across all of these matrices so that we could meaningfully perform arithmetic operations on them.
- We then used Rocchio’s algorithm as described in the literature to surface 2 terms to add to the query in each round of expansion. The new augmented query, which consisted of the original query from that round plus two additional terms, was ordered using the context of the documents retrieved from that round of search.
- We chose not to use synonym search (using WordNet or other thesaurus) to generate more query terms.
    - On average, in each round of query expansion, the vocabulary was approximately 150 words. Rocchio’s algorithm was able to surface 2 relevant terms, unique from the original query, that were not synonyms of the original query in almost all cases.
    - Since we are required to maintain the original query string in every round of search anyway, adding synonyms to the augmented query did not increase precision to the same level as implementing Rocchio’s algorithm did.

### Context

- After determining which two terms from the relevant documents we want to include in our next round of querying, one more question remains: **What order should the words of the expanded query be in?** For example, “new york city restaurant” would be a far better (closer to the user’s intent) query than “new city restaurant york”, and would probably yield better results.
- Goal: We wanted to order the words in the augmented query based on the contents of the query results from the previous iteration and their relevance judgments, but without querying Google again.
- There are many (n!) alternate ways of ordering the words in a query of n terms and we conducted a very preliminary literature review to determine the best possible way to order the words in the expanded query, but most papers focused on mechanisms of query expansion (how might we determine what terms from the corpus to add to the query to retrieve more relevant results?) and not specifically the query reordering.
- Our high-level query reordering algorithm is based off of the term proximity query expansion approaches we saw in lecture and in our preliminary literature review [[4]](https://www.sciencedirect.com/science/article/pii/S0020025511001356). The intuition behind these term proximity approaches is that query terms that appear close to each other are likely phrases (e.g. “new york city”, rather than “new city”). We make the simplification of using N-grams (contiguous sequences of words) in contrast to terms in a window size, which more sophisticated algorithms use.

### Query reordering algorithm:

- Generate all possible permutations of N-grams of length 2 → the length of the query and count the number of times each ngram appears in the *relevant docs only*.
    - 1-grams are not generated because they are single terms, and would therefore automatically occur frequently in documents. The goal here is to give more “weight” to phrases of at least 2 words, even if they occur less frequently than individual words.

```python
{('new', 'york'): 6,
 ('new', 'city'): 0,
 ('new', 'restaurant'): 1,
 ('york', 'city'): 6,
 ('york', 'restaurant'): 3,
 ('york', 'new'): 0,

...

('new', 'york','restaurant'): 1,
...
('new', 'york', 'city', 'restaurant'): 6,
...
('new', 'restaurant', 'city', 'york'): 0,
}
```

- Filter out the N-grams with count: 0. Having a count: 0 means that this permutation of the query terms does not occur in the relevant documents at all and thus should not be considered as a potential reordered query candidate.
- Sort this dictionary containing all the permutations of the query words by decreasing N. We do this because we want to select the longest phrase that occurs in the corpus of relevant documents, e.g. give more weight to “new york city” than “new york”
- Secondarily sort this dictionary by the number of times the N-gram occurs in the relevant documents, in decreasing order. We sort the dictionary by this “phrase frequency” after sorting by the length of the phrase to always prioritize longer phrases.

```python
# filtered & sorted:
{('new', 'york', 'city', 'restaurant'): 6,
('new', 'york','restaurant'): 1,
...
('new', 'york'): 6,
 ('york', 'city'): 6,
 ('york', 'restaurant'): 3,
('new', 'restaurant'): 1,
...
}
```

- Take the longest, most frequently occuring phrase (the N-gram in the first entry) and append whatever query terms that are left over and are not in that N-gram to the augmented query. e.g. if “new york city” is the top N-gram and “new city restaurant york” is the augmented query, our reordered expanded query is “new york city restaurant.” These leftover query terms are appended in the order of the previous iteration’s query.

### Other designs considered

- This approach seemed to work well enough for our constrained context. With the test case of the query “brin”, the augmented query became “brin sergey google”, and the final sorted augmented query because “sergey brin google”, which was the behavior we were hoping for. Other modifications to our algorithm that we considered implemented given more time and energy include:
    - Considering multiple N-grams in the query: A longer query can contain multiple phrases, not just one phrase. In our algorithm, we only consider the case of one phrase and append the rest of the query terms to the end and this could obviously be improved by repeating the process on the leftover query terms. However, this approach is enough for simple query cases.
    - Establish a weighting scheme: We prioritize longer N-grams over slightly shorter N-grams no matter how less frequent the longer N-gram. This scheme seemed to work reasonably well, but in a case where a 4-gram appears once and a 3-gram (that is not in the 4-gram) appears 10 times, we would probably want to include the 3-gram over the 4-gram. This necessitates a more flexible weighting scheme, but these weights would need to be determined empirically via more testing. Ideally, the weight of the N-gram should be a function of the N-gram’s frequency and N.
    - Adding support for term proximity windows instead of enforcing contiguous phrases via N-grams

## Future Work
- The field of query expansion is decently well-researched and there were many alternative, more modern query reformulation techniques that we could have implemented.
- However, many reviewed techniques would have added a good deal of complexity to implement and would have only contributed marginal benefit to our results. Most techniques in literature try to balance multiple evaluation metrics (e.g. precision and recall) or use some sort of extra information about the user (e.g. past query logs) to give more personalized, and thus more relevant results [2]. Given our very specific query setting and scenario for this project—only caring about minimizing the number of iteration that the information retrieval system takes to reach the target precision and having no extra information about the user—many of these techniques would not have adapted well.
- While testing our system, our query results ironically raised more questions, particularly related to how we should be preprocessing our documents. We experimented with different types of preprocessing `sklearn` and `ntlk` packages to help us implement Rocchio’s algorithm and the query term reordering algorithm. Changing the way the documents were preprocessed yield dramatically different results.
    - For example, when querying “brin” with the intent of finding information about Sergey Brin, the co-founder of Google, when using the preprocessor that we implemented in `nlp_utils.py` with  `sklearn.TfIdfVectorizer`, Rocchio’s algorithm yielded the additional search terms `sergey page`, as in Larry Page (the other co-founder of Google).
    - However, when we used the sklearn built-in preprocessor with `sklearn.TfIdfVectorizer`, the output was `sergey google`.
    - We hypothesize that this is due to the fact that our `nlp_utils.py` preprocessor yields different output text than the builtin `sklearn` function, possibly due to the tokenizer we use in `nlp_utils.py` being `nltk.text.word_tokenizer`. It’s not possible to retrieve the processed documents from `sklearn Vectorizers`, so we could not directly identify the differences between the documents.
    - In general, considering how document pre-processing affects both query expansion and precision is a robustly interesting region for future work.

## References
1. Manning, Raghavan, and Schütze Introduction to Information Retrieval, Chapter 9
2. [Azad and Deepak, Query expansion techniques for information retrieval: A survey, Information Processing & Management, Volume 56, Issue 5, 2019](https://www.sciencedirect.com/science/article/pii/S0306457318305466)
3. [Lavrenko, Example of Rocchio Algorithm](https://www.notion.so/README-references-design-doc-how-to-run-etc-650f623d39874e2fbc892bf936d9dadc)
4. [He, Huang, and Zhou, Modeling term proximity for probabilistic information retrieval models, Information Sciences, Volume 181, Issue 14, 2011](https://www.notion.so/README-references-design-doc-how-to-run-etc-650f623d39874e2fbc892bf936d9dadc)
5. [Kodimala, Savitha, "Study of stemming algorithms" (2010). UNLV Theses, Dissertations, Professional Papers, and Capstones. 754.](https://digitalscholarship.unlv.edu/cgi/viewcontent.cgi?article=1755&context=thesesdissertations#:~:text=Stemming%20is%20a%20process%20of,time%20of%20indexing%20and%20searching)
