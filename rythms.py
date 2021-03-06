__author__ = 'maria'

#coding=utf-8
import re

# vowels = ["а", "о", "и", "е", "ё", "э", "ы", "у", "ю", "я"]
vowels = set(r'аеёиоуыэюя')


# =====================
# вход: rythm_detection("жа'лобщик","опа'лубщик")
# =====================
# результат:
# ['л', 'бщ', 'к']
# ['л', 'бщ', 'к']
# ['л', 'о', 'бщ', 'и', 'к']
# ['л', 'у', 'бщ', 'и', 'к']
# заударная
# схема:  # d#D#
# ======================



# rythm_detection("колпа'к","тюльпа'н")


# 1.а. ●В●В●, сороково'й / роково'й;
# 1.б. ●b●В●, прямота / хромо'та;
# 1.в. ●В●b●, тарака'н / старика'н;
# 1.г. ●b●b●, фразиро'вка / фрезеро'вка
# 2.а. ○В●В●, борода' / сковорода';
# 2.б.??? ○b●В●,булава' / пахлава';
# 2.в. ○В●b●, молотьба' / голытьба';
# 2.г. ○b●b●, чащоба' / чищоба.
#               Схемы раздвоенно богатых созвучий:
# 3.а. ●В○В●, сорОкОвой / порОхОвой;
# 3.б. ●b○В●, панОрама / пилОрама;
# 3.в. ●В○b●, зАваруха / зАвируха;
# 3.г. ●b○b●, приставать / проживать.
#               Схемы богатых созвучий:
# 4.а. ○В○В●, лЕбЕда / рЕзЕда;
# 4.б. ○b○В●, симпатя'га / работя'га;
# 4.в. ○В○b●, прОщелыга / мАмалыга;
# 4.г. ○b○b●, бума'га / колыма'га.
#               Схемы отдаленно сдвоенных созвучий:
# 5.а. ●В●В○, кАтЕрок / кОтЕлок;
# 5.б. ●b●В○, порЕшить / перЕжить;
# 5.в. ●В●b○, пОрулить / пОрошить;
# 5.г. ●b●b○, перегон / поролон.
#           Схемы отдаленных созвучий:
# 6.а. ○В●В○, шАрОмыга / тОрОпыга;
# 6.б. ○b●В○, чудОдей / брадОбрей;
# 6.в. ○В●b○, гУлеван / хУлиган;
# 6.г. ○b●b○, карапуз / перегруз.
#           Схемы вдвойне отдаленных созвучий:
# 7.а. ●В○В○, пОдОждать / пОмОгать;
# 7.б. ●b○В○, принИмать / прожИгать;
# 7.в. ●В○b○, пОлоскать / пОднимать;
# 7.г. ●b○b○, поливать / переждать.
# Схемы бедных созвучий:
# 8.а. ○В○В○, бАлАмут / пАрАшют;
# 8.б. ○b○В○, домОсед / языкОвед;
# 8.в. ○В○b○, пОстижение / вОлочение;
# 8.г. ○b○b○, табуретка / сеголетка.


