#coding=utf-8
import re
import io
import verse_analysis.strofas as st
import verse_analysis.verses as vs




# удаляем пустые строки, если они идут сначала, сконца или дублируются по нескольку пустых строк, разделяя строфы
def delete_extra_empty_lines(raw_input_verse):
    empty_line_list = []
    for n, line in enumerate(raw_input_verse):
        if line == "\n":
            empty_line_list.append(n)

    for n, tmp_i in enumerate(empty_line_list):
        if n+1!=len(empty_line_list):
            if tmp_i - empty_line_list[n+1] == -1:
                raw_input_verse[tmp_i] = 'to_delete'

    updated_verse = []
    for line in raw_input_verse:
        if line != 'to_delete':
            updated_verse.append(line)


    if updated_verse[0] =="\n":
        updated_verse.pop(0)
    if updated_verse[-1] =="\n":
        updated_verse.pop(len(updated_verse)-1)

    return updated_verse



# проверка, что кол-во строк в строфах стиха одинаковое (т.е. строфы одинаковой длины)
def is_strof_lines_is_equal(dict):
    flag = True
    tmp_val = ""
    for key in dict.keys():
        if tmp_val == "":
            tmp_val = len(dict[key])
        else:
            if tmp_val != len(dict[key]):
                flag = False
    return flag

# проверка, что в стихе только одна строфа
def is_only_one_strofa(dict):
    flag = True
    if len(dict.keys()) > 1:
        flag = False

    return flag



# разделение на строфы и собрали строфы в стих
# возвращаем подготовленный стих и строфы
def strofa_division(raw_input_verse):
    empty_lines_number = []
    dict = {}
    strofa_num = 0
    raw_input_verse = delete_extra_empty_lines(raw_input_verse)

    for n, line in enumerate(raw_input_verse):
        if line == "\n":
            empty_lines_number.append(n)
            strofa_num = strofa_num + 1
        else:
            if strofa_num in dict.keys():
                tmp_lst = dict[strofa_num]
                tmp_lst.append(line)
                dict[strofa_num] = tmp_lst
            else:
                dict[strofa_num] = [line]
    return raw_input_verse, dict





def make_verse(raw_input_verse):

    raw_input_verse,dict = strofa_division(raw_input_verse)
    # =======================================================================
    # ПЕРВЫЙ СЛУЧАЙ (СТАНДАРТ)
    # остальные пока не рассматриваем (поделили на строфы, равные по длине)
    # =======================================================================

    # если количество строк в строфах равно
    if is_strof_lines_is_equal(dict):
        list_of_strofas = []
        for key in dict.keys():
            value = dict[key]
            tmp_strofa = st.Strofa(value)
            list_of_strofas.append(tmp_strofa)

        input_verse = vs.Verse(raw_input_verse,list_of_strofas)


    # # подслучай: только одна строфа в стихе
    # if is_only_one_strofa(dict):
    #     for key in dict.keys():
    #         input_verse = vs.Verse(raw_input_verse, [dict[key]])


    return input_verse


# Open a file
fo = open("verse.txt", "r")
raw_input_verse = fo.readlines()
input_verse = make_verse(raw_input_verse)

#выводим схему ударения
print(input_verse.get_stress_schema())
print("---")
print(input_verse.get_stress_formula())

print(input_verse.get_num_slog_schema())
print(input_verse.rythm_detection())
print(input_verse.get_all_rythm_words())
print(input_verse.get_all_rythm_stressed_words())

fo.close()





