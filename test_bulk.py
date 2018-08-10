from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
import os

for file in os.listdir("datatest"):
    print(type(file))
def gendata():
    # mywords = ['foo', 'bar', 'baz']
    for file in os.listdir("datatest"):
        f = open(file, "r")
        contentMod = f.read().split('\n')
        yield {
            "_index": "baiviettest",
            "_type": "document",
            "doc": {
                'title': contentMod[0],
                'sum'
                'content'
                'time'
                'category'
                'tags'
                'source'
            },
        }
# f=open("datatest/11111112.txt", "r")
# content = f.read()
# contentMod = content.split('\n')
# print(len(contentMod))
# print(content)

# res = es.search(index="mywords", body={"query": {"match_all": {}}})
# for hit in res['hits']['hits']:
#     print( hit["_source"])

# bulk(es, gendata())