def generate_schema_desc():
    d = {}
    d['*B*B*'] = [1, 'втройне богатые созвучия']
    d['*b*B*'] = [1, 'втройне богатые созвучия']
    d['*B*b*'] = [1, 'втройне богатые созвучия']
    d['*b*b*'] = [1, 'втройне богатые созвучия']

    d['0B*B*'] = [2, 'сдвоенно богатые созвучия']
    d['0b*B*'] = [2, 'сдвоенно богатые созвучия']
    d['0B*b*'] = [2, 'сдвоенно богатые созвучия']
    d['0b*b*'] = [2, 'сдвоенно богатые созвучия']

    d['*B0B*'] = [3, 'раздвоенно богатые созвучия']
    d['*b0B*'] = [3, 'раздвоенно богатые созвучия']
    d['*B0b*'] = [3, 'раздвоенно богатые созвучия']
    d['*b0b*'] = [3, 'раздвоенно богатые созвучия']

    d['0B0B*'] = [4, 'богатые созвучия']
    d['0b0B*'] = [4, 'богатые созвучия']
    d['0B0b*'] = [4, 'богатые созвучия']
    d['0b0b*'] = [4, 'богатые созвучия']

    d['*B*B0'] = [5, 'отдаленно сдвоенные созвучия']
    d['*b*B0'] = [5, 'отдаленно сдвоенные созвучия']
    d['*B*b0'] = [5, 'отдаленно сдвоенные созвучия']
    d['*b*b0'] = [5, 'отдаленно сдвоенные созвучия']

    d['0B*B0'] = [6, 'отдаленные созвучия']
    d['0b*B0'] = [6, 'отдаленные созвучия']
    d['0B*b0'] = [6, 'отдаленные созвучия']
    d['0b*b0'] = [6, 'отдаленные созвучия']

    d['*B0B0'] = [7, 'вдвойне отдаленные созвучия']
    d['*b0B0'] = [7, 'вдвойне отдаленные созвучия']
    d['*B0b0'] = [7, 'вдвойне отдаленные созвучия']
    d['*b0b0'] = [7, 'вдвойне отдаленные созвучия']

    d['0B0B0'] = [8, 'бедные созвучия']
    d['0b0B0'] = [8, 'бедные созвучия']
    d['0B0b0'] = [8, 'бедные созвучия']
    d['0b0b0'] = [8, 'бедные созвучия']

    d['&'] = [1, 'неточная мужская открытая рифма']
    d['*&'] = [1, 'точная мужская открытая рифма']
    d['#'] = [1, 'точная мужская закрытая рифма']
    d['0'] = [0, 'неточная мужская закрытая рифма']

    d['#D#'] = [1, 'точная женская закрытая рифма']
    d['#d#'] = [1, 'точная женская закрытая рифма']

    d['0D#'] = [2, 'отдаленно точная женская закрытая рифма']
    d['0d#'] = [2, 'отдаленно точная женская закрытая рифма']

    d['#D0'] = [3, 'отдаленно неточная женская закрытая рифма']
    d['#d0'] = [3, 'отдаленно неточная женская закрытая рифма']

    d['0D0'] = [4, 'неточная женская закрытая рифма']
    d['0d0'] = [4, 'неточная женская закрытая рифма']

    d['#D'] = [5, 'точная женская открытая рифма']
    d['#d'] = [5, 'точная женская открытая рифма']

    d['0D'] = [1, 'неточная женская открытая рифма']
    d['0d'] = [1, 'неточная женская открытая рифма']

    d['#D#D#'] = [1, 'точная дактилическая закрытая рифма']
    d['#D#d#'] = [1, 'точная дактилическая закрытая рифма']
    d['#d#D#'] = [1, 'точная дактилическая закрытая рифма']
    d['#d#d#'] = [1, 'точная дактилическая закрытая рифма']

    d['#D0D#'] = [2, 'ущербно точная дактилическая закрытая рифма']
    d['#D0d#'] = [2, 'ущербно точная дактилическая закрытая рифма']
    d['#d0D#'] = [2, 'ущербно точная дактилическая закрытая рифма']
    d['#d0d#'] = [2, 'ущербно точная дактилическая закрытая рифма']

    d['0D#D#'] = [3, 'отдаленно точная дактилическая закрытая рифма']
    d['0D#d#'] = [3, 'отдаленно точная дактилическая закрытая рифма']
    d['0d#D#'] = [3, 'отдаленно точная дактилическая закрытая рифма']
    d['0d#d#'] = [3, 'отдаленно точная дактилическая закрытая рифма']

    d['0D0D#'] = [4, 'отдаленно и ущербно точная дактилическая закрытая рифма']
    d['0D0d#'] = [4, 'отдаленно и ущербно точная дактилическая закрытая рифма']
    d['0d0D#'] = [4, 'отдаленно и ущербно точная дактилическая закрытая рифма']
    d['0d0d#'] = [4, 'отдаленно и ущербно точная дактилическая закрытая рифма']


    d['#D#D0'] = [5, 'отдаленно неточная дактилическая закрытая рифма']
    d['#D#d0'] = [5, 'отдаленно неточная дактилическая закрытая рифма']
    d['#d#D0'] = [5, 'отдаленно неточная дактилическая закрытая рифма']
    d['#d#d0'] = [5, 'отдаленно неточная дактилическая закрытая рифма']

    d['0D#D0'] = [6, 'отдаленно и усеченно неточная дактилическая закрытая рифма']
    d['0D#d0'] = [6, 'отдаленно и усеченно неточная дактилическая закрытая рифма']
    d['0d#D0'] = [6, 'отдаленно и усеченно неточная дактилическая закрытая рифма']
    d['0d#d0'] = [6, 'отдаленно и усеченно неточная дактилическая закрытая рифма']


    d['#D0D0'] = [7, 'отдаленно и ущербно неточная дактилическая закрытая рифма']
    d['#D0d0'] = [7, 'отдаленно и ущербно неточная дактилическая закрытая рифма']
    d['#d0D0'] = [7, 'отдаленно и ущербно неточная дактилическая закрытая рифма']
    d['#d0d0'] = [7, 'отдаленно и ущербно неточная дактилическая закрытая рифма']

    d['0D0D0'] = [8, 'неточная дактилическая закрытая рифма']
    d['0D0d0'] = [8, 'неточная дактилическая закрытая рифма']
    d['0d0D0'] = [8, 'неточная дактилическая закрытая рифма']
    d['0d0d0'] = [8, 'неточная дактилическая закрытая рифма']


    d['#D#D'] = [9, 'точная дактилическая открытая рифма']
    d['#D#d'] = [9, 'точная дактилическая открытая рифма']
    d['#d#D'] = [9, 'точная дактилическая открытая рифма']
    d['#d#d'] = [9, 'точная дактилическая открытая рифма']


    d['0D#D'] = [10, 'отдаленно точная дактилическая открытая рифма']
    d['0D#d'] = [10, 'отдаленно точная дактилическая открытая рифма']
    d['0d#D'] = [10, 'отдаленно точная дактилическая открытая рифма']
    d['0d#d'] = [10, 'отдаленно точная дактилическая открытая рифма']

    d['#D0D'] = [11, 'отдаленно неточная дактилическая открытая рифма']
    d['#D0d'] = [11, 'отдаленно неточная дактилическая открытая рифма']
    d['#d0D'] = [11, 'отдаленно неточная дактилическая открытая рифма']
    d['#d0d'] = [11, 'отдаленно неточная дактилическая открытая рифма']


    d['0D0D'] = [12, 'неточная дактилическая открытая рифма']
    d['0D0d'] = [12, 'неточная дактилическая открытая рифма']
    d['0d0D'] = [12, 'неточная дактилическая открытая рифма']
    d['0d0d'] = [12, 'неточная дактилическая открытая рифма']
    return d





