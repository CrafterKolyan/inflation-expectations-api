#
# Created by Maksim Eremeev (mae9785@nyu.edu)
#

import re

import pymorphy2
from nltk.stem import PorterStemmer
from nltk.tokenize.toktok import ToktokTokenizer


class Preprocessing:
    def __init__(self, stopwords):
        self.rgc = re.compile('[^a-zа-яё0-9-_]')
        self.tokenizer = ToktokTokenizer()
        self.lemmatizer = pymorphy2.MorphAnalyzer()
        self.stemmer = PorterStemmer()

        with open(stopwords, 'r') as f:
            self.stopwords = set(f.read().split('\n'))

    def tokenize_words(self, text, preprocess=True, **preprocess_params):
        if not preprocess:
            return text.split()
        return self.preproc(text, **preprocess_params).split()

    @staticmethod
    def __num_non_letter_symbols(token):
        result = re.findall('[^a-zа-яё]', token)
        return len(result)

    @staticmethod
    def __has_consonant(token):
        result = re.findall(r"[^aeuioejаеиоуэюя]", token)
        return len(result) != 0

    def preproc(self, text, check_stopwords=True, check_length=True,
                use_lemm=False, use_stem=False, include_tf=False):
        s = re.sub("\n", r" ", text)
        s = re.sub("'", r" ", s)
        s = re.sub("`", " ", s)
        s = re.sub('[\U00010000-\U0010ffff]', '', s)
        s = s.lower()
        s = self.rgc.sub(" ", s)

        final_agg = []
        tf = {}

        for i, token in enumerate(self.tokenizer.tokenize(s)):
            if check_length and (len(token) < 3 or (token.isnumeric() and len(token) != 4)):
                continue
            if token[0].isnumeric():
                continue
            if not self.__has_consonant(token):
                continue
            symbs = self.__num_non_letter_symbols(token)
            if (len(token) < 5 and symbs > 0) or (symbs > 4) or (symbs > len(token) / 2 + 1):
                continue
            if token[-1] == '-' or token[0] == '-':
                continue
            if use_lemm:
                token = self.lemmatizer.parse(token)[0].normal_form
            if use_stem:
                token = self.stemmer.stem(token)
            if token not in self.stopwords or not check_stopwords:
                if token not in tf:
                    tf[token] = 0
                tf[token] += 1
                final_agg.append(token)

        if include_tf:
            return ' '.join(final_agg), tf
        return ' '.join(final_agg)
