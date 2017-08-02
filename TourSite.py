# -*- coding: utf-8 -*-
"""
Created on 8/2/17
Author: Jihoon Kim
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


class TourSite:

    def __init__(self, document_path, name):
        self.doc = pd.read_csv(document_path)
        self.name = name

    def get_count_vectorizer(self, ngram=(1, 1)):
        "Return word count vector in Pandas Format"
        count_vectorizer = CountVectorizer(ngram_range=ngram)
        count = count_vectorizer.fit_transform(self.doc['review'])
        count = pd.DataFrame(count.toarray(), columns=count_vectorizer.get_feature_names())
        return count

    def get_tf_idf_vectorizer(self, ngram=(1, 1)):
        "Return tf-idf vector in Pandas Format"
        tf_idf_vectorizer = TfidfVectorizer(smooth_idf=False, ngram_range=ngram)
        tf_idf = tf_idf_vectorizer.fit_transform(self.doc['review'])
        tf_idf = pd.DataFrame(tf_idf.toarray(), columns=tf_idf_vectorizer.get_feature_names())
        return tf_idf

    def get_words(self, ngram=(1, 1)):
        "Return used words in the tour site"
        count_vectorizer = CountVectorizer(ngram_range=ngram).fit(self.doc['review'])
        df_words = pd.DataFrame({'word': count_vectorizer.get_feature_names(), 'site': self.name})
        return df_words
