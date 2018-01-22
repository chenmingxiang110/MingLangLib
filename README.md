MingLangLib: A Natural Language Processing Toolkit
=====
汉语自然语言处理包
------
Example Code 1

    from minglanglib import *

    test = quick_split()
    _input = '斯坦福大学为硅谷（Silicon Valley）的形成和崛起奠定了坚实的基础。'
    print test.split_sentence(_input)
    # adv_switch 确保了算法会不断搜索是否有组合词。若不需要此功能，可以关闭。
    print test.split_sentence(_input, adv_switch = False)
    
Output

    斯坦福大学 为 硅谷 （ Silicon Valley ） 的 形成 和 崛起 奠定 了 坚实 的 基础 。
    斯坦 福 大学 为 硅谷 （ Silicon Valley ） 的 形成 和 崛起 奠定 了 坚实 的 基础 。
    
------
运行环境
* numpy 1.12.1 （其他版本的numpy未测试，不过应该没问题）
------
Version 0.2
* 提升了稳定性，增加了 split_sentence 函数的 advanced_merge 功能的开关，避免了不必要的运算。
------
Version 0.1
* 基于词频统计的中文分词功能
* 支持混合语言
* 分割速度稳定，即使需要分割的文字篇幅巨大。以鲁迅的小说《孔乙己》为例，全文共2618个字符，分词耗时7.2秒（MacBook Pro 3.1 GHz Intel Core i7，单核运算）
