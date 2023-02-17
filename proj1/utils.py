"""
Helper functions related to query execution, response handling, and input processing
"""
from googleapiclient.discovery import build


def getQueryResult(dev_key, search_engine_id, query, desired_precision):
    """Get the top 10 results for a given query from Google Custom Search API"""
    print("Parameters:")
    print("Client key  = " + str(dev_key))
    print("Engine key  = " + str(search_engine_id))
    print("Query       = " + str(query))
    print("Precision   = " + str(desired_precision))
    print("Google Search Results: ")
    print("======================")

    service = build("customsearch", "v1", developerKey=dev_key)

    full_res = service.cse().list(q=query, cx=search_engine_id,).execute()

    # TODO: skip non-html files
    # may have to return the entire result from this fn?
    return full_res["items"][0:11]


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
    Returns corpus (dict) with relevance information as marked by the user
    Return format:
    {docid: {Summary: " ", "Relevant": 1}, ....}
    """
    relevant_docs = []
    irrelevant_docs = []

    for i, res in enumerate(top10_res):
        # TODO: use full body text instead of summary?
        print("Result " + str(i + 1))
        print("[")
        print("\n ".join(parseResults(res)))
        print("]\n")

        # TODO: more robust input checking; reprompt if invalid input
        user_relevance = input("Relevant (Y/N)?")
        if user_relevance == "Y" or user_relevance == "y":
            relevant_docs.append(combineResults(res))
        else:
            irrelevant_docs.append(combineResults(res))

    # print(f"Relevant docs: {relevant_docs}")
    # print(f"Irrelevant docs: {irrelevant_docs}")
    return relevant_docs, irrelevant_docs


def printFeedback(query, target_precision, cur_precision):
    """
    Returns query feedback summary to user
    """
    print("Query: " + query)
    print("Precision: " + cur_precision)
    if cur_precision < target_precision:
        print("Still below the desired precision of " + target_precision)
    else:
        print("Desired precision reached, done")
    return
