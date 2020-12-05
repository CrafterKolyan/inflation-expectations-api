#
# Created by Maksim Eremeev (mae9785@nyu.edu)
#

import pandas as pd
import re
from .preprocessing import Preprocessing
from augmentation import Augmentation
from tqdm.auto import tqdm


class ProcessBankData:
    def __init__(self, stopwords):
        self.preprocesing = Preprocessing(stopwords=stopwords)
        self.augmentator = Augmentation()

    def __call__(self, df, augmentation=False):
        texts = []
        tf = {}

        for row in tqdm(df.index):
            record = df.iloc[row, :]

            if record['Язык'] != 'Русский':
                continue

            if pd.isna(record['Текст']):
                continue

            region = ''
            if not pd.isna(record['Регион']):
                region = '_'.join(record['Регион'].split(' '))

            source = record['Ссылка'].split('://')[1].split('/')[0]
            title = record['Заголовок']
            body = record['Текст']

            media_type = ''
            if not pd.isna(record['Тип медиа']):
                media_type = re.sub(':', ' ', record['Тип медиа'])
                media_type = '_'.join(media_type.split(' '))

            record_type = ''
            if not pd.isna(record['Тип сообщения']):
                record_type = re.sub(':', ' ', record['Тип сообщения'])
                record_type = '_'.join(record_type.split(' '))

            author = ''
            if not pd.isna(record['Автор']):
                author = re.sub(':', ' ', record['Автор'])
                author = '_'.join(author.split(' '))

            society = ''
            if not pd.isna(record['Сообщество']):
                society = re.sub(':', ' ', record['Сообщество'])
                society = '_'.join(society.split(' '))

            categories = ''
            if not pd.isna(record['Рубрики']):
                categories = record['Рубрики'].split(' |')
                for i, category in enumerate(categories):
                    category = re.sub(':', ' ', category)
                    category = '_'.join(category.split(' '))
                    categories[i] = category
                categories = ' '.join(categories)

            title, tf_title = self.preprocesing.preproc(title, use_lemm=True, check_length=True,
                                                        check_stopwords=True, include_tf=True)

            if not pd.isna(record['Дата']):
                date = record['Дата']
                date = '_'.join(date.split('.'))

            for word in tf_title:
                if word not in tf:
                    tf[word] = 0
                tf[word] += tf_title[word]

            body, tf_body = self.preprocesing.preproc(body, use_lemm=True, check_length=True,
                                                      check_stopwords=True, include_tf=True)

            for word in tf_body:
                if word not in tf:
                    tf[word] = 0
                tf[word] += tf_body[word]

            texts += [{'id': record['ID'], 'source': source, 'title': title,
                       'body': body, 'author': author, 'categories': categories,
                       'media_type': media_type, 'timestamp': date, 'region': region,
                       'record_type': record_type}]

            if augmentation:
                texts += [{'id': record['ID'], 'source': source, 'title': self.augmentator(title),
                           'body': self.augmentator(body), 'author': author, 'categories': categories,
                           'media_type': media_type, 'timestamp': date, 'region': region,
                           'record_type': record_type}]

        return texts, tf
