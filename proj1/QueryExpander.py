"""
Implements Rocchio's algorithm
"""
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
from itertools import product
from typing import List, Tuple

class QueryExpander:
    """
    Class that expands query using Rocchio's algorithm and sorts using bigram counts
    """
    def __init__(self, query:str, precision:float, relevant_docs:List[str], irrelevant_docs:List[str]):
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
        added_words         = list of strings containing the words added to the query
        updated_query       = string containing the expanded query
        """

        self.query = query
        self.precision = precision
        self.docs = relevant_docs + irrelevant_docs
        self.relevant_docs = relevant_docs
        self.irrelevant_docs = irrelevant_docs
        self.vocab_list, self.query_tfidf, self.relevant_tfidf, self.irrelevant_tfidf = self.computeTfIdfs()
        self.rocchio_score = self.getRocchioScore()
        self.getRocchioScore()
        
        self.added_words, self.updated_query = self.getModifiedQueryVector()
        self.sortQueryTerms()


    def computeTfIdfs(self) -> Tuple[List[str], np.ndarray, np.ndarray, np.ndarray]:
        """
        Computes the tfidf vectors for the query, relevant docs,
        and irrelevant docs
        """
        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_fixedvocab = TfidfVectorizer(vocabulary=tfidf.fit(self.docs).vocabulary_, stop_words="english")
        
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
        score[score<0] = 0
        return score

    def sortQueryTerms(self):
        """
        sorts query terms using bigram counts
        """
        pass
        ## ngram_range = (2, 2) to extract bigrams
        # count_bigrams = CountVectorizer(ngram_range=(2,2), stop_words="english")
        # bigrams = count_bigrams.fit_transform(self.relevant_docs).tolist()[0]
        # bigram_vocab = count_bigrams.get_feature_names_out().tolist()
        # bigram_counts = bigrams.toarray().sum(axis=0)

        # bigrams_freq = dict(zip(bigrams, values))

        # for ng_count, ng_text in sorted([(bigram_counts[i],k) for k,i in bigram_vocab.items()], reverse=True):
        #     print(ng_count, ng_text)
        
        
        # print(f"bigram list: {bigrams}")
        # print(f"bigram list shape: {bigrams.shape}")
        # print(f"bigram vocab: {bigram_vocab}")



        # query_terms = self.added_words.extend(self.query.split())
        # possible_bigrams = [ele for ele in product(query_terms, repeat = 2)]
        # print(f"possible bigrams: {possible_bigrams}")

        # for bigram in possible_bigrams:
        #     index = bigram_vocab[bigram]
        #     print(f"{bigram} count: {bigrams[0, index]}")

        
    def getModifiedQueryVector(self) -> Tuple[str, str]:
        """
        Returns the modified query vector with additional terms
        """

        sorted_rocchio_scores = np.argsort(self.rocchio_score).tolist()[0]
        print(f"sorted rocchio scores: {sorted_rocchio_scores}")
        #print(f"rocchio scores shape: {self.rocchio_score.shape}")

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
        return (' '.join(added_words), ' '.join(added_words) + " " + self.query)
