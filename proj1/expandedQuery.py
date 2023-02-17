"""
Implements Rocchio's algorithm
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from nlp_utils import preprocess

class ExpandedQuery:
        def __init__(self, query, precision, relevant_docs, irrelevant_docs):
                """
                TODO: explain instance vars
                """
                self.precision = precision
                self.relcount = len(relevant_docs)
                self.irrelcount = len(irrelevant_docs)
                self.relevant_docs = relevant_docs
                self.irrelevant_docs = irrelevant_docs
                self.computeTfidfs(query, self.relevant_docs, self.irrelevant_docs) # make less jank

        def computeTfIdfs(self):
                """
                Computes the tfidf vectors for the query, relevant docs,
                and irrelevant docs
                """
                tfidf = TfidfVectorizer()
                self.query_tfidf = tfidf.fit_transform(query)
                self.relevant_tfidf = tfidf.fit_transform(self.relevant_docs)
                self.irrelevant_tfidf = tfidf.fit_transform(self.irrelevant_docs)

                # print(f"relevant tfidf: {self.relevant_tfidf}")
                # print(f"irrelevant tfidf: {self.irrelevant_tfidf}")
                return
        
        def getRocchioScore(self):
                """
                Calculates the Rocchio score of a given word
                """
                # constants set empirically
                alpha = 1
                beta = 0.7
                gamma = 0.15

                score = alpha * q_0 + beta * \
                        relevant_docs + gamma * \
                        irrelevant_docs
        
                return score
        
        def getQueryVector():
                pass
        
        def getDocVector():
                pass