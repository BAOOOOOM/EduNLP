令牌化
=======

令牌化是自然语言处理中一项基本但是非常重要的步骤，它更令人为所熟知的名字是分句和分词。
在EduNLP中我们将令牌化分为不同的粒度，为避免歧义，我们定义如下：

* 词/字级别：分词

* 句级别：分句

* 资源级别：令牌化

本模块提供题目文本的令牌化解析（Tokenization），将题目转换成令牌序列，方便后续向量化表征试题。

在进入此模块前需要先后将item经过 `语法解析 <parse.rst>`_ 和 `成分分解 <seg.rst>`_ 处理，之后对切片后的item中的各个元素进行分词，提供深度选项，可以按照需求选择所有地方切分或者在部分标签处切分（比如\SIFSep、\SIFTag处）；对标签添加的位置也可以进行选择，可以在头尾处添加或仅在头或尾处添加。

具有两种模式，一种是linear模式，用于对文本进行处理（使用jieba库进行分词）；一种是ast模式，用于对公式进行解析。

学习路线图
--------------------

.. toctree::
   :maxdepth: 1
   :titlesonly:
   
   分词 <tokenize/分词>
   分句 <tokenize/分句>
   令牌化 <tokenize/令牌化>
