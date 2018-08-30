from test_tf_idf import cal_tf_idf_dict, print_counter_top
from tf_idf_for_counter import find_sim_post, cal_tf_idf_dict_counter, get_cosine, get_euclide, get_jaccard
from elasticsearch import Elasticsearch
from collections import Counter
from read_file import write_counter, read_counter, read_counter_transform, read_counter_json
from underthesea_to_analysis import create_counter_tokenize
from multiprocessing import Pool
import os
import json

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def query_post(index):
    # Initialize the scroll
    return es.search(
        request_timeout=30,
        index=index,
        # doc_type='post',
        scroll='2m',
        size=50,
        # body={

        #     "query": {
        #         "bool": {
        #             "must": [
        #                 {
        #                     "term": {
        #                         "category.keyword": "{}".format(category)
        #                     }
        #                 }
        #             ],
        #             "must_not": [],
        #             "should": []
        #         }
        #     },
        #     # "size": 1,
        # }
    )


def find_post_to_compare(index, category):
    page = query_post(index)

    hits = page['hits']['hits']
    for post in hits:
        # print(post['_source']['category'])
        if post['_source']['category'] == category:
            return post
    scroll_size = page['hits']['total']  # Start scrolling
    sid = page['_scroll_id']
    count_page = 0
    count = 50
    while count > 0:
        count -= 1
        count_page += 1
        # print(count_page)
        # print('scroll size', scroll_size)
        # print("Scrolling...")
        page = es.scroll(scroll_id=sid, scroll='2m')
        # Update the scroll ID
        sid = page['_scroll_id']
        # Get the number of results that we returned in the last scroll
        scroll_size = len(page['hits']['hits'])
        hits = page['hits']['hits']
        for post in hits:
            # category_dict = append_content_noun_person_for_post(
            #     category_dict, post['_source'])
            if post['_source']['category'] == category:
                return post


def take_content_to_file(post):
    source = post['_source']
    counter = create_counter_tokenize(source['content'])
    write_counter(counter, post['_id'])


def take_thounsand_post_counter(index):
    page = query_post(index)
    p = Pool(5)
    hits = page['hits']['hits']
    # for post in hits:
    p.map(take_content_to_file, hits)
    # take_content_to_file(post)
    scroll_size = page['hits']['total']  # Start scrolling
    sid = page['_scroll_id']
    count_page = 0
    count = 20
    while count > 0:
        count -= 1
        count_page += 1
        print(count_page)
        # print('scroll size', scroll_size)
        # print("Scrolling...")
        page = es.scroll(scroll_id=sid, scroll='2m')
        # Update the scroll ID
        sid = page['_scroll_id']
        # Get the number of results that we returned in the last scroll
        scroll_size = len(page['hits']['hits'])
        hits = page['hits']['hits']
        # for post in hits:
        p.map(take_content_to_file, hits)
        # take_content_to_file(post)


def get_idf_file():
    result = Counter()
    DIR = 'datacounter_transform'
    for filename in os.listdir(DIR):
        with open(os.path.join(DIR, filename)) as f:
            dict_count = json.load(f)
            for k in dict_count:
                result[k] += 1
    DIR_DATA_IDF_COUNTER = 'data_idf'
    with open(os.path.join(DIR_DATA_IDF_COUNTER, 'data'), 'w') as f_to_writen:
        json.dump(result, f_to_writen)


def print_result(result, distance_type, vectorlizer_type):
    print(distance_type, vectorlizer_type)
    for idx, val in enumerate(result):
        post = get_post_from_id(val['_id'])
        print(post['_source']['category'] + '\t' +
              post['_source']['title'])


def get_post_from_id(_id):
    return es.get(index='baivietbaomoi_scrapy', doc_type='baiviet', id=_id)

if __name__ == '__main__':
    # take_thounsand_post_counter('baivietbaomoi_scrapy')
    # get_idf_file()
    cat = 'Thể thao'
    post = find_post_to_compare('baivietbaomoi_scrapy', cat)
    # print(post)
    _id = post['_id']
    post_des = get_post_from_id(_id)
    print(post_des['_source']['title'])
    result = find_sim_post(_id, 'cosine', 'tf')
    print_result(result, 'cosine', 'tf')
    result = find_sim_post(_id, 'euclide', 'tf')
    print_result(result, 'euclide', 'tf')
    result = find_sim_post(_id, 'jaccard', 'tf')
    print_result(result, 'jaccard', 'tf')
    result = find_sim_post(_id, 'cosine', 'tf_idf')
    print_result(result, 'cosine', 'tf_idf')
    result = find_sim_post(_id, 'euclide', 'tf_idf')
    print_result(result, 'euclide', 'tf_idf')
    result = find_sim_post(_id, 'jaccard', 'tf_idf')
    print_result(result, 'jaccard', 'tf_idf')
