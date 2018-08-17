import json
import requests
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def search_tags_by_category():
    query = {
        "query": {
            "bool": {
                "must": [],
                "must_not": [],
                "should": [
                    {
                        "term": {
                            "category.keyword": "Xã hội"
                        }
                    },
                    {
                        "term": {
                            "category.keyword": "Văn hóa"
                        }
                    },
                    {
                        "term": {
                            "category.keyword": "Kinh tế"
                        }
                    },
                    {
                        "term": {
                            "category.keyword": "Giáo dục"
                        }
                    },
                    {
                        "term": {
                            "category.keyword": "Pháp luật"
                        }
                    },
                    {
                        "term": {
                            "category.keyword": "Thể thao"
                        }
                    },
                    {
                        "term": {
                            "category.keyword": "Giải trí"
                        }
                    }
                ]
            }

        },
        "aggs": {
            "tag": {
                "terms": {
                    "field": "category.keyword"
                },
                "aggs": {
                    "category": {
                        "terms": {
                            "field": "tags.keyword",
                            "size": 20
                        }
                    }
                }
            }
        }
    }
    return es.search(index='baivietbaomoi2', body=query)


def search_tags_by_month():
    query = {
        "aggs": {
            "tag": {
                "terms": {
                    "field": "tags.keyword",
                    "size": 20
                },
                "aggs": {
                    "incidents_per_month": {
                        "date_histogram": {
                            "field": "time",
                            "interval": "month"
                        }

                    }
                }
            }
        }
    }
    return es.search(index='baivietbaomoi2', body=query)


res = search_tags_by_category()
# res = search_tags_by_month()
print(res['aggregations'])
