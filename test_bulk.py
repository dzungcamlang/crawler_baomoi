from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
import os

# for file in os.listdir("datatest"):
#     print(type(file))
def gendata():
    # mywords = ['foo', 'bar', 'baz']
    for filename in os.listdir("data"):
        with open(os.path.join('data', filename)) as f:
            contentMod = f.read().split('\n')
            yield {
                "_index": "baivietbaomoi",
                "_type": "baiviet",
                "doc": {
                    'title': contentMod[0],
                    'sum': contentMod[1],
                    'content': contentMod[2],
                    'time': contentMod[3],
                    'category': contentMod[4],
                    'tags': contentMod[5].split(','),
                    'source': contentMod[6],
                },
            }
def testdata():
    # mywords = ['foo', 'bar', 'baz']
    for filename in os.listdir("data"):
        with open(os.path.join('data', filename)) as f:
            content = f.read()
            contentMod = content.split('\n')
            if len(contentMod) == 10:
                print(content)
                print(filename)

def fillter_data():
    for filename in os.listdir("data"):
        with open(os.path.join('data', filename)) as f:
            content = f.read()
            contentMod = content.split('\n')
            if len(contentMod) != 7:
                print(filename)
                print(len(contentMod))
                os.remove(os.path.join('data', filename))
                # print(content)
                # print(filename)
def count_file():
    DIR = 'data/'
    fileCount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    print(fileCount)
# fillter_data()
# count_file()
bulk(es, gendata())
# res = es.search(index="baiviettest", body={"query": {"match_all": {}}})
# for hit in res['hits']['hits']:
#     print( hit["_source"])