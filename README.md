# KNN
K-nearest neighbors feature evaluation for Solr &amp; Elastic search engines

KNN classificators based on Solr & Elastic built-in features. Extracts top K nearest neighbours documents from index.

Here is the structure of this project:


DataExtractorForElastic.py & DataExtractorForSolr.py - data extractors and indexers for two famous search engines Solr & Elastic.

Config.py - configuration file with necessary endoints inside

Utils.py - some useful utils like document conversion

Main.py - main class to execute

KClassifier.py - K classifier to extract top K documents from index from Solr and Elastic
