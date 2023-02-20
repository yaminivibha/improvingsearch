"""
Implements query expansion using Rocchio's algorithm; sorts query terms using n-gram counts
"""
from itertools import permutations
from typing import Dict, List, Tuple

import numpy as np
from nltk.util import everygrams
from sklearn.feature_extraction.text import TfidfVectorizer

from lib.nlp_utils import preprocess, remove_stop_words, tokenize


class QueryExpander:
    """
    Class that expands query using Rocchio's algorithm and sorts using bigram counts
    """

    def __init__(
        self,
        query: str,
        precision: float,
        relevant_docs: List[str],
        irrelevant_docs: List[str],
    ):
        """
        Instance Variables:
        query               = current query terms
        precision           = fraction of retrieved docs that are relevant to the query
        relevant_docs       = list of strings containing relevant docs (unprocessed)
        irrelevant_docs     = list of strings containing irrelevant docs (unprocessed)
        docs                = list of strings containing relevant and irrelevant docs (unprocessed)
        vocab_list          = list of strings containing the vocabulary of the corpus, indexes of strings 
                                correspond to the indexes of the tfidf vectors
        query_tfidf         = tfidf vector of the query
        relevant_tfidf      = tfidf vector of the relevant docs
        irrelevant_tfidf    = tfidf vector of the irrelevant docs
        rocchio_score       = tfidf vector of the expanded query
        added_words         = string containing the words added to the query
        updated_query       = string containing the expanded query
        """

        self.query = query
        self.precision = precision
        self.relevant_docs = relevant_docs
        self.irrelevant_docs = irrelevant_docs
        self.docs = self.relevant_docs + self.irrelevant_docs
        (
            self.vocab_list,
            self.query_tfidf,
            self.relevant_tfidf,
            self.irrelevant_tfidf,
        ) = self.computeTfIdfs()
        self.rocchio_score = self.getRocchioScore()

        self.added_words, self.updated_query = self.getAddedWords()
        self.sortQueryTerms()

    def constructQuery(self) -> str:
        """
        Constructs the expanded query
        """
        expanded_query = self.sortQueryTerms()
        return expanded_query

    def computeTfIdfs(self) -> Tuple[List[str], np.ndarray, np.ndarray, np.ndarray]:
        """
        Computes the tfidf vectors for the query, relevant docs,
        and irrelevant docs
        """

        # Create a tfidf vectorizer over all documents to generate fixed vocabulary
        tfidf = TfidfVectorizer(stop_words="english")
        fixed_vocab = tfidf.fit(self.docs).vocabulary_
        
        # Create a tfidf vectorizer with the fixed vocabulary
        tfidf_fixedvocab = TfidfVectorizer(
            vocabulary=fixed_vocab, stop_words="english"
        )

        # Use the fixed vocabulary to calculate tfidf matrices all docs
        vocab_list = tfidf_fixedvocab.get_feature_names_out()
        query_tfidf = tfidf_fixedvocab.fit_transform([self.query])
        relevant_tfidf = tfidf_fixedvocab.fit_transform(self.relevant_docs)
        irrelevant_tfidf = tfidf_fixedvocab.fit_transform(self.irrelevant_docs)

        return vocab_list, query_tfidf, relevant_tfidf, irrelevant_tfidf

    def getRocchioScore(self) -> np.ndarray:
        """
        Calculates the Rocchio score of a given query over the set of retrieved documents
        """
        # constants set empirically
        alpha = 1
        beta = 0.7
        gamma = 0.15

        score = (
            alpha * self.query_tfidf
            + beta * np.sum(self.relevant_tfidf, axis=0)
            - gamma * np.sum(self.irrelevant_tfidf, axis=0)
        )

        # set negative scores to 0
        score[score < 0] = 0
        return score

    def sortQueryTerms(self):
        """
        Sorts query terms using bigram counts
        """
        query = self.updated_query.split()
        # Grab the longest, most frequent n_gram that appears in relevant docs
        top_ngram = self.sortNgrams(self.constructNgramCounts())[0][0]
        sorted_query = " ".join(top_ngram)
        
        # Whatever words are not in the n_gram, add the words to the end
        if len(top_ngram) < len(query):
            for word in query:
                if word not in top_ngram:
                    sorted_query = sorted_query + " " + word
        
        return sorted_query

        #TODO: move into readme!           
        # theoretically: could have more n_grams in the expanded query 
        # (multiple phrases) but this is enough for a simple query

    def processRelDocs(self) -> List[str]:
        """
        Processes the relevant docs by removing stop words and tokenizing
        """
        processed_rel_docs = []
        for doc in self.relevant_docs:
            doc = preprocess(doc)
            doc = tokenize(doc)
            doc = remove_stop_words(doc)
            processed_rel_docs.append(doc)
        return processed_rel_docs

    def getAddedWords(self) -> str:
        """
        Returns the modified query vector with additional terms
        """

        sorted_rocchio_scores = np.argsort(self.rocchio_score).tolist()[0]

        added_word_ct = 0
        added_words = []
        for i in range(1, self.query_tfidf.shape[1] + 1):
            term_idx = sorted_rocchio_scores[-i]
            term = self.vocab_list[term_idx]
            if term not in self.query.split():
                added_words.append(term)
                added_word_ct += 1
            if added_word_ct == 2:
                break
        self.added_words = added_words
        return (" ".join(added_words), " ".join(added_words) + " " + self.query)

    def constructNgramCounts(self) -> Dict[Tuple[str, ...], int]:
        """
        Constructs a dictionary of ngram counts for the relevant docs
        Example: {('sergey', 'brin'): 2, ('sergey', 'brin', 'google'): 1}
        """

        # Extract the bigrams from the relevant docs
        # Find the bigrams that contain the added words
        processed_rel_docs = self.processRelDocs()
        query = self.updated_query.split()
        possible_ngrams = []

        # Generate all possible ngrams of length 2 - length of query
        for i in range(2, len(query) + 1):
            possible_ngrams.extend(list(permutations(query, i)))
        ngram_counts = {k: 0 for k in possible_ngrams}  

        # Count the number of times each ngram appears in the relevant docs
        for i, doc in enumerate(processed_rel_docs):
            doc_ngrams = list(everygrams(doc, max_len=len(query)))
            for ngram in doc_ngrams:
                if ngram in ngram_counts:
                    ngram_counts[ngram] += 1

        # Filter out ngrams count: 0 (not in relevant docs)
        ngram_counts = {ngram:count for ngram, count in ngram_counts.items() if count !=0}
        return ngram_counts

    def sortNgrams(self, ngram_counts) -> List[Tuple[Tuple[str], int]]:
        """
        Sorts ngrams by decreasing n, then decreasing count
        """
        def sort_key(item: Tuple[Tuple[str], int]) -> Tuple[int]:
            """Helper function returns sort criteria from ngram_counts"""
            ngram = item[0]
            return len(ngram), item[1]

        # Two-step sort: first by n, then by count
        sorted_ngram_counts = sorted(ngram_counts.items(), key=sort_key, reverse=True)
        return sorted_ngram_counts


#TODO: move into readme!
# ngram_counts:
# {('tabs',): 6,
# ('guitar',): 3,
# ('ultimate',): 1,
# ('tabs', 'guitar'): 0,
# ('tabs', 'ultimate'): 0,
# ('guitar', 'tabs'): 2,
# ('guitar', 'ultimate'): 0,
# ('ultimate', 'tabs'): 0,
# ('ultimate', 'guitar'): 1,
# ('tabs', 'guitar', 'ultimate'): 0,
# ('tabs', 'ultimate', 'guitar'): 0,
# ('guitar', 'tabs', 'ultimate'): 0,
# ('guitar', 'ultimate', 'tabs'): 0,
# ('ultimate', 'tabs', 'guitar'): 0,
# ('ultimate', 'guitar', 'tabs'): 1}

# discard all 1grams (done)
# discard any ngram with count: 0
# give more weight to higher n ngrams? but still want to give weight to high counts
# weighting = count * n
#
# Approach 1:
# Sort by ngram_counts by decreasing n
# Secondarily sort by n_gram counts
# grab the top n_gram
# Whatever words are not in the n_gram, add the words to the end
# theoretically: could have more n_grams in the expanded query (multiple phrases) but this is enough for a simple query
