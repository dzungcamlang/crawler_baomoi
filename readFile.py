import os


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
