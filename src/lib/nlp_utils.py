"""utils for preprocessing and tokenizing the documents"""

from string import punctuation
from typing import List
from urllib.parse import urlparse

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


def processRelDocs(relevant_docs: List[str]) -> List[List[str]]:
    """
    Processes the relevant docs by removing stop words and tokenizing
    """
    processed_rel_docs = []
    for doc in relevant_docs:
        doc = preprocess(doc)
        doc = tokenize(doc)
        doc = remove_stop_words(doc)
        processed_rel_docs.append(doc)
    return processed_rel_docs


def urlParse(url: str) -> str:
    """Parse URL to get the path as a string of words (no punctuation)"""
    url_path = urlparse(url).path
    translator = str.maketrans(
        punctuation, " " * len(punctuation)
    )  # map punctuation to space
    return url_path.translate(translator)
