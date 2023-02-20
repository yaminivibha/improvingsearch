#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from QueryExpander import QueryExpander
from utils import QueryExecutor

TOP_K = 10

def main():
    """
    Main function that handles the control flow of the information retrieval system
    """

    if len(sys.argv) != 5:
        print(
            "Usage: python3 main.py <google api key> <google engine id> <precision> <query>"
        )
        sys.exit(-1)

    dev_key = sys.argv[1]
    search_engine_id = sys.argv[2]
    desired_precision = float(sys.argv[3])
    query = sys.argv[4]
    
    exec = QueryExecutor(dev_key, search_engine_id, desired_precision, TOP_K)
    
    # Set the current precision to -1 to indicate that the query has not been executed yet
    cur_precision = -1

    while True:
        # Program should terminate if the precision is 0
        if cur_precision == 0:
            print("Below desired precision, but can no longer augment the query")
            print("Terminating ...")
            break
        exec.printQueryParams(query)
        res = exec.getQueryResult(query)

        # Program should terminate if less than 10 results are returned.
        if len(res) < 10:
            print("Less than 10 results returned")
            print("Terminating ...")
            break
        relevant_docs, irrelevant_docs = exec.getRelevanceFeedback(res)
        cur_precision = exec.computePrecision(len(relevant_docs))

        # Program should terminate if desired precision of query is reached
        if cur_precision >= desired_precision:
            exec.printFeedback(query, "", cur_precision)
            break

        # Else, augment the query and repeat
        expander = QueryExpander(query, cur_precision, relevant_docs, irrelevant_docs)
        added_terms, _query = expander.getAddedWords()
        sorted_query = expander.sortQueryTerms()

        exec.printFeedback(query, added_terms, cur_precision)
        query = sorted_query

if __name__ == "__main__":
    main()
