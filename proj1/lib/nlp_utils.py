"""utils for preprocessing and tokenizing the documents"""

from string import punctuation
from typing import List

from nltk.tokenize import word_tokenize
from sklearn.feature_extraction import text


def preprocess(doc: str) -> str:
    """Preprocesses the documents by lowercasing and removing punctuation"""
    doc = doc.lower()
    return doc.translate(str.maketrans("", "", punctuation))


def tokenize(doc: str) -> List[str]:
    """Tokenizes the documents"""
    return word_tokenize(doc)


def remove_stop_words(doc: List[str]) -> List[str]:
    """Removes stop words from the documents"""
    stopwords = text.ENGLISH_STOP_WORDS
    return [word for word in doc if word not in stopwords]
