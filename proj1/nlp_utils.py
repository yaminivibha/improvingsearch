import nltk.stopwords
import nltk.tokenize


def preprocess(docs):
    """Preprocesses the documents by removing stopwords and tokenizing"""
    docs = [docs.lower() for docs in docs]
    docs = [word_tokenize(docs) for docs in docs]
    docs = [word for word in docs if word not in stopwords.words('english')]
    
    return docs

