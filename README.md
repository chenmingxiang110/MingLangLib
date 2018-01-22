MingLangLib: A Natural Language Processing Toolkit
=====
汉语自然语言处理包
------
运行环境
* numpy 1.12.1 （其他版本的numpy未测试，不过应该没问题）

Example Code 1 分词

    from minglanglib import *

    test = quick_split()
    _input = '斯坦福大学为硅谷（Silicon Valley）的形成和崛起奠定了坚实的基础。'
    print test.split_sentence(_input)
    
  注意：adv_switch 确保了算法会不断搜索是否有组合词。若不需要此功能，可以关闭。

    print test.split_sentence(_input, adv_switch = False)
    
Output

    斯坦福大学 为 硅谷 （ Silicon Valley ） 的 形成 和 崛起 奠定 了 坚实 的 基础 。
    斯坦 福 大学 为 硅谷 （ Silicon Valley ） 的 形成 和 崛起 奠定 了 坚实 的 基础 。
    
Example Code 2 （情感分析模块。输出结果：该句子情感为正面的概率）

    test = sentiment_analyzer()
    _input = "0比3被逆转相对来说比0比1被逆转更难得，更别说还有中场开香槟，2年后成功复仇这些附带剧情。"
    print test.get_score(_input)
    
Output

    0.310471107867
    
------
Version 0.3
* 新增了情感分析模块
* 支持混合语言
* 以电商商品评价举例，好评/差评预测准确率约为79.5%
------
Version 0.2
* 提升了稳定性，增加了 split_sentence 函数的 advanced_merge 功能的开关，避免了不必要的运算。
------
Version 0.1
* 基于词频统计的中文分词功能
* 支持混合语言
* 分割速度稳定，即使需要分割的文字篇幅巨大。以鲁迅的小说《孔乙己》为例，全文共2618个字符，分词耗时7.2秒（MacBook Pro 3.1 GHz Intel Core i7，单核运算）
