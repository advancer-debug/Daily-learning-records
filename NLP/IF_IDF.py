# -*- coding = utf-8 -*-
# /usr/bin/env python

# @Time    : 21-1-9 下午2:03
# @File    : IF_IDF.py
# @Software: PyCharm

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
  (0, 10)	0.44027050419943065
  (0, 8)	0.3703694278374568
  (0, 5)	0.44027050419943065
  (0, 4)	0.5303886653382521
  (0, 3)	0.44027050419943065
  (1, 10)	0.4103997467310884
  (1, 8)	0.34524120496743227
  (1, 7)	0.6128006641982455
  (1, 5)	0.4103997467310884
  (1, 3)	0.4103997467310884
  (2, 9)	0.5490363340004775
  (2, 8)	0.30931749359185684
  (2, 6)	0.5490363340004775
  (2, 1)	0.5490363340004775
  (3, 10)	0.44027050419943065
  (3, 8)	0.3703694278374568
  (3, 5)	0.44027050419943065
  (3, 4)	0.5303886653382521
  (3, 3)	0.44027050419943065
  (4, 12)	0.3779644730092272
  (4, 11)	0.7559289460184544
  (4, 2)	0.3779644730092272
  (4, 0)	0.3779644730092272
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

