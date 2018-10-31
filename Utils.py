import re
from datetime import datetime

rowRe = re.compile('^\s*<row')  # detects a row
attrRe = re.compile('(\w+)="(.*?)"')  # extracts all attribues and values
cleanupRe = re.compile('<[^<]+?>|[\r\n]+|\s+')  # strips out html and extra whitespace
tagsRe = re.compile('&lt;(.*?)&gt;')  # splits tags into a list
intRe = re.compile('^\d+$')  # determines if field is an integer
escapeRe = re.compile('&lt;/?.+?&gt;|&[^q][#\w]+;')  # pulls our XML excapes eg &lt;


def get_docs(f, bulk_size):
    docs = []
    for i, line in enumerate(f):
        line = line.decode('utf-8').strip()
        # skip line if not a row
        if rowRe.match(line) is None:
            continue

        # build the document to be indexed
        doc = {}
        for field, val in attrRe.findall(line):
            # strip whitespace and skip field if empty value
            val = val.strip()
            if not val:
                continue

            # cleanup title and body by stripping html and whitespace
            if field in ['Body', 'Title']:
                val = escapeRe.sub(' ', val)
                val = cleanupRe.sub(' ', val)

            # make sure dates are in correct format
            elif field in ['CreationDate', 'LastActivityDate', 'LastEditDate']:
                # 2008-07-31T21:42:52.667
                val = '%sZ' % val

                # parse creation month, day, hour, and minute
                if field == 'CreationDate':
                    dateObj = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S.%fZ')
                    doc['CreationMonth'] = dateObj.strftime('%B')
                    doc['CreationDay'] = dateObj.strftime('%A')
                    doc['CreationHour'] = dateObj.strftime('%H')
                    doc['CreationMinute'] = dateObj.strftime('%M')

            # split tags into an array of tags
            elif field == 'Tags':
                val = ' '.join(tagsRe.findall(val))

            doc[field] = val
        docs.append(doc)

        if (i + 1) == bulk_size:
                return docs
    return docs
