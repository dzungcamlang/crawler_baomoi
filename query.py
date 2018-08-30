from test_tf_idf import cal_tf_idf_dict, print_counter_top
from tf_idf_for_counter import cal_tf_idf_dict_counter
from elasticsearch import Elasticsearch
from underthesea import ner, word_tokenize
from collections import Counter
from multiprocessing import Pool, Process, Manager


def filter_noun_person(content):
    a = ner(content)
    list = []
    for i in a:
        for u in i:
            if u == 'Np':
                list.append(i[0])
    return list


def append_tags_for_post(category_dict, post_source):
    category_adding = post_source['category']
    tags = post_source['tags']
    if category_adding in category_dict:
        category_dict[category_adding].extend(tags)

    return category_dict


def append_content_noun_person_for_post(category_dict, post_source):
    category_adding = post_source['category']
    content_noun = filter_noun_person(post_source['sum'])
    if category_adding in category_dict:
        category_dict[category_adding].extend(content_noun)

    return category_dict


# def counter_tags(category_dict_counter_tags, post_source):
#     category_adding = post_source['category']
#     counter_tags = Counter(post_source['tags'])
#     if category_adding in category_dict_counter_tags:
#         category_dict_counter_tags[category_adding] += counter_tags

#     return category_dict_counter_tags


def counter_tags(category_dict, post):
    post_source = post['_source']
    category_adding = post_source['category']
    counter_tags = Counter(post_source['tags'])
    if category_adding in category_dict:
        category_dict[category_adding] += counter_tags

    return category_dict


def find_category_dict(index):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    # Initialize the scroll
    page = es.search(
        request_timeout=30,
        index=index,
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

    # category_dict = {
    #     "Xã hội": [],
    #     "Thế giới": [],
    #     "Văn hóa": [],
    #     "Kinh tế": [],
    #     "Giáo dục": [],
    #     "Pháp luật": [],
    #     "Thể thao": [],
    #     "Giải trí": []
    # # }
    # manager = Manager()

    # category_dict = manager.dict()
    category_dict = {
        "Xã hội": Counter(),
        "Thế giới": Counter(),
        "Văn hóa": Counter(),
        "Kinh tế": Counter(),
        "Giáo dục": Counter(),
        "Pháp luật": Counter(),
        "Thể thao": Counter(),
        "Giải trí": Counter()
    }
    for post in hits:
        # Process(target=counter_tags, args=(
        #     category_dict, post['_source'])).start()
        # for post in hits:
        # category_dict = append_content_noun_person_for_post(
        #     category_dict, post['_source'])
        category_dict = counter_tags(
            category_dict, post)
    # result.append(post['source']['userid'] + '' + post['_source']['docId'])
    # print(post['source']['userid'] + '' + post['_source']['docId'])
    # print(len(result))
    scroll_size = page['hits']['total']  # Start scrolling
    count_page = 0
    # count = 50
    while scroll_size > 0:
        # count -= 1
        count_page += 1
        print(count_page)
        print('scroll size', scroll_size)
        print("Scrolling...")
        page = es.scroll(scroll_id=sid, scroll='2m')
        # Update the scroll ID
        sid = page['_scroll_id']
        # Get the number of results that we returned in the last scroll
        scroll_size = len(page['hits']['hits'])
        hits = page['hits']['hits']
        for post in hits:
            # Process(target=counter_tags, args=(
            #     category_dict, post['_source'])).start()
            # for post in hits:
            # category_dict = append_content_noun_person_for_post(
            #     category_dict, post['_source'])
            category_dict = counter_tags(
                category_dict, post)
        # category_dict = append_tags_for_post(
        #     category_dict, post['_source'])
        # result.append(post['source']['userid'] +
        #               '' + post['_source']['docId'])
        # print(post['source']['userid'] + '' + post['_source']['docId'])
        # print(len(result))
    # Do something with the obtained page
    # file_io.write_new_file('data/post_id/' + term.replace(' ', '_'), result)
    return category_dict


if __name__ == '__main__':
    category_dict = find_category_dict('baivietbaomoi_scrapy')
    # print_counter_top(category_dict, 'tags')
    cal_tf_idf_dict_counter(category_dict)
