from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
import os

# for file in os.listdir("datatest"):
#     print(type(file))


def gendata():
    # mywords = ['foo', 'bar', 'baz']
    for filename in os.listdir("data"):
        with open(os.path.join('data', filename), encoding='utf8') as f:
            contentMod = f.read().split('\n')

            yield {
                "_index": "baivietbaomoi2",
                "_type": "baiviet",
                'title': contentMod[0],
                'sum': contentMod[1],
                'content': contentMod[2],
                'time': contentMod[3],
                'category': contentMod[4],
                'tags': contentMod[5].split(','),
                'source': contentMod[6],
            }


def testdata():
    # mywords = ['foo', 'bar', 'baz']
    for filename in os.listdir("data"):
        with open(os.path.join('data', filename), encoding='utf8') as f:
            content = f.read()
            contentMod = content.split('\n')
            if len(contentMod) != 7:
                print(content)
                print(filename)


def fillter_data():
    for filename in os.listdir("data"):
        with open(os.path.join('data', filename), encoding='utf8') as f:
            content = f.read()
            contentMod = content.split('\n')
            if len(contentMod) != 7:
                print(filename)
                print(len(contentMod))
                os.remove(os.path.join('data', filename))
                # print(content)
                # print(filename)


def count_file():
    DIR = 'datasegment/'
    fileCount = len([name for name in os.listdir(
        DIR) if os.path.isfile(os.path.join(DIR, name))])
    print(fileCount)
# fillter_data()
# testdata()
count_file()
# bulk(es, gendata())
# res = es.search(index="baiviettest", body={"query": {"match_all": {}}})
# for hit in res['hits']['hits']:
#     print( hit["_source"])
