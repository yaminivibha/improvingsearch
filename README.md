# CS6111 Advanced Databases Project 1
###### Yamini Ananth yva2002, Erin Liang ell2147


## File Structure

```
├── proj1
│   ├── lib
│   │   ├── nlp_utils.py
│   ├── main.py
│   ├── QueryExpander.py
│   ├── QueryExecutor.py
├── requirements.txt
├── README.md
├── setup.sh
└── query_transcript.txt
```

| Filename           | Description                                                                                        |
|--------------------|----------------------------------------------------------------------------------------------------|
| `requirements.txt` | List of packages to install                                                                        |
| `setup.sh`         | Bash script for setting up environment                                                             |
| `QueryExpander.py` | Creates class for query expansion using Rocchio's algorithm; sorts query terms using n-gram counts |
| `QueryExecutor.py` | Creates class for query execution, response handling, and input processing                         |
| `main.py`          | Main function that handles the control flow of the information retrieval system                    |
| `nlp_utils.py`     | Utilities for processing documents + urls                                                          |


## How To Run
1. Navigate to the repository
```cd <your/path/to/improvingsearch>```
2. Make sure the setup script is executable by changing the file permissions:
```chmod +x setup.sh```
3. From the top level repository, install all the requirements with:
```bash setup.sh```
4. Navigate to the src folder:
```cd src```
5. Then run the project with:
```python3 main.py <google api key> <google engine id> <precision> <query>```
6. Example command with query “6111 databases” and desired precision of 0.9
```python3 main.py <google api key> <google engine id> 0.9 "6111 databases"```

## Credentials
Below are the credentials needed to test the information retrieval system. These credentials were generated following [these instructions](http://www.cs.columbia.edu/~gravano/cs6111/proj1.html#:~:text=As a second step%2C you will have to sign up for the Programmable Search Engine service (https%3A//programmablesearchengine.google.com/about/)%3A)

* Google Custom Search Engine JSON API Key
```AIzaSyDQTz-AzhWHv-Qbk3ADyPG4hFb3Z6PkLHM ```
* Google Engine ID:
```45add40315937647f```




## TODO: Design Description
- [explaining the general structure of your code; what its main high-level components are and what they do]
- [describing all external libraries that you use in your code]

## TODO: Query-Modification Method
- [how you select the new keywords to add in each round]
- [how you determine the query word order in each round]

## TODO: Testing: Google Custom Search Engine JSON API Key and Engine ID

## TODO: Additional Info
