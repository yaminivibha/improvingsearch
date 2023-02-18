from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def preprocess(docs):
    """Preprocesses the documents by removing stopwords and tokenizing"""
    docs = [docs.lower() for docs in docs]
    docs = [docs.translate(str.maketrans('', '', punctuation)) for docs in docs]
    docs = [word_tokenize(docs) for docs in docs]
    docs = [word for word in docs if word not in stopwords.words('english')]
    
    return docs 

# def get_ifidf_for_words(text):
#     tfidf_matrix= tfidf.transform([text]).todense()
#     feature_index = tfidf_matrix[0,:].nonzero()[1]
#     tfidf_scores = zip([feature_names[i] for i in feature_index], [tfidf_matrix[0, x] for x in feature_index])
#     return dict(tfidf_scores)