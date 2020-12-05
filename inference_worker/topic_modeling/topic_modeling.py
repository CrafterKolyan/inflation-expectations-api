#
# Created by Maksim Eremeev (mae9785@nyu.edu)
#

import artm
import os
import numpy as np
from matplotlib import pyplot as plt


class TopicModeling:
    def __init__(self, source_file, batches_folder='batches', batch_size=100):
        self.source_file = source_file
        self.batches_folder = batches_folder
        self.batch_vectorizer = artm.BatchVectorizer(data_path=self.source_file, data_format="vowpal_wabbit",
                                                     target_folder=self.batches_folder, batch_size=batch_size)

        dict_name = os.path.join(self.batches_folder, "dictionary.dict")
        self.dictionary = artm.Dictionary()
        if not os.path.exists(dict_name):
            self.dictionary.gather(batches_folder)
            self.dictionary.save(dict_name)
        else:
            self.dictionary.load(dict_name)

    def fit_model(self, model, num_collection_passes):
        model.fit_offline(batch_vectorizer=self.batch_vectorizer, num_collection_passes=num_collection_passes)

    def add_level(self, hmodel, num_topics, parent_level_weight=None, topic_name_prefix='child'):
        if parent_level_weight is None
            model = hmodel.add_level(num_topics=num_topics)
            model.initialize(self.dictionary)
            return model
        model = hmodel.add_level(num_topics=num_topics,
                                 topic_names=[f'{topic_name_prefix}_topic_' + str(i) for i in range(num_topics)],
                                 parent_level_weight=parent_level_weight)
        model.initialize(self.dictionary)
        return model

    @staticmethod
    def init_hierarchical_model(class_ids):
        score = [artm.PerplexityScore(name='perplexity_words', class_ids=['body']),
                 artm.PerplexityScore(name='perplexity_bigrams', class_ids=['bigrams'])]

        top_tokens = [artm.TopTokensScore(name='top_words', num_tokens=15, class_id='body'),
                      artm.TopTokensScore(name='top_bigrams', num_tokens=10, class_id='bigrams')]

        sparsity = [artm.SparsityThetaScore(name='sparsity_theta', eps=1e-6),
                    artm.SparsityPhiScore(name='sparsity_phi_words', class_id='words', eps=1e-6),
                    artm.SparsityPhiScore(name='sparsity_phi_bigrams', class_id='bigrams', eps=1e-6)]

        regularizers = [artm.DecorrelatorPhiRegularizer(tau=0, class_ids=['body'], name='decorr_words'),
                        artm.DecorrelatorPhiRegularizer(tau=0, class_ids=['bigram'], name='decorr_bigrams'),
                        artm.DecorrelatorPhiRegularizer(tau=0, class_ids=['categories'], name='decorr_categories'),
                        artm.SmoothSparseThetaRegularizer(tau=0, name='sparsity_theta'),
                        artm.SmoothSparsePhiRegularizer(tau=0, class_ids=['body'], name='sparsity_words'),
                        artm.SmoothSparsePhiRegularizer(tau=0, class_ids=['bigram'], name='sparsity_bigrams')]

        hmodel = artm.hARTM(class_ids=class_ids,
                            cache_theta=True,
                            reuse_theta=True,
                            scores=score + top_tokens + sparsity,
                            regularizers=regularizers,
                            theta_columns_naming='title')
        return hmodel

    @staticmethod
    def num_documents(filename):
        with open(filename, 'r') as f:
            s = f.read()
            t = s.split('\n')
            return len(t) - 1

    @staticmethod
    def show_perplexity(model, modality):
        plt.figure(figsize=(7, 7))
        plt.grid()
        plt.title(f'Perplexity for modality {modality}', fontsize=14)
        plt.plot(model.score_tracker[f'perplexity_{modality}'].value[1:])
        plt.show()

    @staticmethod
    def show_sparsity(model, matrix_modality):
        plt.figure(figsize=(7, 7))
        plt.grid()
        plt.title(f'Sparsity for {matrix_modality}', fontsize=14)
        plt.plot(model.score_tracker[f'sparsity_{matrix_modality}'].value[1:])
        plt.show()

    @staticmethod
    def results(self, model):
        self.show_perplexity(model, 'words')
        self.show_perplexity(model, 'bigrams')

        self.show_sparsity(model, 'theta')
        self.show_sparsity(model, 'phi_words')
        self.show_sparsity(model, 'phi_bigrams')

        print("Perplexity score on unigrams:", model.score_tracker['perplexity_words'].last_value)
        print("Perplexity score on bigrams", model.score_tracker['perplexity_bigrams'].last_value)
        print("Theta sparsity score", model.score_tracker['sparsity_theta'].last_value)
        print("Phi sparsity unigrams score", model.score_tracker['sparsity_phi_words'].last_value)
        print("Phi sparsity bigrams score", model.score_tracker['sparsity_phi_bigrams'].last_value)

    @staticmethod
    def topics(model):
        for topic_name in model.topic_names:
            print(topic_name + ': ', )
            try:
                print(", ".join(model.score_tracker['top_words'].last_tokens[topic_name]))
            except:
                print("\nNot enough unigrams in a topic")
            try:
                print(", ".join(model.score_tracker['top_bigrams'].last_tokens[topic_name]))
            except:
                print("\nNot enough bigrams in a topic")
            print()

    @staticmethod
    def get_psi(model, parent_model, level_idx):
        psi = model.get_psi()
        batch = artm.messages.Batch()
        batch_name = 'phi{level_idx}.batch'.format(level_idx=level_idx)

        with open(batch_name, "rb") as f:
            batch.ParseFromString(f.read())

        Ntw = np.zeros(len(parent_model.topic_names))

        for i, item in enumerate(batch.item):
            for (token_id, token_weight) in zip(item.field[0].token_id, item.field[0].token_weight):
                Ntw[i] += token_weight

        Nt1t0 = np.array(psi) * Ntw
        psi_bayes = (Nt1t0 / Nt1t0.sum(axis=1)[:, np.newaxis]).T
        indexes_child = np.argmax(psi_bayes, axis=0)
        return indexes_child

    @staticmethod
    def print_hierarchy_topics(model, parent_model, indexes_child):
        for i, topic_parent_name in enumerate(parent_model.topic_names):
            print(topic_parent_name + ':')
            print(' '.join(parent_model.score_tracker['top_words'].last_tokens[topic_parent_name]))
            print(' '.join(parent_model.score_tracker['top_bigrams'].last_tokens[topic_parent_name]))
            print('')

            for child in np.where(indexes_child == i)[0]:
                print('    ' + model.topic_names[child] + ': ')
                print(" ".join(model.score_tracker['top_words'].last_tokens[model.topic_names[child]]))
                print(" ".join(model.score_tracker['top_bigrams'].last_tokens[model.topic_names[child]]))
                print('')