import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
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
    saved_words_file = 'source/song_cut.txt'
      # 检查存储目录是否存在
    save_dir = os.path.dirname(saved_words_file)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    vector_model = word2vec(args.words_path)
    save_basic_words_data(word_counter, words_counter, genre_counter)
if __name__ == '__main__':
    main()
