MingLangLib: A Natural Language Processing Toolkit
=====
汉语自然语言处理包
------
Example Code

    from minglanglib import *

    test = quick_split()\
    _input = '其基本思想为：假定分词词典中的最长词有i个汉字字符，则用被处理文档的当前字串中的前i个字作为匹配字段，查找字典。'
    print test.split(_input)
    
Output

    其 基本 思想 为 ： 假定 分词 词典 中 的 最长 词 有 i 个 汉字 字符 ， 则 用 被 处理 文档 的 当前 字串 中 的 前 i 个 字 作为 匹配 字段 ， 查找 字典 。

------
运行环境
* numpy
------
Version 0.1
* 基于词频统计的中文分词功能
