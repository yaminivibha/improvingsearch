"""
Implements Rocchio's algorithm
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from nlp_utils import preprocess
import numpy as np


class ExpandedQuery:
    def __init__(self, query, precision, relevant_docs, irrelevant_docs):
        """
        TODO: explain instance vars
        query = String containing current query terms
        precision = fraction of retrieved docs that are relevant to the query
        """
        self.query = query
        self.precision = precision
        self.docs = relevant_docs + irrelevant_docs
        self.relevant_docs = relevant_docs
        self.irrelevant_docs = irrelevant_docs
        self.computeTfIdfs()
        self.getRocchioScore()

    def computeTfIdfs(self):
        """
        Computes the tfidf vectors for the query, relevant docs,
        and irrelevant docs
        """
        tfidf = TfidfVectorizer()
        self.vocab = tfidf.fit(self.docs).vocabulary_

        # print(f"vocab type: {type(vocab)}")
        tfidf_fixedvocab = TfidfVectorizer(vocabulary=self.vocab)
        self.vocab_list = tfidf_fixedvocab.get_feature_names_out()

        self.query_tfidf = tfidf_fixedvocab.fit_transform([self.query])
        self.relevant_tfidf = tfidf_fixedvocab.fit_transform(self.relevant_docs)
        self.irrelevant_tfidf = tfidf_fixedvocab.fit_transform(self.irrelevant_docs)

        print(f"query: {self.query}")

        print(f"query tfidf: {self.query_tfidf}")
        print(f"query tfidf shape: {self.query_tfidf.shape}")
        print(f"relevant tfidf: {self.relevant_tfidf}")
        print(f"relevant tfidf shape: {self.relevant_tfidf.shape}")
        print(f"irrelevant tfidf: {self.irrelevant_tfidf}")
        print(f"irrelevant tfidf shape: {self.irrelevant_tfidf.shape}")
        return

    def getRocchioScore(self):
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
        self.rocchio_score = score
        self.rocchio_score[self.rocchio_score<0] = 0

    def computeBigrams(self):
        """
        Computes the bigrams of the document vectors
        """
        pass

    def getModifiedQueryVector(self):
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
        # print(f"added words: {added_words}")
        return (' '.join(added_words), ' '.join(added_words) + " " + self.query)
