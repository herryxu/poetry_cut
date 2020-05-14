import thulac 
import sqlite3
import numpy as np
import jieba
import string
import re
from collections import Counter, defaultdict, OrderedDict
import pickle
import os
import argparse
import multiprocessing
import xlwt  ## exccel
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

def clean_txt(str):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    chinese = re.sub(pattern, '', str)
    return chinese
def save_data(saved_words_file):
    sql = sqlite3.connect('source/ci.db')
    thu = thulac.thulac()  # 分词器 
    char_counter = Counter()  # 字频统计
    author_counter = Counter()  # 每个作者的写诗篇数
    words_counter = Counter() # 所有词统计
    rhythmic_counter = Counter() #词牌统计
    vocab = set()  # 词汇库
    word_counter = Counter()  # 词频统计
    genre_counter = defaultdict(Counter)  # 针对每个词性的Counter
    cursor = sql.execute("SELECT rhythmic, author, content from ci;")
    d = {"rhythmic": None, "author": None, "paragraphs": None}
    dump_file = 'source/song_words_stat_result.pkl'
    fid_save = open(saved_words_file, 'w', encoding = 'utf-8')
    line_cnt = 0 # show line
    for row in cursor:
        ci = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
        valid_char = []
        rhythmic = row[0] 
        author = row[1]
        rhythmic_counter[rhythmic] += 1
        author_counter[author] += 1 
        poem = row[2].split('\n')
        if poem == []:
            continue
        for c in poem:
            valid_char.append(clean_txt(c))
        valid_str = ''.join(valid_char)
        word_genre_pairs = thu.cut(valid_str)
        word_list = []
        for word, genre in word_genre_pairs:
          word_list.append(word)
          vocab.add(word)
          if len(word) <= 1:
              ## 排除虚词
            if genre in ['c','p','u','y','e','o','g','x']: 
              char_counter[word] += 1
          else:
            word_counter[word] += 1
          genre_counter[genre][word] += 1
          words_counter[word] += 1  
        if line_cnt % 10 == 0:
          print('%d poets processed.' % line_cnt)
        line_cnt += 1
        save_line = ' '.join(word_list)
        fid_save.write(save_line + '\n')
    fid_save.close()
    # 保存作作者与词牌统计
    save_sort_word_data( 'data/song_author',author_counter)
    save_sort_word_data( 'data/song_ryth',rhythmic_counter)
    dumped_data = [char_counter, author_counter, vocab, words_counter, genre_counter]
    with open(dump_file, 'wb') as f:
      pickle.dump(dumped_data, f)
    return char_counter, author_counter, genre_counter,word_counter, words_counter

def save_basic_char_data(char_counter, author_counter = [], genre_counter = []):
    lstWords = {}
    # 基于字的分析
    print('\n\n基于字的分析')
    # 常用字排名
    print('\n常用字排名')   
    for c,v in char_counter.most_common(100):
        lstWords[c] = v
    save_sort_word_data('data/song_char', lstWords)
    lstWords = {}
    # 季节排名
    print('\n季节排名')
    for c in ['春', '夏', '秋', '冬']:
        print(c, char_counter[c])
        lstWords[c] = char_counter[c] if char_counter[c] > 0 else 0
    save_sort_word_data('data/song_season', lstWords)
    # 颜色排名
    lstWords = {}
    print('\n颜色排名')
    colors = ['红', '白', '青', '蓝', '绿', '紫', '黑', '黄']
    for c in colors:
        print(c, char_counter[c])
        lstWords[c] = char_counter[c] if char_counter[c] > 0 else 0
    save_sort_word_data('data/song_color', lstWords)    
    # 植物排名
    lstWords = {}
    print('\n植物排名')
    lists = ['梅', '兰', '竹', '菊', '松', '柳', '枫', '桃', '梨', '杏', '荷','柳']
    for c in lists:
        print(c, char_counter[c]) 
        lstWords[c] = char_counter[c] if char_counter[c] > 0 else 0    
    save_sort_word_data('data/song_plant', lstWords)
    # 情绪排名
    lstWords = {}
    print('\n情绪统计')
    lists = ['悲','惧','乐','怒','思','喜','忧'] 
    for c in lists:
        print(c, char_counter[c]) 
        lstWords[c] = char_counter[c] if char_counter[c] > 0 else 0    
    save_sort_word_data('data/song_metion', lstWords)     

