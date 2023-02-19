"""
Helper functions related to query execution, response handling, and input processing
"""
from googleapiclient.discovery import build
import regex as re


def printQueryParams(dev_key, search_engine_id, query, desired_precision):
    """
    Prints the arguments sent to the Google Custom Search API
    """
    print("Parameters:")
    print("Client key  = " + str(dev_key))
    print("Engine key  = " + str(search_engine_id))
    print("Query       = " + str(query))
    print("Precision   = " + str(desired_precision))
    print("Google Search Results: ")
    print("======================")
    return
    
def getQueryResult(dev_key, search_engine_id, query, top_k):
    """
    Get the top 10 results for a given query from Google Custom Search API
    """
    # TODO: build class for QueryExecutor so service is an instance variable
    service = build("customsearch", "v1", developerKey=dev_key)

    full_res = service.cse().list(q=query, cx=search_engine_id,).execute()

    return full_res["items"][0:top_k + 1]


def parseResults(res):
    """
    Returns the URL, Title, Summary of a Google Custom Search API Result
    """

    parsed_res = [
        " URL: " + res["formattedUrl"],
        "Title: " + res["title"],
        "Summary: " + res["snippet"],
    ]

    return parsed_res


def combineResults(res):
    # TODO: Parse URL (to get whats between the / / after the .com)
    # url = res["formattedUrl"]

    return res["title"] + " " + res["snippet"]


def getRelevanceFeedback(top10_res):
    """
    Returns a list of relevant docs and list of irrelevant docs
    as marked by the user
    """
    relevant_docs = []
    irrelevant_docs = []

    for i, res in enumerate(top10_res):
        print("Result " + str(i + 1))
        print("[")
        print("\n ".join(parseResults(res)))
        print("]\n")

        while True:
            user_relevance = input("Relevant (Y/N)?")

            # To guard against bad inputs, we only accept "Y", "y", "N", "n"
            # as valid relevance feedback
            if not re.match("^[Y,y,N,n]{1,1}$", user_relevance):
                print('Please type in Y or N (or y or n)')
            else:
                if user_relevance == "Y" or user_relevance == "y":
                    relevant_docs.append(combineResults(res))
                else:
                    irrelevant_docs.append(combineResults(res))
                break

    # print(f"Relevant docs:\n {relevant_docs}")
    # print(f"====================")
    # print(f"Relevant docs, Processed:\n {preprocess(relevant_docs)}")
    # print(f"Irrelevant docs: {irrelevant_docs}")
    return relevant_docs, irrelevant_docs


def printFeedback(query, expanded_terms, desired_precision, cur_precision):
    """
    Returns query feedback summary to user
    """
    print("======================")
    print("FEEDBACK SUMMARY")
    print(f"Query: {query}")
    print(f"Precision: {cur_precision}")
    if cur_precision < desired_precision:
        print(f"Still below the desired precision of {desired_precision}")
        print("Indexing results ....")
        print("Indexing results ....")
        print(f"Augmenting by {expanded_terms}")
    else:
        print("Desired precision reached, done")
    return

def computePrecision(num_rel, num_docs):
    """
    Computes the precision of the web search results using
    the formula below:
    
    precision = |relevant docs that are retrieved| / |retrieved docs|
    """
    return num_rel / num_docs