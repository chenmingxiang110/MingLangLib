MingLangLib: A Natural Language Processing Toolkit
=====
汉语自然语言处理包
------
Example Code

    from minglanglib import *

    test = quick_split()
    _input = '斯坦福大学为硅谷（Silicon Valley）的形成和崛起奠定了坚实的基础。'
    print test.split(_input)
    
Output

    斯坦福大学 为 硅谷 （ Silicon Valley ） 的 形成 和 崛起 奠定 了 坚实 的 基础 。

------
运行环境
* numpy
------
Version 0.1
* 基于词频统计的中文分词功能
* 支持混合语言