def word_to_txt(fileName,lstWords):
    with open(fileName + '.txt', 'w') as fileOut:
     print ('字符\t字频')
     for e in lstWords:
         fileOut.write('%s,%d\n' % e)

# 保存排序完成的数据
def save_sort_word_data(fileName, list):   
    lstWords = sorted(list.items(), key=lambda x:x[1],  reverse=True)
    word_to_excel(fileName, lstWords)
    word_to_txt(fileName, lstWords)

def save_basic_words_data(word_counter,char_counter, genre_counter):
   # 基于词的分析
    lstWords = {}
    # 常用字排名
    print('\n常用词排名')
    for c,v in word_counter.most_common(100):
        lstWords[c] = v
    save_sort_word_data('data/song_word', lstWords)
    lstWords = {}
    print('\n\n基于词的分析')
     # 动物排名
    print('\n动物排名')
    for c in ['鸟', '鱼','蝉', '杜鹃','鹧鸪','雁' ,'乌鸦','蟋蟀','鸳鸯','燕','猿','鹰','鼠', '牛', '虎', '兔', '龙', '蛇', '马','羊', '猴', '鸡', '狗', '猪']:
        print(c, char_counter[c])
        lstWords[c] = char_counter[c] if char_counter[c] > 0 else 0
    save_sort_word_data('data/song_animal', lstWords) 
    # 特殊诩
    lstWords = {}
    print('\n特殊词')
    for c in ['胡虏','骄虏','匈奴','羌']:
        print(c, char_counter[c])
        lstWords[c] = char_counter[c] if char_counter[c] > 0 else 0
    save_sort_word_data('data/song_special_word', lstWords)
    # 节日
    lstWords = {}
    print('\n节日')
    for c in ['元日','人日','上元','社日','寒食','清明','端午','七夕','中元','中秋','重阳','冬至','腊日','除夕']:
        print(c, char_counter[c])
        lstWords[c] = char_counter[c] if char_counter[c] > 0 else 0
    save_sort_word_data('data/song_festival', lstWords) 
    # 食物
    lstWords = {}
    print('\n食物')
    for c in ['茶','酒','米','桃','鱼','荔枝','水果','餐食','汤圆','大豆','高粱','麦','糖','米酒']:
        print(c, char_counter[c])
        lstWords[c] = char_counter[c] if char_counter[c] > 0 else 0
    save_sort_word_data('data/song_food', lstWords)    
    # 地名排名
    lstWords = {}
    print('\n地名词排名')
    for c,v in genre_counter['ns'].most_common(100):
        lstWords[c] = v
    save_sort_word_data('data/song_place', lstWords)
    # 场景排名
    lstWords = {}
    print('\n场景排名')
    for c,v in genre_counter['s'].most_common(100):
        lstWords[c] = v
    save_sort_word_data('data/song_scene', lstWords) 

def save_basic_math_data():
   # 基于词向量分析数据 
    vector_model.most_similar(word)
    print_similar_words()
    
def print_similar_words(word):
    print('\n与"%s"比较意思比较接近的词' % word)
    print_counter(vector_model.most_similar(word))
 
# 将分词结果转换为向量
def word2vec(words_file):
  save_dir = os.path.dirname((words_file))
  vector_file = os.path.join(save_dir, 'word_vectors.model')

  if os.path.exists(vector_file):
    print('find word vector file, loading directly...')
    model = Word2Vec.load(vector_file)
  else:
    print('calculating word vectors...')
    model = Word2Vec(LineSentence(words_file), size=400, window=3, min_count=10,
                     workers=multiprocessing.cpu_count())
    # 将计算结果存储起来，下次就不用重新计算了
    model.save(vector_file)
  return model

def main():
    saved_words_file = 'data/song_cut.txt'
  #  word_to_cloud(saved_words_file)
   # vector_model = word2vec(saved_words_file)
    char_counter, author_counter, genre_counter,word_counter, words_counter = save_data(saved_words_file)
    save_basic_char_data(char_counter)
    save_basic_words_data(word_counter, words_counter, genre_counter)
if __name__ == '__main__':
    main() 
