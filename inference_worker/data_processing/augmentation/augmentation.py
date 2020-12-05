#
# Created by Maksim Eremeev (mae9785@nyu.edu)
#

import nlpaug.augmenter.word as naw
from textaugment import Translate


class Augmentation:
    def __init__(self, bert_model='distilbert-base-multilingual-cased', target_language='ja'):
        self.vec_aug = naw.ContextualWordEmbsAug(model_path=bert_model, action="substitute")
        self.translation_aug = Translate(src="ru", to=target_language)

    def __call__(self, text):
        text = self.translation_aug.augment(text)
        text = self.vec_aug.augment(text)
        return text