def get_schema_desc(schema):

    schema_desc = ""
    rank = -1
    d = generate_schema_desc()

    if schema in d.keys():
        schema_desc = (d[schema])[1]
        rank = (d[schema])[0]

    return schema_desc, rank


def find_clausula(words_line):
    last_word = words_line[-1]

def find_predudarn_segment(word):
    predudarn = (re.split("'", word)[0])[:-1]
    predudarn_sogl_list = re.split(r"[аеёиоуыэюя]",predudarn)
    predudarn_sogl_list = list(filter(None, predudarn_sogl_list)) # очищаем список от пустых элементов

    predudarn_glas_list = re.split(r"[бвгджзйклмнпрстфхцчшщьъ]",predudarn)
    predudarn_glas_list = list(filter(None, predudarn_glas_list)) # очищаем список от пустых элементов

    # print(predudarn_sogl_list)
    # print(predudarn_glas_list)
    return [predudarn_sogl_list,predudarn_glas_list]

def find_zadudarn_segment(word):
    zadudarn = (re.split("'", word)[1])
    zadudarn_sogl_list = re.split(r"[аеёиоуыэюя]",zadudarn)
    zadudarn_sogl_list = list(filter(None, zadudarn_sogl_list)) # очищаем список от пустых элементов

    zadudarn_glas_list = re.split(r"[бвгджзйклмнпрстфхцчшщьъ]", zadudarn)
    zadudarn_glas_list = list(filter(None, zadudarn_glas_list))  # очищаем список от пустых элементов

    # print(zadudarn_sogl_list)
    return [zadudarn_sogl_list,zadudarn_glas_list]

