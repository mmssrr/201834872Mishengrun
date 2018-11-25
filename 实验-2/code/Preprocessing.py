#!usr/bin/env python
#-*- coding:utf-8 _*-

import os
from textblob import TextBlob
from textblob import Word
from collections import Counter
from nltk.corpus import stopwords
import random

base_path = 'data/20news-18828/'
mid_path = 'data/words/'
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

        new_path=new_path[:-new_path[::-1].find('/')]
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        new_path+=file_path[-file_path[::-1].find('/'):]
        with open(new_path,'w',encoding='utf-8',errors='ignore') as f:
            for word in words:
                f.write(word+' ')
            print(new_path)
            print('Preprocessing Finish!')

    def check_words(self,words):
        new_words=[]
        sr=stopwords.words('english')
        for word in words:
            word=word.lower()
            flag=False
            for letter in word:
                if not ((letter>='a' and letter<='z') or letter=='-'):
                    flag =True
                    break
            if flag:
                continue
            word=Word(word).lemmatize()
            word = Word(word).lemmatize('v')
            new_words.append(word)
        clean_words = [i for i in new_words if i not in sr]

        return clean_words

    def All_data(self):
        i = 1
        with open('data/all.txt', 'w', encoding='utf-8', errors='ignore') as f:
            for dir in os.listdir(mid_path):
                for file in os.listdir(mid_path + dir + '/'):
                    file_path = mid_path + dir + '/' + file
                    f.write('%d' % i + ' ' + file_path + '\n')
                    i += 1
    def Divide_data(self):
        all_list = []
        data_list = list(range(1, 18829))
        slice = random.sample(data_list, 3766)  # 从data_list中随机获取3766个元素，作为一个片断返回
        other = list(set(data_list).difference(set(slice)))
        with open('data/all.txt', 'r', encoding='utf-8', errors='ignore') as f:
            for line in f.readlines():
                line = line.strip('\n').split(' ')
                all_list.append(line)
            print(all_list)
        with open('data/test.txt', 'w', encoding='utf-8', errors='ignore') as ff, open('data/train.txt', 'w',encoding='utf-8',errors='ignore') as fff:
            for i in slice:
                for data in all_list:
                    if i == int(data[0]):
                        ff.write(data[1] + '\n')
            for j in other:
                for data in all_list:
                    if j == int(data[0]):
                        fff.write(data[1] + '\n')

    def Create_dict(self):
        vocab = {}
        train = []
        with open('data/train.txt','r',encoding='utf-8',errors='ignore') as f:
            for line in f.readlines():
                line = line.strip('\n')
                train.append(line)

        for file in train:
            with open(file, 'r', encoding='utf-8', errors='ignore') as ff:
                temp_vocab = dict(Counter(ff.readline().strip().split(' ')))
                for key in temp_vocab:
                    vocab[key] = vocab.get(key,0) + temp_vocab[key]

        vocab=sorted(vocab.items(),key=lambda x:x[1],reverse=True)

        with open('data/dict.txt','w',encoding='utf-8',errors='ignore') as fff:
            for i,v in enumerate(vocab):
                fff.write(str(i)+' '+v[0]+' '+str(v[1])+'\n')

    def alter_vacob(self):
        path = 'data/dict.txt'
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            all_text = f.readlines()

        with open('data/alter_vacob.txt', 'w', encoding='utf-8', errors='ignore') as ff:
            for line in all_text:
                linelist = line.strip().split(' ')
                if int(linelist[2]) >= 9 and int(linelist[2]) <= 10000:
                    ff.write(linelist[0] + ' ' + linelist[1] + ' ' + linelist[2] + '\n')
if __name__=='__main__':

    p=Preprocessing()
    #p.read_file()
    #p.All_data()
    #p.Divide_data()
    #p.Create_dict()
    p.alter_vacob()