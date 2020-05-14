import xlwt  ## exccel

def word_to_excel(fileName, max = 100):
    count = 0
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Sheet Name1", cell_overwrite_ok=True)
    sheet.write(count,0, '关键字')
    sheet.write(count,1, '次数')
    with open('data/'+fileName + ".txt","r") as fileIn:
       for line in fileIn:
            if count > max:
                break; 
            count=count+1
            text = line.split(',')
            sheet.write(count,0, text[0]) # row, column, value
            sheet.write(count,1, int(text[1].strip()))
    workbook.save('excel/' + fileName + '_' + max +'.xls')
    return True
def main():
    ## 生成excel
    list = ['song_ryth', 'song_char','song_author', 'song_word']
    for f in ['song_char']:
        word_to_excel(f)
    print('excel生成完成')
if __name__ == '__main__':
    main()
