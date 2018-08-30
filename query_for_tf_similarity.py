from test_tf_idf import cal_tf_idf_dict, print_counter_top
from tf_idf_for_counter import cal_tf_idf_dict_counter, get_cosine, get_euclide, get_jaccard
from elasticsearch import Elasticsearch
from underthesea import ner
from collections import Counter
from read_file import write_counter, read_counter
from underthesea_to_analysis import create_counter_tokenize

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


def find_post_to_compare(index, category, sumary):
    page = query_post(index)

    hits = page['hits']['hits']
    for post in hits:
        # print(post['_source']['category'])
        if post['_source']['category'] == category:
            return post['_source']
    scroll_size = page['hits']['total']  # Start scrolling
    sid = page['_scroll_id']
    count_page = 0
    count = 20
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
                return post['_source']


def append_to_top_content(result, counter_content, post_source, distance_type):
    counter_content_compare = create_counter_tokenize(post_source['content'])
    if distance_type == 'cosine':
        similarity = get_cosine(counter_content, counter_content_compare)
    if distance_type == 'euclide':
        similarity = get_euclide(counter_content, counter_content_compare)
    if distance_type == 'jaccard':
        similarity = get_jaccard(counter_content, counter_content_compare)
    # print(result.keys())
    for position in result.keys():
        if similarity > result[position]['similarity']:
            result[position]['title'] = post_source['title']
            result[position]['cat'] = post_source['category']
            result[position]['similarity'] = similarity
            break
    return result


def find_most_common_content(index, counter_content, distance_type):
    page = query_post(index)
    hits = page['hits']['hits']
    # for post in hits:
    #     print(post['category'])
    sid = page['_scroll_id']
    hits = page['hits']['hits']
    result = {
        '1st': {
            'similarity': 0
        },
        '2st': {
            'similarity': 0
        },
        '3st': {
            'similarity': 0
        },
        '4st': {
            'similarity': 0
        },
        '5st': {
            'similarity': 0
        },
    }
    for post in hits:
        # category_dict = append_content_noun_person_for_post(
        #     category_dict, post['_source'])
        result = append_to_top_content(result, counter_content, post[
                                       '_source'], distance_type)
        # result.append(post['source']['userid'] + '' + post['_source']['docId'])
        # print(post['source']['userid'] + '' + post['_source']['docId'])
        # print(len(result))
    scroll_size = page['hits']['total']  # Start scrolling
    count_page = 0
    count = 20
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
            result = append_to_top_content(result,
                                           counter_content, post['_source'], distance_type)
            # category_dict = append_tags_for_post(
            #     category_dict, post['_source'])
            # result.append(post['source']['userid'] +
            #               '' + post['_source']['docId'])
            # print(post['source']['userid'] + '' + post['_source']['docId'])
            # print(len(result))
    # Do something with the obtained page
    # file_io.write_new_file('data/post_id/' + term.replace(' ', '_'), result)
    return result


def find_category_dict(index):
    page = query_post(index)
    hits = page['hits']['hits']
    # for post in hits:
    #     print(post['category'])
    sid = page['_scroll_id']
    hits = page['hits']['hits']
    result = []
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
        # category_dict = append_content_noun_person_for_post(
        #     category_dict, post['_source'])
        category_dict = counter_tags(
            category_dict, post['_source'])
        # result.append(post['source']['userid'] + '' + post['_source']['docId'])
        # print(post['source']['userid'] + '' + post['_source']['docId'])
        # print(len(result))
    scroll_size = page['hits']['total']  # Start scrolling
    count_page = 0
    count = 20
    while count > 0:
        count -= 1
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
            # category_dict = append_content_noun_person_for_post(
            #     category_dict, post['_source'])
            category_dict = counter_tags(
                category_dict, post['_source'])
            # category_dict = append_tags_for_post(
            #     category_dict, post['_source'])
            # result.append(post['source']['userid'] +
            #               '' + post['_source']['docId'])
            # print(post['source']['userid'] + '' + post['_source']['docId'])
            # print(len(result))
    # Do something with the obtained page
    # file_io.write_new_file('data/post_id/' + term.replace(' ', '_'), result)
    return category_dict


def print_result(dict_result):
    for pos in dict_result:
        print(pos + '\t' + str(dict_result[pos]) + '\n')

if __name__ == '__main__':
    post_source = find_post_to_compare(
        'baivietbaomoi_scrapy', "Thể thao", 'Ronaldo')
    counter_content = create_counter_tokenize(post_source['content'])
    common_post_by_cosine = find_most_common_content(
        'baivietbaomoi_scrapy', counter_content, 'cosine')
    common_post_by_euclide = find_most_common_content(
        'baivietbaomoi_scrapy', counter_content, 'euclide')
    common_post_by_jaccard = find_most_common_content(
        'baivietbaomoi_scrapy', counter_content, 'jaccard')
    print(post_source['title'])
    print('cosine')
    print_result(common_post_by_cosine)
    print('euclide')
    print_result(common_post_by_euclide)
    print('jaccard')
    print_result(common_post_by_jaccard)
