__author__ = 'maria'

#coding=utf-8
import re
import verse_analysis.rythms as ryth
import numpy
import verse_analysis.rythm_schema as ryth_sch

class Verse:
    def __init__(self, raw_verse, list_of_strofas):
        """Constructor"""
        self.raw_verse = raw_verse
        self.list_of_strofas = list_of_strofas  # lisf of objects (type:Strofa)

    # схема ударений со словами
    def get_stress_schema(self):
        strofas_in_verse = []
        for strofa in self.list_of_strofas:
            lines_in_strofa = []
            for line in strofa.lisf_of_lines:
                words_in_line = []
                for word in line.by_words:
                    if word.stress_word !=None:
                        words_in_line.append((word.stress_word)[0])
                    else:
                        words_in_line.append(word.norm_word)
                lines_in_strofa.append((" ").join(words_in_line))

            strofas_in_verse.append(("\n").join(lines_in_strofa))

        print("схема ударений в стихе")
        return ("\n\n").join(strofas_in_verse)

        #         lines_in_strofa.append(words_in_line)
        #
        #     strofas_in_verse.append(lines_in_strofa)
        # print("схема ударений в стихе")
        # return strofas_in_verse


    # слоговая формула вида: ссССссС
    #[[['C', 'cC', 'cCcc'], ['C', 'cC', 'Cc'], ['C', 'Cc', 'ccCcc'], ['Cc', 'Cc', 'Cc']]]
    def get_stress_formula(self):
        strofas_in_verse = []
        for strofa in self.list_of_strofas:
            lines_in_strofa = []
            for line in strofa.lisf_of_lines:
                words_in_line = []
                for word in line.by_words:
                    if word.stress_word !=None:
                        words_in_line.append(word.shemaCc)
                # lines_in_strofa.append((" ").join(words_in_line)) # --  с пробелами
                lines_in_strofa.append(("").join(words_in_line))  # --  без пробелами
                line.set_stress_schema(words_in_line)

            strofas_in_verse.append(("\n").join(lines_in_strofa))
        print("слоговая формула")
        return ("\n\n").join(strofas_in_verse)


    # [[['1s', '23s', '456'], ['1s', '23s', '4'], ['1s', '23s', '4567'], ['12s', '34s', '5']]]
    def get_num_slog_schema(self):
        strofas_in_verse = []
        for strofa in self.list_of_strofas:
            lines_in_strofa = []
            for line in strofa.lisf_of_lines:
                total = 0
                slog_list = []
                ending = line.form_endings_for_rythm()
                for word in line.by_words[:-(len(ending))]: # не берем последнее фонетическое слово
                    word_vowels_length = len(word.shemaCc)
                    res = ""
                    for i in range(0,word_vowels_length):
                        total = total + 1
                        res = res + str(total)
                    slog_list.append(res+"s")
                res = ""
                for word in ending:
                    word_vowels_length = len(word.shemaCc)

                    for i in range(0,word_vowels_length):
                        total = total + 1
                        res = res + str(total)
                slog_list.append(res)
                # lines_in_strofa.append(slog_list)
                lines_in_strofa.append((" ").join(slog_list))

            strofas_in_verse.append(("\n").join(lines_in_strofa))
        print("схема словоразделов")
        return ("\n\n").join(strofas_in_verse)



    def get_all_rythm_words(self):
        res_arr = []
        for strofa in self.list_of_strofas:
            for line in strofa.lisf_of_lines:
                res = ryth_sch.get_rythm_words(line,0)
                res_arr.append(res)
        return res_arr

    def get_all_rythm_stressed_words(self):
        res_arr = []
        for strofa in self.list_of_strofas:
            for line in strofa.lisf_of_lines:
                res = ryth_sch.get_rythm_words(line,1)
                res_arr.append(res)
        return res_arr





    def find_rifma(self):
        strofas_in_verse = []
        for strofa in self.list_of_strofas:
            endings = []
            for line in strofa.lisf_of_lines:
                endings.append(line.form_endings_for_rythm())



    def match_metr(self):
        dict = {}
        dict['ямб'] = 'cC'
        dict['хорей'] = 'Cc'
        dict['анапест'] = 'ccC'
        dict['дактиль'] = 'Ccc'
        dict['амфибрахий'] = 'cCc'



    def rythm_detection(self):
        strofas_in_verse = []
        for strofa in self.list_of_strofas:
            ending_list = []
            dict_lines = {}
            index = 0
            for line in strofa.lisf_of_lines:
                ending = line.form_endings_for_rythm()
                ending_list.append(ending)
                dict_lines[index] = {}
                index = index + 1


            for n_i, i in enumerate(ending_list):
                for n_j, j in enumerate(ending_list):
                    if n_i != n_j and n_i < n_j:
                        # print(str(n_i) + " и " + str(n_j))
                        value = dict_lines[n_i]
                        value[n_j] = ryth.rythm_detection(((i[-1]).stress_word)[0], ((j[-1]).stress_word)[0])
                        dict_lines[n_i] = value

            final_dict = {}
            for key,value in dict_lines.items():
                for key2, value2 in value.items():
                    for item in value2:
                        schema_desc, rank = ryth.get_schema_desc(item)
                        if rank != -1 and rank !=0:
                            final_dict[str(key)+"_"+str(key2)] =[rank, schema_desc,item]

            result = []
            for key, value in final_dict.items():
                result.append(key+" ранк: "+ str(value[0]) + ", " + value[1] + ", схема: " + value[2])
                first, second = re.split("_",key)
                first = int(first)
                second = int(second)
                rythm_lines = (strofa.lisf_of_lines[first]).get_rythm_lines()
                rythm_lines[second] = value[0]
                (strofa.lisf_of_lines[first]).set_rythm_lines(rythm_lines)


            strofas_in_verse.append(("\n").join(result))
        print("рифмы:")
        return ("\n\n").join(strofas_in_verse)


def optimize_stress_schema(self):

    for strofa in self.list_of_strofas:
        stress_schema = numpy.empty() #0,len(strofa.lisf_of_lines)
        for line in strofa.lisf_of_lines:
            stress_schema = numpy.add(stress_schema,numpy.array(line.get_stress_schema()), axis = 0)

            # line.get_rythm_lines()


