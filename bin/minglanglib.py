# -*- coding: utf-8 -*-
# @Author: mingxiangchen
# @Date:   2018-01-21T00:08:10-08:00
# @Email:  ming1993@stanford.edu
# @Last modified by:   mingxiangchen
# @Last modified time: 2018-01-21T05:16:31-08:00


import os
import math
import numpy as np
import warnings

class quick_split:

    def __init__(self):
        _path = os.path.dirname(os.path.abspath(__file__))
        _path = "/".join(_path.split('/')[:-1])+"/data/"
        self.personal_dict_path = _path+"data1.txt"
        self.web_dict_path = _path+"data2.txt"
        self.freq_words_path = _path+"freq_words.txt"
        self.character_path = _path+"hzpy-utf8.txt"
        self.positive_words_path = _path+"all_positive.txt"
        self.negative_words_path = _path+"all_negative.txt"

        self.personal_dict = {}
        self.web_dict = {}
        # 2/(1+exp(x/100))
        self.scores = {}
        self.freq_words = set()
        self.max_length = 0
        self.character_set = set()

        with open(self.character_path) as f:
            for line in f:
                line = line.strip().split(',')
                word = line[0].decode('utf-8')
                word = word.replace(u'\ufeff', '')
                if len(word)>1: print "Warning! Possible Byte Order Mark!"
                self.character_set.add(word)
        for i in xrange(1000):
            self.scores[i] = 2.0/(1.0+math.exp(i/100.0))
        with open(self.freq_words_path,'r') as f:
            for line in f:
                word = line.strip().decode('utf-8')
                word = word.replace(u'\ufeff', '')
                self.freq_words.add(word)
        with open(self.personal_dict_path,'r') as f:
            for line in f:
                line = line.strip().split(',')
                words = line[0].decode('utf-8')
                words = words.replace(u'\ufeff', '')
                if len(words) < 2:
                    continue
                if words in self.personal_dict: print "Warning! Repeating Words!"
                self.personal_dict[words] = int(line[1])
        with open(self.web_dict_path,'r') as f:
            for line in f:
                line = line.strip().split(',')
                words = line[0].decode('utf-8')
                words = words.replace(u'\ufeff', '')
                if len(words) < 2:
                    continue
                if words in self.web_dict: print "Warning! Repeating Words!"
                if int(line[1])<10: continue
                self.web_dict[words] = int(line[1])/10+1


        for item in self.web_dict:
            if len(item)>self.max_length:
                self.max_length = len(item)
        for item in self.personal_dict:
            if len(item)>self.max_length:
                self.max_length = len(item)

        with open(self.positive_words_path) as f:
            for line in f:
                line = line.strip()
                word = line.decode('utf-8')
                word = word.replace(u'\ufeff', '')
                if len(word) > 1:
                    self.freq_words.add(word)
                if (word not in self.web_dict) and len(word)>1 :
                    self.web_dict[word] = 1
        with open(self.negative_words_path) as f:
            for line in f:
                line = line.strip()
                word = line.decode('utf-8')
                word = word.replace(u'\ufeff', '')
                if len(word) > 1:
                    self.freq_words.add(word)
                if (word not in self.web_dict) and len(word)>1 :
                    self.web_dict[word] = 1

    def isAlpha(self,word):
        try:
            return word.encode('ascii').isalpha()
        except UnicodeEncodeError:
            return False

    def find_max_in_two_dicts(self,word):
        appearances = [0,0]
        if word in self.personal_dict:
            appearances[0] = self.personal_dict[word]
        if word in self.web_dict:
            appearances[1] = self.web_dict[word]
        return max(appearances)

    def is_in_two_dicts(self,word):
        return ((word in self.personal_dict) or (word in self.web_dict))

    def split_helper(self, current_unicode):
        if len(current_unicode) == 1: return ([current_unicode],1.0)
        scores = []
        results = []
        if self.is_in_two_dicts(current_unicode):
            num = self.find_max_in_two_dicts(current_unicode)
            scores.append(self.scores[num])
            results.append([current_unicode])
        else:
            scores.append(len(current_unicode))
            all_split = []
            for item in current_unicode:
                all_split.append(item)
            results.append(all_split)

        for i in xrange(1,len(current_unicode)):
            result1,score1 = self.split_helper(current_unicode[:i])
            result2,score2 = self.split_helper(current_unicode[i:])
            scores.append(score1+score2)
            results.append(result1+result2)
        min_index = np.argmin(scores)
        return (results[min_index],scores[min_index])

    def advanced_merge(self,unicode_list):
        if len(unicode_list) == 1: return unicode_list
        all_merge = "".join(unicode_list)
        if (len(all_merge) < self.max_length) and self.is_in_two_dicts(all_merge):
            return [all_merge]
        results = []
        lengths = []
        for i in xrange(1,len(unicode_list)):
            temp_result1 = self.advanced_merge(unicode_list[:i])
            temp_result2 = self.advanced_merge(unicode_list[i:])
            temp_result = temp_result1+temp_result2
            results.append(temp_result)
            lengths.append(len(temp_result))
        min_index = np.argmin(lengths)
        return results[min_index]

    def force2split(self, _str):
        result = []
        for i in xrange(0,len(_str),10):
            result.append(_str[i:i+10])
        return result

    def partial_split(self,_input,adv_switch = True):
        if len(_input) == 0: return _input
        rough_split = []
        is_checked = []

        last_indicator = 0
        indicator = 0
        while indicator<len(_input)-1:
            for i in xrange(indicator+2,len(_input)+1):
                if _input[indicator:i] in self.freq_words:
                    if last_indicator!=indicator:
                        rough_split.append(_input[last_indicator:indicator])
                        if len(_input[last_indicator:indicator])>1:
                            is_checked.append(0)
                        else:
                            is_checked.append(1)
                    rough_split.append(_input[indicator:i])
                    is_checked.append(1)
                    last_indicator = i
                    indicator = i
            indicator+=1
        if last_indicator!=len(_input):
            rough_split.append(_input[last_indicator:])
            if len(_input[last_indicator:])>1:
                is_checked.append(0)
            else:
                is_checked.append(1)
        assert len(rough_split) == len(is_checked)

        # for i in xrange(len(rough_split)):
        #     print rough_split[i]
        #     print is_checked[i]

        for i in xrange(len(is_checked)):
            if is_checked[i] == 0:
                if len(rough_split[i])>15:
                    print "Warning! Too long to split:"
                    print rough_split[i]
                    _input_list = self.force2split(rough_split[i])
                    result_list = []
                    for _str in _input_list:
                        result_list+=self.split_helper(_str)[0]
                    rough_split[i]=result_list
                else:
                    rough_split[i] = self.split_helper(rough_split[i])[0]

        merged_result = []
        for i in xrange(len(is_checked)):
            if isinstance(rough_split[i], list):
                for item in rough_split[i]:
                    merged_result.append(item)
            else:
                merged_result.append(rough_split[i])

        if adv_switch:
            if len(merged_result)>15:
                print "Warning! Too many items to do advanced_merge!"
                temp_merge_result = []
                for i in xrange(0,len(merged_result),10):
                    temp_merge_result+=self.advanced_merge(merged_result[i:i+10])
                merged_result = temp_merge_result
                print " ".join(merged_result)
            else:
                merged_result = self.advanced_merge(merged_result)
        return " ".join(merged_result)
        # result = split_helper(_input)

    def split_sentence(self,_input,adv_switch = True):
        _input = _input.strip()
        if not isinstance(_input, unicode):
            _input = _input.decode('utf-8')
        # _input = _input.lower()
        special_character_positions = []
        for i in xrange(len(_input)):
            if _input[i] not in self.character_set:
                special_character_positions.append(i)
        if len(special_character_positions) == 0:
            return self.partial_split(_input,adv_switch)
        final_result = []
        for i in xrange(len(special_character_positions)):
            if i == 0:
                temp_input = _input[:special_character_positions[i]]
            else:
                temp_input = _input[special_character_positions[i-1]+1:special_character_positions[i]]
            if len(temp_input)<1:
                final_result.append(_input[special_character_positions[i]])
            else:
                final_result.append(self.partial_split(temp_input,adv_switch))
                final_result.append(_input[special_character_positions[i]])
        final_result.append(self.partial_split(_input[special_character_positions[-1]+1:],adv_switch))

        i1 = 0
        i2 = 0
        while i1<len(final_result):
            if final_result[i1].isalpha():
                i2 = i1
                i1+=1
                while  i1<len(final_result) and self.isAlpha(final_result[i1]):
                    i1+=1
                temp_word = "".join(final_result[i2:i1])
                if i1>=len(final_result):
                    final_result = final_result[:i2]+[temp_word]
                    break
                final_result = final_result[:i2]+[temp_word]+final_result[i1:]
                i1 = i2+1
            else:
                i1+=1
        temp = (" ".join(final_result)).split()
        return " ".join(temp)

