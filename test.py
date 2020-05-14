#encoding=utf-8
import jieba
import thulac
seg_list = jieba.cut("我来到北京清华大学",cut_all=True)
print( '/'.join(seg_list)) #全模式
seg_list = jieba.cut("我来到北京清华大学",cut_all=False)
print('/' .join(seg_list))
seg_list = jieba.cut('我爱自然语言处理')
print('/' .join(seg_list))
thu = thulac.thulac()
seg_list = thu.cut('这是一句不一样的话')
print(seg_list)

