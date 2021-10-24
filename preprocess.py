# -*- coding: utf-8 -*-
import argparse
import sys
import os
import glob

alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'ａ', 'ｂ', 'ｃ', 'ｄ', 'ｅ', 'ｆ', 'ｇ', 'ｈ', 'ｉ', 'ｊ', 'ｋ', 'ｌ', 'ｍ', 'ｎ', 'ｏ', 'ｐ', 'ｑ', 'ｒ', 'ｓ', 'ｔ', 'ｕ', 'ｖ', 'ｗ', 'ｘ', 'ｙ', 'ｚ', 'Ａ', 'Ｂ', 'Ｃ', 'Ｄ', 'Ｅ', 'Ｆ', 'Ｇ', 'Ｈ', 'Ｉ', 'Ｊ', 'Ｋ', 'Ｌ', 'Ｍ', 'Ｎ', 'Ｏ', 'Ｐ', 'Ｑ', 'Ｒ', 'Ｓ', 'Ｔ', 'Ｕ', 'Ｖ', 'Ｗ', 'Ｘ', 'Ｙ', 'Ｚ']

# extract sentences from Aozora Bunko
def preprocess(dir):

    files = glob.glob(dir + '/*')

    documents_without_ruby = []

    for file in files:
        fp = open(file)
        lines = fp.readlines()
        fp.close()
    
        begining_note = 0
        end_note = 0
    
        sentences_with_ruby = []
    
        # delete Aozora Bunko header
        for i in range(0, len(lines)):
            if lines[i][:-1] == '-------------------------------------------------------':
                begining_note += 1
                continue
    
            if lines[i].find('底本：') != -1:
                end_note = 1
    
            if begining_note < 2:
                continue

            if end_note == 1:
                continue

            if lines[i].find('［＃') != -1:
                continue

            in_parenthese = False
            x = ''
            for j in range(0, len(lines[i])):
                

                alpha_chk = False
                for k in range(0, len(alpha)):
                    if lines[i][j] == alpha[k]:
                        alpha_chk = True
                        break
                if alpha_chk:
                    x = ''
                    break
                
                if lines[i][j] == '\u3000':
                    continue			
    
                if lines[i][j] == '\n':
                    continue
    
                if lines[i][j] == '「':
                    continue

                if lines[i][j] == '」':
                    continue

                if lines[i][j] == '『':
                    continue

                if lines[i][j] == '』':
                    continue

                if in_parenthese:
                    continue

                if lines[i][j] == '（':
                    in_parenthese = True
                    continue
                elif lines[i][j] == '）':
                    in_parenthese = False
                    continue

                if lines[i][j] == '。' or lines[i][j] == '！' or lines[i][j] == '？':
                    x += lines[i][j]
                    sentences_with_ruby.append(x)
                    x = ''
                else:
                    x += lines[i][j]
    
            if x != '':
                if x[:-1] == '。' or x[:-1] == '！' or x[:-1] == '？':
                    sentences_with_ruby.append(x)
    
    
        # delete ruby
        sentences_without_ruby = []
        for i in range(0, len(sentences_with_ruby)):
            x = ''
            in_parenthese = False
            for j in range(0, len(sentences_with_ruby[i])):
                if sentences_with_ruby[i][j] == '｜':
                    continue
    
                if sentences_with_ruby[i][j] == '《':
                    in_parenthese = True
                    continue
    
                if sentences_with_ruby[i][j] == '》':
                    in_parenthese = False		
                    continue
    
                if in_parenthese:
                    pass
                else:
                    x += sentences_with_ruby[i][j]
    
    
            sentences_without_ruby.append(x)
    
        documents_without_ruby.extend(sentences_without_ruby)


    return documents_without_ruby

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='preprocess')
    parser.add_argument('--in-dir',help='directory where files are stored')
    parser.add_argument('--out-file',help='original sentences')
    args = parser.parse_args()
    
    documents_without_ruby = preprocess(args.in_dir)

    fp = open(args.out_file, 'w')
    for i in range(0, len(documents_without_ruby)):
        fp.write(documents_without_ruby[i] + '\n')
    fp.close()