def parts_of_zaudar(word, sogl,glas):
    # return  ['вк', 'а'] (ФРАЗИРО'ВКА)
    word_in_parts = []
    word = re.split("'", word)[1]
    sogl = "бвгджзйклмнпрстфхцчшщьъ"
    glas = "аеёиоуыэюя"
    part_str = ""

    for i, letter in enumerate(word):
        if i != len(word)-1:  # не последний элемент
            if (word[i] in sogl and word[i + 1] in glas) or (word[i] in glas and word[i + 1] in sogl):
                part_str = part_str + letter
                word_in_parts.append(part_str)
                part_str = ""
            if (word[i] in sogl and word[i + 1] in sogl) or (word[i] in glas and word[i + 1] in glas):
                part_str = part_str + letter
        if i == len(word)-1:
            part_str = part_str + letter
            word_in_parts.append(part_str)
    return word_in_parts


def parts_of_preudar(word, sogl,glas):
    # return  ['фр', 'а', 'з', 'и', 'р'] (ФРАЗИРО'ВКА)
    word_in_parts = []
    word = re.split("'",word)[0]
    i = 0
    for part in sogl:
        l = len(part)
        if word[0:l] == part:
            word_in_parts.append(part)
            word = word[l:]
        else:
            # для гласных
            l = len(glas[i])
            if word[0:l] == glas[i]:
                word_in_parts.append(glas[i])
                word = word = word[l:]
                i = i + 1
                # еще для согласного
                l = len(part)
                if word[0:l] == part:
                    word_in_parts.append(part)
                    word = word[l:]
    return word_in_parts





def get_zaudar_schema(word1, word2):
    solg_pairs = [['б', 'п'],['г', 'к'],['д', 'т'],['з', 'с'],['в', 'ф'],['ж', 'ш'], ['здн', 'зн'],['рдц', 'рц'],['дц', 'ц'],['дч', 'ч'],['жд', 'ж'],['стл', 'сл'],['стн', 'сн'],['нтск', 'нск'],['тск', 'цк'],['тц', 'ц'],['тч', 'ч'],['вств', 'ств'],['лнц', 'нц'],['зж', 'ж'],['сж', 'ж'],['стск', 'ск'],['тьс', 'ц'],['тс', 'ц'],['зч', 'щ'],['жч', 'щ'],['сч', 'щ'],['ждь', 'щ'],['гк', 'хк']]


    sogl1, glas1 = find_zadudarn_segment(word1)
    sogl2, glas2 = find_zadudarn_segment(word2)

    # ==============================
    #  СОГЛАСНЫЕ ЗАУДАРНЫЕ
    # ==============================
    # 0 - отсутствие созвучия
    # * - созвучие
    #     рифмы: (##), (0##), (#0#) ....
    # ................................

    # выбираем наименьший по длине список (заударная часть, идем с начала)
    if len(sogl1) < len(sogl2):
        len_min = len(sogl1)-1
    else:
        len_min = len(sogl2)-1

    r = dict()

    r['shema_sogl'] = '0' * (len_min + 1)

    for i in range(0, len_min + 1):
        for pair in solg_pairs:
            # если 1) парные согласные 2) согласные одинаковые 3) одинаковые последние согласные (если их 2 и более: [ст, т])
            if (sogl1[i] in pair and sogl2[i] in pair) or (sogl1[i] == sogl2[i]) or ((sogl1[i])[-1] == (sogl2[i])[-1]):
                r[i] = [sogl1[i], sogl2[i]]
                val = r['shema_sogl']
                r['shema_sogl'] = val[:i] + '#' + val[i + 1:]

    # ==============================
    #  ГЛАСНЫЕ ПРЕУДАРНЫЕ
    # ==============================
    # b - отсутствие созвучия
    # B - созвучие
    #     рифмы:
    # ................................
    glas_pairs = [['и', 'ы'],['у', 'ю'],['ъ', 'а'],['ъ', 'о'],['ъ', 'э'],['ь', 'я'],['ь', 'ё'],['ь', 'е'],['е', 'э'],['ё', 'о'],['ю', 'у'],['я', 'а']]

    # выбираем наименьший по длине список (преударная часть, идем с конца)
    if len(glas1) < len(glas2):
        len_min = len(glas1)-1
    else:
        len_min = len(glas2)-1

    r['shema_gl'] = 'd' * (len_min + 1)

    for i in (range(0, len_min + 1)):
        for pair in glas_pairs:
            # если 1) парные согласные 2) согласные одинаковые 3) одинаковые последние согласные (если их 2 и более: [ст, т])
            if (glas1[i] in pair and glas2[i] in pair) or (glas1[i] == glas2[i]) or ((glas1[i])[-1] == (glas2[i])[-1]):
                r[str(i) + 'g'] = [glas1[i], glas2[i]]
                val = r['shema_gl']
                r['shema_gl'] = val[:i] + 'D' + val[i + 1:]

    # print(r['shema_gl'])

    # ==============================
    #  СОБИРАЕМ СХЕМУ
    # ==============================

    if 'shema_gl' in r.keys() and 'shema_gl' in r.keys():
        total_schema = ''
        s_s = r['shema_sogl']
        s_g = r['shema_gl']




        word_in_parts1 = parts_of_zaudar(word1, sogl1,glas1)
        word_in_parts2 = parts_of_zaudar(word2, sogl2,glas2)
        # print(word_in_parts1)
        # print(word_in_parts2)

        for letter in word_in_parts1:
            if letter in glas1:
                if len(s_g)!=0:
                    total_schema = total_schema + s_g[0]
                    s_g = s_g[1:]
            else:
                if len(s_s) != 0:
                    total_schema = total_schema + s_s[0]
                    s_s = s_s[1:]

        # print("заударная схема: "+total_schema)
    return total_schema




