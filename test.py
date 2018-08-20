import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from underthesea import word_tokenize
from readFile import read_content
import os


def tokenize(text):
    tokens = word_tokenize(text)
    # stems = []
    # for item in tokens:
    #     stems.append(PorterStemmer().stem(item))
    return tokens

# your corpus
DIR = 'datatest'
text = list(map(lambda f: read_content(
    DIR + '/' + f), os.listdir(DIR)))
# word tokenize and stem
text = [tokenize(txt.lower()) for txt in text]
vectorizer = CountVectorizer()
matrix = vectorizer.fit_transform(text).todense()
# transform the matrix to a pandas df
matrix = pd.DataFrame(matrix, columns=vectorizer.get_feature_names())
# sum over each document (axis=0)
top_words = matrix.sum(axis=0).sort_values(ascending=False)
print(top_words)
