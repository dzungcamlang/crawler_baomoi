from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

es.indices.delete(index='baivietbaomoi_scrapy', ignore=[400, 404])
