# poetry_cut
古诗词分词、词频统计、词性分析，作者关系图，包括诗词数据库
# 依赖源
来自另一位git主的仓库数据库，https://github.com/chinese-poetry/chinese-poetry/tree/master/ci 
down下来后存储在source目录下
由于CBDB数据库很大，有400+M。github不允许上传这么大的文件，请大家自行去[CBDB官网](http://projects.iq.harvard.edu/chinesecbdb/%E4%B8%8B%E8%BC%89cbdb%E5%96%AE%E6%A9%9F%E7%89%88)下载单机版数据库，并且以cbdb_sqlite.db为文件名存储在source目录下。
# 依赖库
程序依赖了多个python库
``` shell
pip3 install thulac
pip3 install gensim
pip3 install wordcloud
pip3 install xlwt
```
其中thulac用于分词，gensim用于word2vec. wordcloud 用于输出词云图，xlwt用于生成excel
# 程序
``` shell
python3 words_cut.py #切词以及生成统计txt
python3 words_vec.py # 词向量分析
python3 words_excel.py #输出到excel
python3 words_cloud.py # 输出到词云
python3 get_author_info.py  # 获取作者信息
python3 construct_authors_relation.py # 构建作者关系网
```
