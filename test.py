import json
import requests
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# r = requests.get('http://localhost:9200')
# j = {'a': 123}
# es.index(index='sw', doc_type='people', id=1, body=j)
# # r = es.get(index='sw', doc_type='people', id=1)
# print(r)
# def gendata():
#     mywords = ['foo', 'bar', 'baz']
#     for word in mywords:
#         yield {
#             "_index": "mywords",
#             "_type": "document",
#             "doc": {"word": word},
#         }
res = es.search(index="mywords", body={"query": {"match_all": {}}})
for hit in res['hits']['hits']:
    print( hit["_source"])

# bulk(es, gendata())