def get_preudar_schema(word1, word2):
    solg_pairs = [['б', 'п'],['г', 'к'],['д', 'т'],['з', 'с'],['в', 'ф'],['ж', 'ш'], ['здн', 'зн'],['рдц', 'рц'],['дц', 'ц'],['дч', 'ч'],['жд', 'ж'],['стл', 'сл'],['стн', 'сн'],['нтск', 'нск'],['тск', 'цк'],['тц', 'ц'],['тч', 'ч'],['вств', 'ств'],['лнц', 'нц'],['зж', 'ж'],['сж', 'ж'],['стск', 'ск'],['тьс', 'ц'],['тс', 'ц'],['зч', 'щ'],['жч', 'щ'],['сч', 'щ'],['ждь', 'щ'],['гк', 'хк']]


    sogl1, glas1 = find_predudarn_segment(word1)
    sogl2, glas2 = find_predudarn_segment(word2)

    # ==============================
    #  СОГЛАСНЫЕ ПРЕУДАРНЫЕ
    # ==============================
    # 0 - отсутствие созвучия
    # * - созвучие
    #     рифмы: (***), (0**), (*0*) ....
    # ................................

    # выбираем наименьший по длине список (преударная часть, идем с конца)
    if len(sogl1) < len(sogl2):
        len_min = len(sogl1)-1
    else:
        len_min = len(sogl2)-1

    r = dict()

    r['shema_sogl'] = '0' * (len_min + 1)

    r_sogl1 = list(reversed(sogl1))
    r_sogl2 = list(reversed(sogl2))

    for i in range(0, len_min + 1):
        for pair in solg_pairs:
            # если 1) парные согласные 2) согласные одинаковые 3) одинаковые последние согласные (если их 2 и более: [ст, т])
            if (r_sogl1[i] in pair and r_sogl2[i] in pair) or (r_sogl1[i] == r_sogl2[i]) or (
                (r_sogl1[i])[-1] == (r_sogl2[i])[-1]):
                r[len_min + 1 - i] = [r_sogl1[i], r_sogl2[i]]
                val = r['shema_sogl']
                r['shema_sogl'] = val[:(len_min - i)] + '*' + val[(len_min - i) + 1:]

    # print(r['shema_sogl'])

    # ==============================
    #  ГЛАСНЫЕ ПРЕУДАРНЫЕ
    # ==============================
    # b - отсутствие созвучия
    # B - созвучие
    #     рифмы:
    # ................................
    glas_pairs = [['и', 'ы'],['у', 'ю'],['ъ', 'а'],['ъ', 'о'],['ъ', 'э'],['ь', 'я'],['ь', 'ё'],['ь', 'е'],['е', 'э'],['ё', 'о'],['ю', 'у'],['я', 'а']]

    # выбираем наименьший по длине список (преударная часть, идем с конца)
    if len(glas1) < len(glas2):
        len_min = len(glas1)-1
    else:
        len_min = len(glas2)-1

    r['shema_gl'] = 'b' * (len_min + 1)

    r_glas1 = list(reversed(glas1))
    r_glas2 = list(reversed(glas2))
    for i in (range(0, len_min + 1)):
        for pair in glas_pairs:
            # если 1) парные согласные 2) согласные одинаковые 3) одинаковые последние согласные (если их 2 и более: [ст, т])
            if (r_glas1[i] in pair and r_glas2[i] in pair) or (r_glas1[i] == r_glas2[i]) or (
                (r_glas1[i])[-1] == (r_glas2[i])[-1]):
                r[str(len_min - i) + 'g'] = [r_glas1[i], r_glas2[i]]
                val = r['shema_gl']
                r['shema_gl'] = val[:(len_min - i)] + 'B' + val[(len_min - i) + 1:]

    # ==============================
    #  СОБИРАЕМ СХЕМУ
    # ==============================




    if 'shema_gl' in r.keys() and 'shema_gl' in r.keys():
        total_schema = ''
        s_s = r['shema_sogl']
        s_g = r['shema_gl']

        word_in_parts1 = parts_of_preudar(word1, sogl1,glas1)
        word_in_parts2 = parts_of_preudar(word2, sogl2,glas2)
        # print(word_in_parts1)
        # print(word_in_parts2)

        for letter in word_in_parts1:
            if letter in glas1:
                if len(s_g)!=0:
                    total_schema = total_schema + s_g[0]
                    s_g = s_g[1:]
            else:
                if len(s_s) != 0:
                    total_schema = total_schema + s_s[0]
                    s_s = s_s[1:]

        # print("предударная схема: "+total_schema)
    return total_schema

