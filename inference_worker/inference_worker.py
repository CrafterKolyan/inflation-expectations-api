#
# Created by Maksim Eremeev (mae9785@nyu.edu)
#

import numpy as np
from worker_compose import noexcept
import artm
from data_processing import ProcessBankData
from topmine_tools import

class InferenceWorker:
    def __init__(self, model_path, stopwords, ngram_list):
        self.model = artm.load_model(model_path)
        self.preprocessor = ProcessBankData(stopwords)

        self.phi_labels = self.model.get_phi(class_id='labels')
        self.phi_labels = np.array(self.phi_labels)

        self.ngram_list = ngram_list

    def count_proba(self, theta_vec):
        return self.phi_labels.dot(np.array(theta_vec))

    def create_vowpal_wabbit(self, doc):
        vw += f"{doc['id']} "
        for modality in doc:
            if modality == 'id':
                continue
            if modality in ['words', 'bigrams', 'trigrams', 'fourgrams']:
                doc[modality] = ' '.join(
                    list(filter(lambda token: tf[token] >= 2, doc[modality].split(' ')[:-1]))
                )
            vw += f"|{modality} {doc[modality]} "
        return vw

    @noexcept('{"data": [], "errors": ["fatal error in inference_worker"]}')
    def run(self, text):
        preprocessed_text = self.preprocessor(text)
        transformed_text = topmine_tools.add_ngrams(self.ngram_list, [text], None)

        vowpal_wabbit = self.create_vowpal_wabbit(transformed_text)

        theta_vec = self.model.transform(vowpal_wabbit)

        return np.argmax(self.count_proba(theta_vec))
