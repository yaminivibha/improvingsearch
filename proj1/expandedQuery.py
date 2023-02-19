"""
Implements Rocchio's algorithm
"""
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
from itertools import product

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
        # TODO: create empty instances of things initialized in function
        # self.vocab = 
        # self.vocab_list
        # self.query_tfidf
        # self.relevant_tfidf
        # self.irrelevant_tfidf
        # self.rocchio_score
        # self.added_words = ""
        self.computeTfIdfs()
        self.getRocchioScore()

    def computeTfIdfs(self):
        """
        Computes the tfidf vectors for the query, relevant docs,
        and irrelevant docs
        """
        tfidf = TfidfVectorizer(stop_words="english")
        self.vocab = tfidf.fit(self.docs).vocabulary_

        # print(f"vocab type: {type(vocab)}")
        tfidf_fixedvocab = TfidfVectorizer(vocabulary=self.vocab, stop_words="english")
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

    def sortQueryTerms(self):
        """
        sorts query terms using bigram counts
        """
        
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
        self.added_words = added_words
        # print(f"added words: {added_words}")
        return (' '.join(added_words), ' '.join(added_words) + " " + self.query)
