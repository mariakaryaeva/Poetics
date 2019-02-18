__author__ = 'maria'

#coding=utf-8
import re
import io
import pymorphy2




def normalize(word):
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(word)[0]
    return p.normal_form

def POS(word):
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(word)[0]

    return re.split(",",str(p.tag))[0]

def get_probab_stress(word):
    all_poss_stress_words = []
    vowels = "аеёиоуыэюя"
    for n, letter in enumerate(word):
        if letter in vowels:
            all_poss_stress_words.append(word[:n] +letter+"'"+word[n+1:])

    return all_poss_stress_words

def calcucate_stress_probability(word,list_res):

    vowels = r"[аеёиоуыэюя]"
    dict = {}
    N = len(re.findall(vowels, word)) # количество слогов
    full_syllab_list = []
    count = 0
    for letter in word:
        count += 1
        if letter in vowels:
            letter_stress = re.sub(letter, letter + "'", letter)
            word_stress = word[:count - 1] + letter_stress + word[count:]
            full_syllab_list.append(word_stress)

    try:
        for item in full_syllab_list:
            if item in list_res:
                prob = 1 / N + 1 / N ** 2
                dict[item] = prob
            else:
                prob = (1-len(list_res)*(1 / N + 1 / N ** 2))/(N-len(list_res))
                dict[item] = prob
    except ZeroDivisionError:
        dict[list_res[0]] = 1

    return dict







def find_word_stress_opt(word):
        res = set()
        res_extra = []
        word_lst = []
        vowels = set(r'аеёиоуыэюя')
        count = 0
        stress_variants = []
        stress_variant_extra = []
        if set(word).intersection(vowels)!=set():
            for letter in word:
                count += 1
                if letter in vowels:
                    letter_stress = re.sub(letter, letter + "'", letter)
                    word_stress = word[:count - 1] + letter_stress + word[count:]
                    stress_variants.append(word_stress)


            if len(stress_variants) == 1:
                res = stress_variants
            else:
                first_letter = (stress_variants[0])[0]
                file = open("/Users/maria/PycharmProjects/poetics/verse_analysis/letters/"+first_letter+".txt", 'r')
                # file = open("Stress_forms.txt", 'r')
                set_stress_variant = set(stress_variants)

                for item in stress_variants:
                    if len(item) > 3:
                        stress_variant_extra.append(item[:-1])

                for line in file:
                    line = re.sub("#", ",", line)
                    line = re.sub("\n", "", line)
                    res = set(re.split(",", line)).intersection(set_stress_variant)


                    for i_pattern in stress_variant_extra:
                        if len(re.findall(i_pattern, line)) > 0:
                            if len(re.findall(i_pattern, line)) > 0:
                                for i in stress_variants:
                                    if i_pattern in i:
                                        res_extra.append(i)

                    if len(res) > 0:
                        break


                if len(res) == 0:
                    if len(res_extra) > 0:
                        res = res_extra
                    else:
                        res = set([word])


        else:
            res = set([word])



        dict = calcucate_stress_probability(word, list(res))

        return list(res),dict


        #
    #     if word_stress in line:
    #                 find = 1
    #         if find == 1:
    #             word_lst.append(word_stress)
    # return word_lst


def find_word_stress(word):
    word_lst = []
    vowels = set(r'аеёиоуыэюя')
    count = 0
    for letter in word:
        find = 0
        count += 1
        if letter in vowels:
            letter_stress = re.sub(letter, letter+"'", letter)
            word_stress = word[:count-1]+letter_stress+word[count:]
            file = open("Stress_forms.txt", 'r')
            for line in file:
                if word_stress in line:
                    find = 1
            if find == 1:
                word_lst.append(word_stress)
    return word_lst


def get_syllables(word, vowels, sign_chars, pattern):
    mask = ''.join(['v' if c in vowels else c if c in sign_chars else 'c' for c in word.lower()])
    return [word[m.start():m.end()] for m in pattern.finditer(mask)]

def devide_syllables(word):
    vowels = set('аеёиоуыэюя')
    sign_chars = set('ъь')
    pattern_str = "(c*[ьъ]?vc+[ьъ](?=v))|(c*[ьъ]?v(?=v|cv))|(c*[ьъ]?vc[ъь]?(?=cv|ccv))|(c*[ьъ]?v[cьъ]*(?=$))"
    pattern = re.compile(pattern_str)
    print('-'.join(get_syllables(word, vowels, sign_chars, pattern)))



def tokenize(line):
     line_tok = str.split(line)
     return line_tok


def clean_text(line):
    line_clear = re.sub(r"[.\««,\»»;\–:—\"|{}@~!?\-&+=*…]", "", line)
    line_clear = re.sub("\d+", "", line_clear)
    return line_clear.strip()



def devide_verse(infile):
    verse_desc = []
    line_number = 0


    for line in open(infile, "r"):
        if line!="":
            line_number+=1

        d = {}
        d = dict.fromkeys(['stanza', 'line_number', 'raw_line', 'prep_line', 'scheme'])

        p_line = tokenize(clean_text(line))
        prep_list = []
        for word in p_line:
            prep_word = []
            prep_word.append(word)
            prep_d = {}
            prep_d = dict.fromkeys(['syl_word', 'stress', 'lemm'])
            syl_word = devide_syllables(word)


def define_stress(word_with_stress):

    vowels = set('аеёиоуыэюя')
    result=""
    count = 0
    if set(word_with_stress).intersection(vowels) != set():

        for letter in word_with_stress:

            if letter in vowels:

                if len(word_with_stress)>count+1 and word_with_stress[count+1]=="'":
                    result = result+"C"
                else:
                    result = result+"c"
            count += 1
    else:
        result = ""
    # print(result+" "+word_with_stress)
    return result



def func():
    outf2 = open("result_stress.txt", "w")
    with open("result.txt", "w") as outf:
        for line in open("verse.txt", 'r'):
            words = tokenize(clean_text(line))
            print(words)
            for word in words:
                res = find_word_stress_opt(word.lower())
                print(res)

                if len(res)<1:
                    outf.write(word+" ")
                elif len(res)==1:
                    outf.write(res[0]+" ")
                else:
                    count = 0
                    for i in res:
                        if count == len(res)-1:
                            outf.write(i+" ")
                        else:
                            outf.write(i+"|")
                        count += 1
                if len(res)>=1:
                    outf2.write(define_stress(res[0]))
                else:
                    outf2.write(define_stress(word))



            outf.write("\n")
            outf2.write("\n")