def get_last_stress_syllab_schema(word1, word2):
    glas_pairs = [['и', 'ы'],['у', 'ю'],['ъ', 'а'],['ъ', 'о'],['ъ', 'э'],['ь', 'я'],['ь', 'ё'],['ь', 'е'],['е', 'э'],['ё', 'о'],['ю', 'у'],['я', 'а']]

    solg_pairs = [['б', 'п'], ['г', 'к'], ['д', 'т'], ['з', 'с'], ['в', 'ф'], ['ж', 'ш'], ['здн', 'зн'], ['рдц', 'рц'],
                  ['дц', 'ц'], ['дч', 'ч'], ['жд', 'ж'], ['стл', 'сл'], ['стн', 'сн'], ['нтск', 'нск'], ['тск', 'цк'],
                  ['тц', 'ц'], ['тч', 'ч'], ['вств', 'ств'], ['лнц', 'нц'], ['зж', 'ж'], ['сж', 'ж'], ['стск', 'ск'],
                  ['тьс', 'ц'], ['тс', 'ц'], ['зч', 'щ'], ['жч', 'щ'], ['сч', 'щ'], ['ждь', 'щ'], ['гк', 'хк']]

    total_schema = ""
    if word1[-1] == "'" and word2[-1] == "'":
        for pair in glas_pairs:
            # если 1) парные согласные 2) согласные одинаковые 3) одинаковые последние согласные (если их 2 и более: [ст, т])
            if (word1[-2] in pair and word2[-2] in pair) or (word1[-2] == word2[-2]):
                total_schema = '&'

        for pair in solg_pairs:
            if (word1[-3] in pair and word2[-3] in pair) or (word1[-3] == word2[-3]):
                total_schema = '*&'



    # if total_schema!="":
        # print('ударение на последний слог, последнюю гласную')
        # print(total_schema)

    return total_schema



def rythm_detection(word1, word2):
    preudar_schema = get_preudar_schema(word1, word2)
    zaudar_schema = get_zaudar_schema(word1, word2)
    stress_schema = get_last_stress_syllab_schema(word1, word2)

    return [preudar_schema, zaudar_schema, stress_schema]


