from wordcloud import WordCloud

def counter_to_words(data):
    word_dict = {}
    word_dict[data[0]] = int(data[1].strip())
    return word_dict
    word_list = []
    text = data[0]
    len = int(data[1].strip())
    for i in range(1,int(len/10)):
        word_list.append(text)
    return word_list
def word_to_cloud(fileName, max = 100, width = 600, height = 500):
  with open('data/'+fileName + ".txt","r") as fileIn:
    count = 0
    txt = ''
    word_dict = {} 
    for line in fileIn:
        if count >= 100:
            break;
        text = line.split(',')
        word_dict[text[0]] = int(text[1].strip())
        #data = counter_to_words(text)
        # txt = txt + ' '.join(data) + ' '
        #1.读取文本内容
        count += 1
    #2.设置词云的背景颜色、宽高、字数
    wordcloud=WordCloud(
    background_color="white",width=width,
    font_path = 'source/chinese.ttf',
    height=height,max_words=max,collocations = False).generate_from_frequencies(word_dict)
    #3.生成图片
    image=wordcloud.to_image()
    #4.显示图片
    # image.show()
    wordcloud.to_file('image/'+fileName + '_50.jpg')

def main():
    ## 生成词云图
    list = ['song_ryth', 'song_char','song_author', 'song_word']
    for f in ['song_place']:
        word_to_cloud(f)
    print('词云生成完成\n')
if __name__ == '__main__':
    main()
