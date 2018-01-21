MingLangLib: A Natural Language Processing Toolkit
=====
汉语自然语言处理包
------
Example Code

from minglanglib import *

test = quick_split()
_input = 'Oh my god! What a wonderful day'
print _input
print test.split(_input)
print "---------------------"
_input = '通常简称为MM法。其基本思想为：假定分词词典中的最长词有i个汉字字符，则用被处理文档的当前字串中的前i个字作为匹配字段，查找字典。'
print _input
print test.split(_input)
------
运行环境
* numpy
------
Version 0.1
* 基于词频统计的中文分词功能
