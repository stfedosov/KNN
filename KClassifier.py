import requests
from collections import defaultdict
import Config


def get_sorted_top_k(k, tagDict):
    if tagDict.__len__() == 0:
        print('Tags dictionary is empty!')
    sorted_k = sorted(tagDict, key=lambda x: tagDict[x], reverse=True)[:k]
    result = ''
    for item in sorted_k:
        result += item + ' '
    return result


def classify_solr(k=3, params=""):
    check_params(params)
    sess = requests.Session()
    resp = sess.get(url=Config.solr_url + Config.collection + "/mlt", params=params)

    if resp.status_code != 200:
        raise RuntimeError("HTTP Status " + str(resp))
    json = resp.json()
    if int(json["match"]["numFound"]) == 0:
        raise RuntimeError("no document with that id")
    count = int(json["response"]["numFound"])
    if count == 0:
        raise RuntimeError("no interesting terms in document")
    print('\nTotal hits count:%d' % count)
    tagDict = defaultdict(int)
    for tagList in json['response']['docs']:
        for tag in tagList['Tags'].split(' '):
            tagDict[tag] += 1
    return get_sorted_top_k(k, tagDict)


def check_params(params):
    if params.__len__() == 0:
        raise RuntimeError("params should not be empty!")


def classify_elastic(k=3, params=""):
    check_params(params)
    sess = requests.Session()
    resp = sess.post(url=Config.es_url + Config.collection + '/_search', json=params)
    if resp.status_code != 200:
        raise RuntimeError("HTTP Status " + str(resp))
    json = resp.json()
    count = len(json['hits']['hits'])
    if count == 0:
        raise RuntimeError("no document with that id")
    print('\nTotal hits count:%d' % json['hits']['total'])
    tagDict = defaultdict(int)
    for tagList in json['hits']['hits']:
        if not list(tagList['_source']).__contains__('Tags'):
            continue
        for tag in tagList['_source']['Tags'].split(' '):
            tagDict[tag] += 1
    return get_sorted_top_k(k, tagDict)
