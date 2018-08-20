import math
from textblob import TextBlob as tb


def tf(word, blob):
    return blob.count(word) / len(blob)


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)


def idf(word, bloblist):
    return math.log(len(bloblist) / (n_containing(word, bloblist)))


def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

if __name__ == '__main__':
    document1 = ['ahohoho', 'ahihi', 'ahuhu', 'ahohoho', 'ahehe']
    document2 = ['ahihi', 'ahuhu', 'ahihi', 'ahohoho', 'ahihi']
    document3 = ['ahuhu', 'ahohoho', 'ahuhu', 'ahohoho', 'ahuhu']
    bloblist = [document1, document2, document3]
    for i, blob in enumerate(bloblist):
        print("Top words in category {}".format(i + 1))
        scores = {word: tfidf(word, blob, bloblist) for word in blob}
        sorted_words = sorted(
            scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:3]:
            print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
