"""
Helper functions related to query execution, response handling, and input processing
"""
from googleapiclient.discovery import build
import regex as re
from typing import List, Tuple

class QueryExecutor:
    """
    Class that handles query execution, response handling, and input processing
    """
    def __init__(self, dev_key: str, search_engine_id: str,  
                 desired_precision: float, top_k: int):
        """
        Parameters:
        dev_key             = developer key for Google Custom Search API
        search_engine_id    = search engine ID for Google Custom Search API
        desired_precision   = desired precision of the query
        top_k               = number of results to return from Google Custom Search API
        Instance Variables:
        googleservice       = Google Custom Search API service
        num_docs            = number of results to return from Google Custom Search API
        """

        self.dev_key = dev_key
        self.num_docs = top_k
        self.search_engine_id = search_engine_id
        self.desired_precision = desired_precision
        self.top_k = top_k
        self.googleservice = build("customsearch", "v1", developerKey=self.dev_key)
        #....
        #also make relevant docs and irrelevant docs instance vars? 
        # Maybe not because we want to use the same build for every loop right? or that's the lowk goal?
        # self.relevant_docs = []
        # self.irrelevant_docs = []
        
    def printQueryParams(self, query: str) -> None:
        """
        Prints the arguments sent to the Google Custom Search API
        """
        print("Parameters:")
        print("Client key  = " + str(self.dev_key))
        print("Engine key  = " + str(self.search_engine_id))
        print("Query       = " + str(query))
        print("Precision   = " + str(self.desired_precision))
        print("Google Search Results: ")
        print("======================")
        return
    
    def getQueryResult(self, query: str) -> None:
        """
        Get the top 10 results for a given query from Google Custom Search API
        """
        full_res = self.googleservice.cse().list(q=query, cx=self.search_engine_id,).execute()

        return full_res["items"][0:self.top_k + 1]

    def computePrecision(self, num_rel: int) -> float:
        """
        Computes the precision of the web search results using
        the formula below:
        
        precision = |relevant docs that are retrieved| / |retrieved docs|
        """
        return num_rel / self.top_k

    def printFeedback(self, query: str, expanded_terms: str, cur_precision: float) -> None:
        """
        Returns query feedback summary to user
        """
        print("======================")
        print("FEEDBACK SUMMARY")
        print(f"Query: {query}")
        print(f"Precision: {cur_precision}")
        if cur_precision < self.desired_precision:
            print(f"Still below the desired precision of {self.desired_precision}")
            print("Indexing results ....")
            print("Indexing results ....")
            print(f"Augmenting by {expanded_terms}")
        else:
            print("Desired precision reached, done")
        return
    
    def getRelevanceFeedback(self, top10_res: List) -> Tuple[List[str], List[str]]:
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
        return relevant_docs, irrelevant_docs


def parseResults(res: List) -> List[str]:
    """
    Returns the URL, Title, Summary of a Google Custom Search API Result
    """

    parsed_res = [
        " URL: " + res["formattedUrl"],
        "Title: " + res["title"],
        "Summary: " + res["snippet"],
    ]

    return parsed_res


def combineResults(res: List) -> str:
    # TODO: Parse URL (to get whats between the / / after the .com)
    # url = res["formattedUrl"]

    return res["title"] + " " + res["snippet"]
