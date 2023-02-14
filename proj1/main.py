#!/usr/bin/env python
# -*- coding: utf-8 -*-
# source: https://github.com/googleapis/google-api-python-client/blob/main/samples/customsearch/main.py

import pprint
import sys
import utils

def main():
	# Build a service object for interacting with the API. Visit
	# the Google APIs Console <http://code.google.com/apis/console>
	# to get an API key for your own application.

	# !!! is invoking the program with python3 xx.py ok? or how do you get it to run with the ./run thing?
	if len(sys.argv) != 5:
		print("Usage: python3 main.py <google api key> <google engine id> <precision> <query>")
		sys.exit(-1)
	
	dev_key = sys.argv[1]
	search_engine_id = sys.argv[2]
	desired_precision = sys.argv[3]
	query = sys.argv[4]

	res = utils.executeQuery(dev_key, search_engine_id, query, desired_precision)

	relevant_docs = utils.getRelevanceFeedback(res)
	
	



if __name__ == "__main__":
	main()
