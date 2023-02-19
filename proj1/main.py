#!/usr/bin/env python
# -*- coding: utf-8 -*-
# source: https://github.com/googleapis/google-api-python-client/blob/main/samples/customsearch/main.py

import sys
import utils
from expandedQuery import *

TOP_K = 10

def main():
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.

    if len(sys.argv) != 5:
        print(
            "Usage: python3 main.py <google api key> <google engine id> <precision> <query>"
        )
        sys.exit(-1)

    dev_key = sys.argv[1]
    search_engine_id = sys.argv[2]
    desired_precision = float(sys.argv[3])
    query = sys.argv[4]

    cur_precision = -1

    while True:
        if cur_precision == 0:
            print("Precision of 0. Terminating...")
            break
        utils.printQueryParams(dev_key, search_engine_id, query, desired_precision)
        res = utils.getQueryResult(dev_key, search_engine_id, query, TOP_K)

        # Program should terminate if less than 10 results are returned.
        if len(res) < 10:
                # TODO: reference behavior if there's less than 10 docs? test "alksdjfal;ksdjf" (keyboard smash query)
                print("Less than 10 results returned, done")
                break
        relevant_docs, irrelevant_docs = utils.getRelevanceFeedback(res)
        cur_precision = utils.computePrecision(len(relevant_docs), TOP_K)
        
        # Program should terminate of desired precision of query is reached
        if cur_precision >= desired_precision:
                utils.printFeedback(query, "", desired_precision, cur_precision)
                break

        expanded_query = ExpandedQuery(
            query, cur_precision, relevant_docs, irrelevant_docs
        )
        added_terms, query = expanded_query.getModifiedQueryVector()
        print(f"expanded query: {query}")
        # expanded_query.sortQueryTerms()

        utils.printFeedback(query, added_terms, desired_precision, cur_precision)



if __name__ == "__main__":
    main()
