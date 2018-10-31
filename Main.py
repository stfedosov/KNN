import sys

import KClassifier

if __name__ == '__main__':
    solr_params = {"q": "Id:8555",
                   "mlt.fl": ["Title", "Body"],
                   "fl": "Tags",
                   "fq": "Tags:*",
                   "rows": 1000,
                   "wt": "json"
                   }
    print('Solr classification:')
    print(KClassifier.classify_solr(params=solr_params))
    print('\n------------------------\n')
    elastic_params = {
        "query": {
            "more_like_this": {
                "fields": ["Title", "Body"],
                "like": {
                    "_index": "movies",
                    "_type": "doc",
                    "_id": "8723"
                }
            }
        }
    }
    elastic_params_with_filter = {
        "query": {
            "bool": {
                "must": [
                    {
                        "more_like_this": {
                            "fields": [
                                "Title",
                                "Body"
                            ],
                            "like": {
                                "_index": "movies",
                                "_type": "doc",
                                "_id": "8723"
                            }
                        }
                    }
                ],
                "filter": {
                    "range": {
                        "ViewCount": {
                            "gte": 851,
                            "lte": 1702
                        }
                    }
                }
            }
        }
    }
    print('\nElastic classification:')
    print(KClassifier.classify_elastic(params=elastic_params))
    print(KClassifier.classify_elastic(params=elastic_params_with_filter))
    sys.exit()
