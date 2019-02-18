__author__ = 'maria'

#coding=utf-8
import re

import verse_analysis.lines as lin

# # сформировали lisf_of_lines объектами класса Line
def create_list_of_lines(text):
    tmp_list_of_lines = []
    for line in text:
        new_line = lin.Line(line)
        tmp_list_of_lines.append(new_line)

    return tmp_list_of_lines


class Strofa:
    def __init__(self, raw_strofas):
        """Constructor"""
        self.raw_strofas = raw_strofas
        self.lisf_of_lines = create_list_of_lines(raw_strofas) # list of objects (class: Line)



    def compare_phonetix_words(self):
        phonetix_word_list = []
        for line in self.lisf_of_lines:
            tmp_phonetix_word = line.form_endings_for_rythm()
            phonetix_word_list.append(tmp_phonetix_word)

        for ph_w in phonetix_word_list:
            schema = ""
            for w in ph_w:
                schema = schema + w.shemaCc
            print(schema)










