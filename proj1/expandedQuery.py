"""
Implements Rocchio's algorithm
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from nlp_utils import preprocess

class expandedQuery:
	def __init__(self, query, precision, relevant_docs, irrelevant_docs):
		self.precision = precision
		self.relevant_docs = relevant_docs
		self.irrelevant_docs = irrelevant_docs
		self.relcount = len(relevant_docs)
		self.irrelcount = len(irrelevant_docs)

	def computeTfIdf(self):
		tfidf = TfidfVectorizer()
		relevant_result = tfidf.fit_transform(self.relevant_docs)
		pass
	
	def getRocchioScore(self):
		alpha = 1
		beta = 0.7
		gamma = 0.15

		score = alpha * q_0 + beta * relevant_docs + gamma * irrelevant_docs
		return score
	
	def getQueryVector():
		pass
	
	def getDocVector():
		pass