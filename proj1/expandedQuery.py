"""
Implements Rocchio's algorithm
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from nlp_utils import preprocess
import pandas as pd

class ExpandedQuery:
        def __init__(self, query, precision, relevant_docs, irrelevant_docs):
                """
                TODO: explain instance vars
                """
                self.query = query
                self.precision = precision
                self.relcount = len(relevant_docs)
                self.irrelcount = len(irrelevant_docs)
                self.docs = relevant_docs + irrelevant_docs
                self.relevant_docs = relevant_docs
                self.irrelevant_docs = irrelevant_docs
                self.computeTfIdfs() # make less jank

        def computeTfIdfs(self):
                """
                Computes the tfidf vectors for the query, relevant docs,
                and irrelevant docs
                """
                tfidf = TfidfVectorizer()
                vocab = tfidf.fit(self.docs).vocabulary_

                #print(f"vocab type: {type(vocab)}")
                tfidf_fixedvocab = TfidfVectorizer(vocabulary=vocab)

                self.query_tfidf = tfidf_fixedvocab.fit_transform([self.query])
                self.relevant_tfidf = tfidf_fixedvocab.fit_transform(self.relevant_docs)
                self.irrelevant_tfidf = tfidf_fixedvocab.fit_transform(self.irrelevant_docs)
                
                print(f"query tfidf: {self.query_tfidf}")
                print(f"relevant tfidf: {self.relevant_tfidf}")
                print(f"irrelevant tfidf: {self.irrelevant_tfidf}")
                return
        
        def getRocchioScore(self):
                """
                Calculates the Rocchio score of a given word
                """
                # constants set empirically
                alpha = 1
                beta = 0.7
                gamma = 0.15

                #score = alpha * self.query_tfidf + beta * self.relevant_tfidf - gamma * self.irrelevant_tfidf
                #print(f"Rocchio score: {score}")
                return score
        
        def getQueryVector():
                pass
        
        def getDocVector():
                pass