"""
Implements Rocchio's algorithm
"""
from sklearn.feature_extraction.text import TfidfVectorizer

class expandedQuery:
	def __init__(self, query, precision):
		self.precision = precision
		self.relevant_docs = []
		self.irrelevant_docs = []
		self.relcount = 0
		self.irrelcount = 0
		pass
	
	def computeTfIdf(self):
		tfidf = TfidfVectorizer()
		result = tfidf.fit_transform(self.corpus)
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