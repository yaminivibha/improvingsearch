"""
Implements Rocchio's algorithm
"""
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
from itertools import permutations
from typing import List, Tuple
from nltk.util import everygrams
from collections import defaultdict
from nlp_utils import preprocess, tokenize, remove_stop_words


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
        Parameters:
        query               = current query terms
        precision           = fraction of retrieved docs that are relevant to the query
        relevant_docs       = list of strings containing relevant docs (unprocessed)
        irrelevant_docs     = list of strings containing irrelevant docs (unprocessed)
        Instance Variables:
        vocab_list          = list of strings containing the vocabulary of the corpus, indexes of strings 
                                correspond to the indexes of the tfidf vectors
        query_tfidf         = tfidf vector of the query
        relevant_tfidf      = tfidf vector of the relevant docs
        irrelevant_tfidf    = tfidf vector of the irrelevant docs
        rocchio_score       = tfidf vector of the expanded query
        added_words         = *string* containing the words added to the query
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

    def computeTfIdfs(self) -> Tuple[List[str], np.ndarray, np.ndarray, np.ndarray]:
        """
        Computes the tfidf vectors for the query, relevant docs,
        and irrelevant docs
        """
        tfidf = TfidfVectorizer(stop_words="english", preprocessor=preprocess)
        fixed_vocab = tfidf.fit(self.docs).vocabulary_
        tfidf_fixedvocab = TfidfVectorizer(
            vocabulary=fixed_vocab, stop_words="english", preprocessor=preprocess
        )

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
        sorts query terms using bigram counts
        """

        # we only care bout the bigrams that contain the added words
        # so we need to extract the bigrams from the relevant docs
        # and then find the bigrams that contain the added words
        processed_rel_docs = []
        for doc in self.relevant_docs:
            doc = preprocess(doc)
            doc = tokenize(doc)
            doc = remove_stop_words(doc)
            processed_rel_docs.append(doc)

        query = self.updated_query.split()
        print(f"query: {query}")
        possible_ngrams = []

        # Generate all possible ngrams of length 2 - length of query
        for i in range(2, len(query) + 1):
            possible_ngrams.extend(list(permutations(query, i)))
        list(everygrams(query))
        print(f"all possible ngrams of query: {possible_ngrams}")
        ngram_counts = {k: 0 for k in possible_ngrams}  # TODO: get_ngram_counts()
        # print(f"ngram_counts: {ngram_counts}")

        for doc in processed_rel_docs:
            doc_ngrams = list(everygrams(doc))
            print(f"doc ngrams: {doc_ngrams}")
            for ngram in doc_ngrams:
                if ngram in ngram_counts:
                    ngram_counts[ngram] += 1
        print(f"ngram_counts: {ngram_counts}")

        # actual sorting part
        # Sort by ngram_counts by decreasing n
        def ngram_sort(item: Tuple[Tuple[str], int]) -> Tuple[int]:
            ngram = item[0]
            return len(ngram), item[1]

        sorted_ngram_counts = dict(
            sorted(ngram_counts.items(), key=ngram_sort, reverse=True)
        )
        print(f"sorted_ngram by n: {sorted_ngram_counts}")

        # grab the top n_gram
        # Whatever words are not in the n_gram, add the words to the end
        # theoretically: could have more n_grams in the expanded query (multiple phrases) but this is enough for a simple query

    def getAddedWords(self) -> Tuple[str, str]:
        """
        Returns the modified query vector with additional terms
        """

        sorted_rocchio_scores = np.argsort(self.rocchio_score).tolist()[0]
        # print(f"sorted rocchio scores: {sorted_rocchio_scores}")
        # print(f"rocchio scores shape: {self.rocchio_score.shape}")

        added_word_ct = 0
        added_words = []
        for i in range(1, self.query_tfidf.shape[1] + 1):
            term_idx = sorted_rocchio_scores[-i]
            term = self.vocab_list[term_idx]
            # print(f"{i} th highest tf-idf term: {term} (index {term_idx})")
            if term not in self.query.split():
                added_words.append(term)
                added_word_ct += 1
            if added_word_ct == 2:
                break
        self.added_words = added_words
        # print(f"added words: {added_words}")
        return (" ".join(added_words), " ".join(added_words) + " " + self.query)


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
