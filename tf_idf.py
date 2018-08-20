from sklearn.feature_extraction.text import TfidfVectorizer
from readFile import read_content
import pandas as pd
import os
from

DIR = 'datatest'
# DIR = 'data'
# result = {}


def tokenize(text):
    return word_tokenize(text)

vectorizer = TfidfVectorizer()
list_content = list(map(lambda f: read_content(
    DIR + '/' + f), os.listdir(DIR)))
matrix = vectorizer.fit_transform(list_content).todense()
matrix = pd.DataFrame(matrix, columns=vectorizer.get_feature_names())
# sum over each document (axis=0)
top_words = matrix.sum(axis=0).sort_values(ascending=False)
print(top_words)
