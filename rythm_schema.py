
__author__ = 'maria'

#coding=utf-8
import re
import io
import pymorphy2
from pymystem3 import Mystem
import numpy


# Стих или строка стихового текста Fпо сути является последовательностью
# k ритмических слов Рi=br(i)Аids(i),
# где Аi– ударный слог,
# br(i) – предударная цепочка r(i) безударных слогов,
# ds(i) – заударная цепочка s(i) безударных слогов
#
# с объемом слогов |Рi|=(r(i)+1+s(i)):
# F = ∏i=1,2,..kРi = ∏i=1,2,..kbr(i)Аids(i) = br(1)А1ds(1) br(2)А2ds(2)… br(k)Аkds(k).
# Можно представить Fчерез последовательность (k-1) междуиктовых интервалов Vi=ds(i)br(i+1)
# со слоговым объемом |Vi|=(s(i)+r(i+1)), примыкающих к ударному слогу:
# F= br(1)(∏i=1,2,..(k-1)Si)Аkds(k) = br(1)(∏i=1,2,..(k-1)Аids(i)br(i+1))Аkds(k).

#  (|Vi|max+1) ≤  |Рi|, то места их ударения обозначат сильные места
# (|Vi|max+1) ≤  r(i) или (|Vi|max+1) ≤  s(i),
# то это означает, что имеет место пропуск метрического ударения в предударной или заударной цепочке.


pre = ["а","в","и","к","на","не","о","по","при","про","с","у","со","то","или","для","над","из","за","да","ни","ко","во","об","обо","без","безо","через","чрез","между","что","чтоб","чтобы","как","где","перед","пред","передо","предо","уж","но","от","до","дабы","коли","аки","ан","под","коль","изо","хоть","ведь"]
post = ["б","бы","же","ли","ль","ж"]

def get_rythm_words(line, kind):
    # kind = 0 - raw_word
    # kind = 1 - stressed word


    line_words = []
    tmp_word = []
    ln_ar = line.by_words
    ln_ar_sz = len(ln_ar)-1
    for iter, word in enumerate(ln_ar):
        if iter < ln_ar_sz:
            if word.raw_word.lower() in pre and (((ln_ar[iter + 1]).raw_word).lower() not in pre and ((ln_ar[iter + 1]).raw_word).lower() not in post):
                tmp_word.append(word)

            if word.raw_word.lower() in pre and  ((ln_ar[iter + 1]).raw_word).lower() in pre:
                tmp_word.append(word)

            if word.raw_word.lower() in post and (((ln_ar[iter + 1]).raw_word).lower() not in pre and ((ln_ar[iter + 1]).raw_word).lower() not in post):
                tmp_word.append(word)
                line_words.append(tmp_word)
                tmp_word = []

            if word.raw_word.lower() in post and ((ln_ar[iter + 1]).raw_word).lower() in pre:
                tmp_word.append(word)
                line_words.append(tmp_word)
                tmp_word = []

            if word.raw_word.lower() in post and ((ln_ar[iter + 1]).raw_word).lower() in post:
                tmp_word.append(word)

            if word.raw_word.lower() not in pre and word.raw_word.lower() not in post and (((ln_ar[iter + 1]).raw_word).lower() not in pre and ((ln_ar[iter + 1]).raw_word).lower() not in post):
                tmp_word.append(word)
                line_words.append(tmp_word)
                tmp_word = []


            if word.raw_word.lower() not in pre and word.raw_word.lower() not in post and (((ln_ar[iter + 1]).raw_word).lower() in post):
                tmp_word.append(word)

            if word.raw_word.lower() not in pre and word.raw_word.lower() not in post and (((ln_ar[iter + 1]).raw_word).lower() in pre):
                tmp_word.append(word)
                line_words.append(tmp_word)
                tmp_word = []

        if iter == ln_ar_sz:
                tmp_word.append(word)
                line_words.append(tmp_word)




    line_words_words = []
    for line in line_words:
        line_words_item = []
        if kind == 0:
            for item in line:
                line_words_item.append(item.raw_word)
        if kind == 1:
            for item in line:
                line_words_item.append((item.stress_word)[0])
        line_words_words.append(line_words_item)

    return line_words_words





