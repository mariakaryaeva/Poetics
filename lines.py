__author__ = 'maria'

#coding=utf-8
import re
import verse_analysis.lib_prep as lp
import verse_analysis.words as wd

prepositives = ["а","в","и","к","на","не","о","по","при","про","с","у","со","то","или","для","над","из","за","да","ни","ко","во","об","обо","без","безо","через","чрез","между","что","чтоб","чтобы","как","где","перед","пред","передо","предо","уж","но","от","до","дабы","коли","аки","ан","под","коль","изо","хоть","ведь"]
postpositives = ["б","бы","же","ли","ль","ж"]


def create_words_list(line):
    words = lp.tokenize(lp.clean_text(line))
    words_list = []
    for word in words:
        words_list.append(wd.Word(word))

    return words_list

def get_number_of_syllables(line):
    vowels = set(r'аеёиоуыэюя')
    count = 0
    for letter in line:
        if letter.lower() in vowels:
            count = count + 1
    return count



class Line:
    def __init__(self, raw_line):
        """Constructor"""
        self.raw_line = raw_line
        self.text_only_line = lp.clean_text(raw_line)
        self.by_words = create_words_list(raw_line) # list of objects (words) (class: Word)
        self.syllables_number = get_number_of_syllables(raw_line)
        self.rythm_lines = {}  # {номер рифмующийся строки: ранк}
        self.stress_schema = "" # схема ударений CCcCCc
    def get_rythm_lines(self):
        return self.rythm_lines

    def set_rythm_lines(self, value):
        self.rythm_lines = value

    def get_stress_schema(self):
        return self.stress_schema

    def set_stress_schema(self, value):
        self.stress_schema = value

    def form_endings_for_rythm(self):
        endings = []
        flag = False  # лежит или не лежит слово основное слово в эндинге
        for word in reversed(self.by_words):
            if (word.raw_word).lower() in postpositives and flag == False:
                endings.append(word)
            if (word.raw_word).lower() in prepositives and flag == True:
                endings.append(word)
            if ((word.raw_word).lower() not in postpositives) and ((word.raw_word).lower() not in prepositives) and flag == False:
                flag = True
                endings.append(word)
            else:
                if ((word.raw_word).lower() not in postpositives) and ((word.raw_word).lower() not in prepositives) and flag == True:
                    break


        return list(reversed(endings))







    # def form_endings_for_rythm(self):
    #     inapprop_POS = ["NPRO", "PRED", "PREP", "CONJ", "PRCL", "INTJ"]
    #     endings = []
    #     flag = False  # лежит или не лежит слово основное слово в эндинге
    #     for word in reversed(self.by_words):
    #         # print(word+" "+ POS(word))
    #         if word.POS not in inapprop_POS and flag == True:
    #             break
    #         if word.POS not in inapprop_POS and flag == False:
    #            # if len(endings) == 0:
    #             flag = True
    #             endings.append(word)
    #
    #         if word.POS in inapprop_POS:
    #             endings.append(word)
    #
    #     return list(reversed(endings))