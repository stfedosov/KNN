from elasticsearch import Elasticsearch
import Config
from optparse import OptionParser
from Utils import get_docs
import sys

settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "doc": {
            "properties": {
                "Id": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "ParentId": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "PostTypeId": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "AcceptedAnswerId": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "CreationDate": {
                    "type": "date"
                },
                "ClosedDate": {
                    "type": "date"
                },
                "CommunityOwnedDate": {
                    "type": "date"
                },
                "LastEditDate": {
                    "type": "date"
                },
                "LastActivityDate": {
                    "type": "date"
                },
                "CreationMonth": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "CreationDay": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "CreationHour": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "CreationMinute": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "OwnerDisplayName": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "OwnerUserId": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "LastEditorUserId": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "LastEditorDisplayName": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "Score": {
                    "type": "integer"
                },
                "ViewCount": {
                    "type": "integer"
                },
                "AnswerCount": {
                    "type": "integer"
                },
                "FavoriteCount": {
                    "type": "integer"
                },
                "CommentCount": {
                    "type": "integer"
                },
                "Body": {
                    "type": "text",
                    "store": "true"
                },
                "Title": {
                    "type": "text",
                    "store": "true"
                },
                "Tags": {
                    "type": "text"
                }
            }
        }
    }
}

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
indices = es.indices
if indices.exists(Config.collection):
    indices.delete(index=Config.collection)
indices.create(index=Config.collection, ignore=400, body=settings)
indices.refresh(index=Config.collection)


def main(file):
    with open(file) as f:
        total = 0
        while True:
            data = get_docs(f, BULK_SIZE)
            bulk_data = []
            for d in data:
                op_dict = {
                    "index": {
                        "_index": Config.collection,
                        "_type": 'doc',
                        "_id": d['Id']
                    }
                }
                bulk_data.append(op_dict)
                bulk_data.append(d)
            if bulk_data:
                es.bulk(index=Config.collection, body=bulk_data)
                total += BULK_SIZE
                print('\n Indexed %d documents (approximately)' % total)
            else:
                return


if __name__ == '__main__':
    parser = OptionParser()
    args = parser.parse_args()
    if len(args[1]) == 0:
        parser.error('The Posts.xml file location must be specified')

    BULK_SIZE = 10000

    main(args[1][0])
    sys.exit()
