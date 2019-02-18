__author__ = 'maria'

#coding=utf-8
import re
import verse_analysis.lib_prep as lp

class Word:
    def __init__(self, raw_word):
        """Constructor"""
        self.raw_word = raw_word.lower()
        self.norm_word = lp.normalize(raw_word)
        self.stress_word, self.stress_word_probabilities = lp.find_word_stress_opt(raw_word.lower())
        self.probab_stress_list = lp.get_probab_stress(raw_word)
        self.POS = lp.POS(raw_word)
        self.shemaCc = lp.define_stress((self.stress_word)[0])


        def get_raw_word(self):  # Чтение
            return self.raw_word
        def set_raw_word(self, value):  # Запись
            self.raw_word = value


        def get_norm_word(self):  # Чтение
            return self.norm_word
        def set_norm_word(self, value):  # Запись
            self.norm_word = value


        def get_stress_word(self):  # Чтение
            return self.stress_word
        def set_raw_word(self, value):  # Запись
            self.stress_word = value