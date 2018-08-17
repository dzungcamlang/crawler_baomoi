from collections import Counter


def write_file():
    c = Counter('abcdeabcdabcaba')
    with open('abc.txt', 'w') as f:
        for k, v in c.most_common():
            f.write("{} {}\n".format(k, v))


def read_file():
    with open('abc.txt', encoding='utf8') as f:
        dict_for_read = {}
        for line in f:
            key, value = line.strip().split(' ')
            dict_for_read[key] = value
        return Counter(dict_for_read)

a = read_file()
print(a)
