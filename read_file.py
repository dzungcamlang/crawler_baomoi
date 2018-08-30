from collections import Counter
import os
import json
from tf_idf_for_counter import cal_tf_idf_of_file


def read_content(file_name):
    count = 0
    with open(file_name, encoding='utf8') as f:
        for line in f:
            if count == 2:
                return line
            count += 1


def read_date(file_name):
    count = 0
    with open(file_name, encoding='utf8') as f:
        for line in f:
            if count == 3:
                a = line.split(' ')[0][0:8]
                return a
            count += 1


def write_segment(file_name, content_segmented):
    with open('datasegment/' + 'seg_' + file_name, 'w') as f:
        f.write(str(content_segmented))


def save_result_segment(content):
    with open('segment.txt', 'w') as f:
        f.write(str(content))


def write_counter(counter, file_name):
    with open(file_dir, 'w') as f:
        for item in counter.most_common():
            [key, value] = item
            string = key + ' ' + str(value) + '\n'
            f.write(str(string))
    f.close()


def transform_counter():
    DIR = 'datacounter'
    DIR_DES = 'datacounter_transform'
    for filename in os.listdir(DIR):
        with open(os.path.join(DIR_DES, filename), 'w') as f_des:
            with open(os.path.join(DIR, filename), encoding='utf8') as f:
                result = {}
                for line in f:
                    item = line.strip().split(' ')
                    value = int(item.pop())
                    key = ' '.join(item)
                    result[key] = value
                json.dump(result, f_des)
            f.close()
        f_des.close()


def count_file(DIR):
    fileCount = len([name for name in os.listdir(
        DIR) if os.path.isfile(os.path.join(DIR, name))])
    return fileCount


def transform_to_if_idf():
    DIR = 'datacounter_transform'
    DIR_DES = 'datacounter_if_idf'
    counter_corpus = Counter()
    with open('data_idf/data') as f_idf:
        counter_corpus = json.load(f_idf)
    total = count_file('datacounter_transform')
    for filename in os.listdir(DIR):
        with open(os.path.join(DIR_DES, filename), 'w') as f_des:
            with open(os.path.join(DIR, filename)) as f:
                result = json.load(f)
                result = cal_tf_idf_of_file(result, counter_corpus, total)
                json.dump(result, f_des)
            f.close()
        f_des.close()


def read_counter(file_name):
    count_dict = {}
    with open('datacounter/' + file_name, 'r') as f:
        for line in f:
            print(line)
            item_count = line.strip().split(' ')
            count_dict[item_count[0]] = int(item_count[1])
    return Counter(count_dict)


def read_counter_transform(file_dir):
    count_dict = {}
    with open(file_dir, 'r') as f:
        for line in f:
            item_count = line.strip().split(':')
            print(line)
            # print(item_count[0])
            # if item_count[0] == ':':
            #     continue
            count_dict[item_count[0]] = int(item_count[1])
    return Counter(count_dict)


def read_counter_json(file_dir):
    count_dict = {}
    with open(file_dir, 'r') as f:
        for line in f:
            item_count = line.strip().split(':')
            print(line)
            # print(item_count[0])
            # if item_count[0] == ':':
            #     continue
            count_dict[item_count[0]] = int(item_count[1])
    return Counter(count_dict)


if __name__ == '__main__':
    # a = Counter({'a': 2, 'b': 1, 'c': 5, 'd': 2})
    # write_counter(a, 'ahihi')
    # result = read_counter('ahihi')
    # print(result)
    # transform_counter()
    transform_to_if_idf()
