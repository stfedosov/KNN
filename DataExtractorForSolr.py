import httplib
import sys
from optparse import OptionParser

import Config
from Utils import get_docs


def main(file):
    request(url=Config.solr_url + Config.collection + '/update?commit=true',
            body='<delete><query>*:*</query></delete>')
    with open(file) as f:
        while True:
            data = get_bulk_solr_doc_set(f, 10000)
            if data:
                request(url=Config.solr_url + Config.collection + '/update', body=data)
            else:
                return


def request(url="", method='POST', body=""):
    conn = httplib.HTTPConnection('localhost:8983')
    if method == 'POST':
        conn.request(method, url, body, {"Content-type": "text/xml"})
    else:
        conn.request(method, url, body)
    resp = conn.getresponse()

    print(resp.read())


def get_bulk_solr_doc_set(f, bulk_size):
    docs = get_docs(f, bulk_size)
    if docs:
        return "<add>" + '\n'.join([make_solr_doc(doc) for doc in docs]) + "</add>"


def make_solr_doc(doc):
    return '\n'.join(['<doc>'
                         , '\n'.join(['<field name="%s">%s</field>' % (key, doc[key]) for key in doc])
                         , '</doc>'])


if __name__ == '__main__':
    parser = OptionParser()
    args = parser.parse_args()
    if len(args[1]) == 0:
        parser.error('The Posts.xml file location must be specified')

    main(args[1][0])
    request(url=Config.solr_url + Config.collection + '/update?commit=true', method='GET')
    sys.exit()
