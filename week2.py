from underthesea import word_tokenize
import os
from collections import Counter
from readFile import read_content, read_date, write_segment, save_result_segment

# print(word_tokenize(sentence))
# DIR = 'datatest'
DIR = 'data'
result = {}
for idx, filename in enumerate(os.listdir(DIR)):
    print(idx)
    if idx > 100:
        break
    content = read_content(DIR + '/' + filename)
    conten_seg = word_tokenize(content)
    # write_segment(filename, conten_seg)
    date = read_date(DIR + '/' + filename)
    if date not in result:
        result[date] = Counter(conten_seg)
    else:
        result[date] += Counter(conten_seg)
    remove_sign = ['.', ',', '“', '”', '-', '(', ')', ':']
    for m in remove_sign:
        del result[date][m]

save_result_segment(result)
print(len(result))