class sentiment_analyzer:
    def __init__(self):
        self.splitter = quick_split()

        _path = os.path.dirname(os.path.abspath(__file__))
        _path = "/".join(_path.split('/')[:-1])+"/data/"
        positive_words_path = _path+"all_positive.txt"
        negative_words_path = _path+"all_negative.txt"

        self.positive_words = set()
        self.negative_words = set()
        with open(positive_words_path, 'r') as f:
            for line in f:
                line = line.strip()
                word = line.decode('utf-8')
                word = word.replace(u'\ufeff', '')
                self.positive_words.add(word)
        with open(negative_words_path, 'r') as f:
            for line in f:
                line = line.strip()
                word = line.decode('utf-8')
                word = word.replace(u'\ufeff', '')
                self.negative_words.add(word)

    def count_words(self, _input):
        _input = _input.strip()
        splitted_input = self.splitter.split_sentence(_input,adv_switch = False)
        splitted_input = splitted_input.split()
        pos_num = 0
        neg_num = 0
        for word in splitted_input:
            if word in self.positive_words: pos_num+=1
            if word in self.negative_words: neg_num+=1
        return pos_num,neg_num,len(_input)

    def calc_score(self, stats):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            pos_num,neg_num,length = stats
            X = np.array([[pos_num,neg_num,length]])
            Weights1 = np.array([[-1.90182692,-1.00246861,1.84768407,-3.64999117,1.03589266,2.31532596,2.89711564,1.98777375,-0.45237745,0.95548137],
                [2.8486167,4.10382932,1.06056173,2.88157075,-1.37585019,-0.87110768,-2.26924785,2.01158528,1.16686712,2.7833062],
                [0.24065763,-0.03765879,2.60870956,0.05527978,-0.00711582,-0.11916056,-0.16676489,3.87820933,-0.03177381,1.96674413]],dtype = np.float64)
            biases1 = np.array([[-1.68875263,0.23228552,-2.13660485,-3.11010808,-0.23813621,-0.76334739,-1.94071001,-4.59103548,1.25225239,-0.86990503]],dtype = np.float64)
            Weights2 = np.array([[-0.28296541],[-0.53647374],[ 0.02993459],[-0.39071311],[ 0.57038062],[ 0.33308203],[ 0.38660777],[ 0.04774547],[-0.73926376],[ 0.02830038]],dtype = np.float64)
            biases2 = np.array([[0.35243915]])

            output1 = 1/(1+np.exp(X.dot(Weights1)+biases1))
            output2 = 1/(1+np.exp(output1.dot(Weights2)+biases2))
            return output2.reshape([-1])[0]

    def get_score(self, _input):
        _input = _input.strip()
        if not isinstance(_input, unicode):
            _input = _input.decode('utf-8')
        _input = _input.lower()
        pos_num,neg_num,length = self.count_words(_input)
        stats = pos_num,neg_num,length
        return self.calc_score(stats)
