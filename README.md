# KNN
K-nearest neighbors feature evaluation for Solr &amp; Elastic search engines

KNN-classifiers based on Solr & Elastic built-in features. 
The goal is to extract top "K nearest neighbour" documents from the index.

Structure of this project:

 - DataExtractorForElastic.py & DataExtractorForSolr.py - data extractors and indexers for two famous search engines Solr & Elastic.

 - Config.py - configuration file with all necessary endpoints inside

 - Utils.py - useful utils

 - Main.py - main class to execute

 - KClassifier.py - KNN-classifier to extract top K documents from Solr and Elastic

Prerequisite for the environment:

 - Solr & Elastic
 - Python 3 
 - Sci-Fi StackExchange dataset
