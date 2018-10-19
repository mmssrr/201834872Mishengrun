#!usr/bin/env python
#-*- coding:utf-8 _*-
import os,sys
from textblob import TextBlob
from textblob import Word

base_path = 'data/20news-18828/'
class Preprocessing():

    def read_file(self):
        print('Read Data：')
        for dir in os.listdir(base_path):
            for file in os.listdir(base_path+dir+'/'):
                file_path=base_path+dir+'/'+file
                self.trans_words(file_path)

    def trans_words(self,file_path):
        words=[]
        with open(file_path,'r',encoding='utf-8',errors='ignore') as f:
            for line in f.readlines():
                textblob=TextBlob(line.strip())
                words.extend(textblob.words)
        words=self.check_words(words)

        new_path=file_path.replace('20news-18828','words')
        print(file_path)
        new_path=new_path[:-new_path[::-1].find('/')]
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        new_path+=file_path[-file_path[::-1].find('/'):]
        with open(new_path,'w',encoding='utf-8',errors='ignore') as f:
            for word in words:
                f.write(word+' ')

    def check_words(self,words):
        new_words=[]
        for word in words:
            word=word.lower()
            flag=False
            for letter in word:
                if not ((letter>'a' and letter<'z') or letter=='-'):
                    flag =True
                    break
            if flag:
                continue
            word=Word(word).lemmatize()
            word = Word(word).lemmatize('v')
            new_words.append(word)
        return new_words


if __name__=='__main__':

    p=Preprocessing()
    p.read_file()
