# TF-IDF

### 简述

TF-IDF (term frequency-inverse document frequency)是一种用于信息检索(information  retrieval)与文本挖掘(text  mining)的常用加权技术，比较容易理解的一个应用场景是当我们手头有一些文章时或者微博评论，我们希望计算机能够自动地进行关键词提取。而TF－IDF就是可以帮我们完成这项任务的一种统计方法。**它能偶用于评估一个词语对于一个文集或一个语料库中的其中一份文档的重要程度。这个方法又称为"词频－逆文本频率"。

###  TF-IDF原理叙述

**词频(term frequency, TF)指的是某一个给定的词语在该文件中出现的次数**。这个数字通常会被归一化（分子一般小于分母区别于IDF），以防止它偏向长的文件。（同一个词语在长文件里可能会比短文件有更高的词频，而不管该词语重要与否）

**逆向文件频率** (inverse document frequency, IDF) 是一个词语普遍重要性的度量**。**某一特定词语的IDF，**可以由总文件数目除以包含该词语之文件的数目，再将得到的商取对数得到。**

在一特定文件内的高词语频率，以及该词语在整个文件集合中的低文件频率，可以产生出高权重的TF-IDF。因此，**TF-IDF倾向于过滤掉常见的词语，保留重要的词语。**

**综上TF－IDF的主要思想是：**如果某个词或短语在一篇文章中出现的频率TF高，并且在其他文章中很少出现，则认为此词或者短语具有很好的类别区分能力，适合用来分类。TF－IDF实际上是：TF * IDF，TF为词频，IDF反文档频率。

上面是从定性上说明的TF－IDF的作用，那么如何对一个词的IDF进行定量分析呢？这里直接给出一个词x的IDF的基本公式如下

![图片](https://mmbiz.qpic.cn/mmbiz_png/pkLOV48rcrllHRhlQIRp8Aibu3DKGqcpwVLHP5PgpoBlkXQ0gAgJsTKkledq2EPbok6L5FiafonicLxY8Q4ZJQcibw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

其中，N代表语料库中文本的总数，而N(x)代表语料库中包含词x的文本总数。

在一些特殊的情况下上面的公式会有一些小的问题，比如某一个生僻词在语料库中没有，则分母变为0，IDF就没有意义了，所以常用的IDF需要做一些平滑，使得语料库中没有出现的词也可以得到一个合适的IDF值，平滑的方法有很多种：参考最后链接，**最常见的IDF平滑公式之一为**：



![图片](https://mmbiz.qpic.cn/mmbiz_png/pkLOV48rcrllHRhlQIRp8Aibu3DKGqcpwDmcQtC5eqAOYtKq5XI1aNvBNHPeuias84XA7UGXqic3qaN8u8xhkfGqQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

进而可以计算某一个词的TF－IDF值：



![图片](https://mmbiz.qpic.cn/mmbiz_png/pkLOV48rcrllHRhlQIRp8Aibu3DKGqcpwDbcBN9ffQg26nwtSvnDx7DfY84y8o0vdtMbgqGAliafHRpgkYtboGBA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

其中TF(x)是指词x在当前文本的词频。这个数字是对词数的归一化，以防止它偏向长的文件。对于某一特定文件里的词语x来说，它的重要性可表示为：



![图片](https://mmbiz.qpic.cn/mmbiz_png/pkLOV48rcrllHRhlQIRp8Aibu3DKGqcpwhfz7TqAPqVIjiboXlbiabndc2ibUd2czLdiarPM7hssNICIMqFbkomXbmA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

以上式子中分子为x词在第j个文件中出现的次数，而分母是在第j个文件中所有字词的出现词数之和。

### TF-ID的实现(python

```python
# 有很多方法可以计算TF－IDF的预处理，比如genism和scikit-learn包中，这里使用scikit－learn中的两种方法进行TF－IDF的预处理

# 第一种
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

#
corpus = [
    'This is the first document',
    'This is the second document',
    'And the third one.',
    'Is this the first document?',
    'I come to American to travel'
]

words = CountVectorizer().fit_transform(corpus)
tfidf = TfidfTransformer().fit_transform(words)

print(tfidf)
"""
在(index1,index2)中：index1表示为第几个句子或者文档，index2为所有语料库中的单词组成的词典的序号
，之后的数字为该词所计算得到的TF－IDF的结果值
输出的各词的TF-IDF值如下
  (0, 10)  0.44027050419943065
  (0, 8)   0.3703694278374568
  (0, 5)   0.44027050419943065
  (0, 4)   0.5303886653382521
  (0, 3)   0.44027050419943065
  (1, 10)  0.4103997467310884
  (1, 8)   0.34524120496743227
  (1, 7)   0.6128006641982455
  (1, 5)   0.4103997467310884
  (1, 3)   0.4103997467310884
  (2, 9)   0.5490363340004775
  (2, 8)   0.30931749359185684
  (2, 6)   0.5490363340004775
  (2, 1)   0.5490363340004775
  (3, 10)  0.44027050419943065
  (3, 8)   0.3703694278374568
  (3, 5)   0.44027050419943065
  (3, 4)   0.5303886653382521
  (3, 3)   0.44027050419943065
  (4, 12)  0.3779644730092272
  (4, 11)  0.7559289460184544
  (4, 2)   0.3779644730092272
  (4, 0)   0.3779644730092272
"""

# 第二种

#
corpus1 = [
    'This is the first document',
    'This is the second document',
    'And the third one.',
    'Is this the first document?',
    'I come to American to travel'
]

tfidf1 = TfidfVectorizer().fit_transform(corpus1)
print('===='*8 + "第二种结果")
print(tfidf1)
```



[代码地址]()

[参考地址](https://mp.weixin.qq.com/s?__biz=MzIwNzYzNjA1OQ==&mid=2247484212&idx=1&sn=8a1f402fcdbf5c982c71859ce7e08c25&chksm=970e1000a079991611e03948ba0a74e6e45f6c2d64dcc0d65d9848d266ef751a0cb6a48864d2&scene=21#wechat_redirect)

[平滑方法参考](https://mp.weixin.qq.com/s?__biz=MzIwNzYzNjA1OQ==&mid=2247483725&idx=1&sn=a3168411ba9d38d4135b14a0e8d57275&chksm=970e1279a0799b6f2c451dfc7273c98200aae678c89cfb1a422e09b0c15bf50b50225fbf3d51&scene=21#wechat_redirect)





































