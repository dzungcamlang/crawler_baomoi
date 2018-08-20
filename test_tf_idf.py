import math
from textblob import TextBlob as tb


def tf(word, blob):
    return blob.count(word) / len(blob)


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)


def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))


def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

# if __name__ == '__main__':
#     document1 = ['ahohoho', 'ahihi', 'ahuhu', 'ahohoho', 'ahehe']
#     document2 = ['ahihi', 'ahuhu', 'ahihi', 'ahohoho', 'ahihi']
#     document3 = ['ahuhu', 'ahohoho', 'ahuhu', 'ahohoho', 'ahuhu']
#     bloblist = [document1, document2, document3]


def cal_tf_idf_dict(blobdict):
    with open('result_tfidf.txt', 'w') as f:
        for blob, blob_value in blobdict.items():
            f.write("\n\nTop words in category {}".format(blob))
            scores = {word: tfidf(word, blob_value, blobdict.items())
                      for word in blob_value}
            sorted_words = sorted(
                scores.items(), key=lambda x: x[1], reverse=True)
            for word, score in sorted_words[:20]:
                f.write("\nWord: {}, TF-IDF: {}".format(word, round(score, 5)))
                # f.write(str(content))
