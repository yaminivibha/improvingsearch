#!/usr/bin/env python
# -*- coding: utf-8 -*-
# source: https://github.com/googleapis/google-api-python-client/blob/main/samples/customsearch/main.py

import pprint
import sys

from googleapiclient.discovery import build

def parse_res(res):
	"""
	Returns the URL, Title, Summary of a Google Custom Search API Result
	"""
	
	parsed_res = [" URL: " + res["formattedUrl"],
			 "Title: " + res["title"],
			"Summary: " + res["snippet"]]

	return parsed_res

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

	print("Parameters: ")
	print("Client key  = " + str(dev_key))
	print("Engine key  = " + str(search_engine_id))
	print("Query       = " + str(query))
	print("Precision   = " + str(desired_precision))
	print("Google Search Results: ")
	print("======================")

	service = build(
		"customsearch", "v1", developerKey=dev_key
	)

	full_res = (
		service.cse()
		.list(
			q=query,
			cx=search_engine_id,
	)
		.execute()
	)
	
	top10_res = full_res["items"][0:11]
	for i, res in enumerate(top10_res):
		print("Result " + str(i + 1))
		print("[")
		print("\n ".join(parse_res(res)))
		print("]\n")

		user_relevance = input("Relevant (Y/N)?")
		# TODO: input checking lol

	# pprint.pprint(top10_res)

	
	



if __name__ == "__main__":
	main()
