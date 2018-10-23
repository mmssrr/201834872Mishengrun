#!usr/bin/env python
#-*- coding:utf-8 _*-
import os,sys
from gensim import corpora, models, similarities
import pickle as pkl
class Knn():
    def Filter_word(self):#过滤词频少于N的word
        path = 'data/dict.txt'
        texts=[]
        label=[]
        filter_word=[]
        train = []
        temp_vocab=[]
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f.readlines():
                linelist = line.strip().split(' ')
                #print(linelist)
                if int(linelist[2]) <=10 or int(linelist[2]) >= 10000:
                    filter_word.append(linelist[1])
            #print(filter_word)
            #return filter_word

            with open('data/train.txt', 'r', encoding='utf-8', errors='ignore') as f:
                for line in f.readlines():
                    line = line.strip('\n')
                    label.append(line.split('/')[2])
                    train.append(line)
            #print(train)
            print(label)
            print(len(label))
            for file in train:
                with open(file, 'r', encoding='utf-8', errors='ignore') as ff:
                    temp_vocab=[]
                    temp_vocab.extend(ff.readline().strip().split(' '))
                    #print(temp_vocab)
                    final_words = [i for i in temp_vocab if i not in filter_word]
                    #print(final_words)
                    texts.append(final_words)
            dictionary = corpora.Dictionary(texts)
            print(dictionary.token2id)

            #corpus = [dictionary.doc2bow(text) for text in texts]
if __name__=='__main__':
    p=Knn()
    p.Filter_word()