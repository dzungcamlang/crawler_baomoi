import math
from textblob import TextBlob as tb
from collections import Counter
import json
import os
# from query_for_list_counter_tfidf import print_result


def tf(most_common_item, counter):
    return most_common_item[1] / sum(counter.values())


def n_containing(most_common_item, counters):
    cat = most_common_item[0]
    return sum(1 for counter in counters if cat in counter.keys())


def idf(most_common_item, counters):
    return math.log(len(counters) / (1 + n_containing(most_common_item, counters)))


def tfidf(most_common_item, counter, counters):
    # print(type(counters))
    return tf(most_common_item, counter) * idf(most_common_item, counters)

# if __name__ == '__main__':
#     document1 = ['ahohoho', 'ahihi', 'ahuhu', 'ahohoho', 'ahehe']
#     document2 = ['ahihi', 'ahuhu', 'ahihi', 'ahohoho', 'ahihi']
#     document3 = ['ahuhu', 'ahohoho', 'ahuhu', 'ahohoho', 'ahuhu']
#     bloblist = [document1, document2, document3]


def find_sim_post(_id, distance_type, vectorlizer_type):
    vec1 = Counter()
    vec2 = Counter()
    result = [
        {'_id': '', 'score': 0},
        {'_id': '', 'score': 0},
        {'_id': '', 'score': 0},
        {'_id': '', 'score': 0},
        {'_id': '', 'score': 0},
        {'_id': '', 'score': 0},
        {'_id': '', 'score': 0},
        {'_id': '', 'score': 0}
    ]
    DIR = ''
    if vectorlizer_type == 'tf':
        DIR = 'datacounter_transform'
    if vectorlizer_type == 'tf_idf':
        DIR = 'datacounter_if_idf'
    with open(os.path.join(DIR, _id)) as f1:
        vec1 = Counter(json.load(f1))
    f1.close()
    for filename in os.listdir(DIR):
        with open(os.path.join(DIR, filename)) as f_to_compare:
            if filename == _id:
                continue
            vec2 = Counter(json.load(f_to_compare))
            score = 0
            if distance_type == 'cosine':
                score = get_cosine(vec1, vec2)
            if distance_type == 'euclide':
                score = get_euclide(vec1, vec2)
            if distance_type == 'jaccard':
                score = get_jaccard(vec1, vec2)
            for idx, val in enumerate(result):
                if score == val['score']:
                    break
                if score > val['score']:
                    val_to_insert = {'_id': filename, 'score': score}
                    result.insert(idx, val_to_insert)
                    result.pop()
                    break
    # print_result(result, distance_type, vectorlizer_type)
    return result


def cal_tf_idf_dict_counter(category_dict_counter):
    # print('111111' + str(type(category_dict_counter)))
    # with open('result_tfidf.txt', 'w') as f:
    # print(blobdict)
    for cat, counter in category_dict_counter.items():
        print("Top tags in category {}".format(cat))
        scores = {c[0]: tfidf(c, counter, category_dict_counter.values())
                  for c in counter.most_common(20)}
        sorted_words = sorted(
            scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:20]:
            print("\ttag: {}, TF-IDF: {}".format(word, round(score, 5)))
            # f.write(str(content))


def cal_tf_idf_of_file(counter_item, counter_corpus, total):
    result = Counter()
    for k in counter_item.keys():
        if_term = counter_item[k] / sum(counter_item.values())
        idf_term = math.log(total / counter_corpus[k])
        result[k] = if_term * idf_term
    return result


def print_counter_top(category_dict, type_count):
    for k, value in category_dict.items():
        print("Top {} in category {}".format(type_count, k))
        # print(value)
        for i in value.most_common()[:20]:
            print(type_count, i[0], i[1])
            # print("\t{}: {}, times: {}".format(type_count, i[0], i[1]))


def norm_counter(counter):
    norm = dict(counter)
    sum_count = sum(norm.values())
    for k, v in norm.items():
        norm[k] = v / sum_count
    return norm


def get_cosine(vec1, vec2):
    vec1 = norm_counter(vec1)
    vec2 = norm_counter(vec2)
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def get_euclide(vec1, vec2):
    vec1 = norm_counter(vec1)
    vec2 = norm_counter(vec2)
    set_key_1 = set(vec1.keys())
    set_key_2 = set(vec2.keys())
    intersection = set_key_1 & set_key_2
    only_1 = set_key_1 - set_key_2
    only_2 = set_key_2 - set_key_1
    distance = float(sum([(vec1[x] - vec2[x])**2 for x in intersection]))
    distance += float(sum([(vec1[x])**2 for x in only_1]))
    distance += float(sum([(vec2[x])**2 for x in only_2]))
    distance = math.sqrt(distance)
    sim = 1 / (1 + distance)
    return sim


def get_jaccard(vec1, vec2):
    set_key_1 = set(vec1.keys())
    set_key_2 = set(vec2.keys())
    distance = len(set_key_1 ^ set_key_2) / len(set_key_1 | set_key_2)
    sim = 1 - distance
    return sim


# if __name__ == '__main__':
#     vec1 = 'ahuhu ahihi hohoho'
#     vec2 = 'ahuhu ahehe hohoho'
#     vec1_trans = Counter(vec1.split(' '))
#     vec2_trans = Counter(vec2.split(' '))
#     print(vec1_trans)
#     print(vec2_trans)
#     print('get_cosine: ' + str(get_cosine(vec1_trans, vec2_trans)))
#     print('get_euclide: ' + str(get_euclide(vec1_trans, vec2_trans)))
#     print('get_jaccard: ' + str(get_jaccard(vec1_trans, vec2_trans)))
