MingLangLib: A Natural Language Processing Toolkit
=====
汉语自然语言处理包
------
运行环境
* numpy 1.12.1 （其他版本的numpy未测试，不过应该没问题）

Example Code 1 分词

    from minglanglib import *

    qs = quick_split()
    _input = '斯坦福大学为硅谷（Silicon Valley）的形成和崛起奠定了坚实的基础。'
    print qs.split_sentence(_input)
    
  注意：adv_switch 确保了算法会不断搜索是否有组合词。若不需要此功能，可以关闭。

    print test.split_sentence(_input, adv_switch = False)
    
Output

    斯坦福大学 为 硅谷 （ Silicon Valley ） 的 形成 和 崛起 奠定 了 坚实 的 基础 。
    斯坦 福 大学 为 硅谷 （ Silicon Valley ） 的 形成 和 崛起 奠定 了 坚实 的 基础 。
    
Example Code 2

  情感分析模块。输出结果：该句子情感为正面的概率）

    sa = sentiment_analyzer()
    _input = "这谈判团队真业余，一开始的风声的3000万+姆希塔良，后来再变成1000万，"+
        "现在又成平换了，不要告诉我这是为了照顾姆希塔良情绪主动不要钱？ 再给他开个20万的周薪我就真笑了 "
    print sa.get_score(_input)
    
Output

    0.382575117931
    
------
Version 0.3
* 新增了情感分析模块
* 支持混合语言
* 以电商商品评价举例，好评/差评预测准确率约为79.5%（参考数据：data/sentiment/test_sentences_100pos_100neg.txt，前一百个为好评，后一百个为差评）
* 由于数据量较小，该算法是基于词语情感极性词典的，并使用了小型 Neural Network 作为辅助，而非目前较为普遍的 Recurrent Neural Network。
------
Version 0.2
* 提升了稳定性，增加了 split_sentence 函数的 advanced_merge 功能的开关，避免了不必要的运算。
------
Version 0.1
* 基于词频统计的中文分词功能
* 支持混合语言
* 分割速度稳定，即使需要分割的文字篇幅巨大。以鲁迅的小说《孔乙己》为例，全文共2618个字符，分词耗时7.2秒（MacBook Pro 3.1 GHz Intel Core i7，单核运算）
