from test_tf_idf import cal_tf_idf_dict
from elasticsearch import Elasticsearch


def append_tags_for_post(category_dict, post_source):
    category_adding = post_source['category']
    tags = post_source['tags']
    if category_adding in category_dict:
        category_dict[category_adding].extend(tags)

    return category_dict


def find_category_dict():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    # Initialize the scroll
    page = es.search(
        request_timeout=30,
        index='baivietbaomoi2',
        # doc_type='post',
        scroll='2m',
        size=50,
        # body={
        #     "query": {
        #         "bool": {
        #             "filter": [
        #                 {
        #                     "query_string": {
        #                         "fields": [
        #                             "message",
        #                             "content"
        #                         ],
        #                         "query": "\"{}\"".format(term)
        #                     }
        #                 },
        #                 {
        #                     "query_string": {
        #                         "fields": [
        #                             "docType"
        #                         ],
        #                         "query": "user_post"
        #                     }
        #                 }
        #             ],
        #             "must_not": [],
        #             "should": [],
        #             "minimum_should_match": 0
        #         }
        #     }
        # }
    )
    hits = page['hits']['hits']
    # for post in hits:
    #     print(post['category'])
    sid = page['_scroll_id']
    hits = page['hits']['hits']
    result = []

    category_dict = {
        "Xã hội": [],
        "Thế giới": [],
        "Văn hóa": [],
        "Kinh tế": [],
        "Giáo dục": [],
        "Pháp luật": [],
        "Thể thao": [],
        "Giải trí": []
    }
    for post in hits:
        category_dict = append_tags_for_post(category_dict, post['_source'])
        # result.append(post['source']['userid'] + '' + post['_source']['docId'])
        # print(post['source']['userid'] + '' + post['_source']['docId'])
        # print(len(result))
    scroll_size = page['hits']['total']  # Start scrolling
    count = 100
    while count > 0:
        count -= 1
        print('scroll size', scroll_size)
        print("Scrolling...")
        page = es.scroll(scroll_id=sid, scroll='2m')
        # Update the scroll ID
        sid = page['_scroll_id']
        # Get the number of results that we returned in the last scroll
        # scroll_size = len(page['hits']['hits'])
        hits = page['hits']['hits']
        for post in hits:
            category_dict = append_tags_for_post(
                category_dict, post['_source'])
            # result.append(post['source']['userid'] +
            #               '' + post['_source']['docId'])
            # print(post['source']['userid'] + '' + post['_source']['docId'])
            # print(len(result))
    # Do something with the obtained page
    # file_io.write_new_file('data/post_id/' + term.replace(' ', '_'), result)
    return category_dict


if __name__ == '__main__':
    category_dict = find_category_dict()
    # print(category_dict)
    cal_tf_idf_dict(category_dict)
