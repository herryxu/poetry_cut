# poetry_cut
古诗词分词统计
由于CBDB数据库很大，有400+M。github不允许上传这么大的文件，请大家自行去[CBDB官网](http://projects.iq.harvard.edu/chinesecbdb/%E4%B8%8B%E8%BC%89cbdb%E5%96%AE%E6%A9%9F%E7%89%88)下载单机版数据库，并且以cbdb_sqlite.db为文件名存储在data目录下。
# 依赖库
程序依赖了多个python库
``` shell
pip3 install thulac
pip3 install gensim
pip3 install wordcloud
pip3 install xlwt
```
其中thulac用于分词，gensim用于word2vec. wordcloud 用于输出词云图，xlwt用于生成excel
这两个库只用于第一篇文章的分析。如果您只关心如何构建诗人关系网络，那么不需要安装这个两个库。
