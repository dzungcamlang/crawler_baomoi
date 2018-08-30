from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

query = {
    "size": 0,
    "aggs": {
        "duplicateCount": {
            "terms": {
                "field": "name",
                "min_doc_count": 2
            },
            "aggs": {
                "duplicateDocuments": {
                    "top_hits": {}
                }
            }
        }
    }
}

res = es.search(index='baivietbaomoi_scrapy', body=query)
print(res)
