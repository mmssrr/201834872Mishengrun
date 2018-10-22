#!usr/bin/env python
#-*- coding:utf-8 _*-
import os,sys
from collections import Counter
import random
base_path = 'data/words/'
class Vsm():
    def All_data(self):
        i=1
        with open('data/all.txt', 'w', encoding='utf-8', errors='ignore') as f:
            for dir in os.listdir(base_path):
                for file in os.listdir(base_path + dir + '/'):
                    file_path = base_path + dir + '/' + file
                    f.write('%d'% i+' '+file_path+'\n')
                    i+=1
    #print('Finish!')
    def Divide_data(self):
        all_list=[]
        data_list=list(range(1,18829))
        slice = random.sample(data_list, 3766)  # 从data_list中随机获取3766个元素，作为一个片断返回
        other = list(set(data_list).difference(set(slice)))
        with open('data/all.txt','r',encoding='utf-8',errors='ignore') as f:
            for line in f.readlines():
                line=line.strip('\n').split(' ')
                all_list.append(line)
            print(all_list)
        with open('data/test.txt','w',encoding='utf-8',errors='ignore') as ff,open('data/train.txt', 'w', encoding='utf-8', errors='ignore') as fff:
            for i in slice:
                for data in all_list:
                    if i==int(data[0]):
                        ff.write(data[1]+'\n')
            for j in other:
                for data in all_list:
                    if j==int(data[0]):
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
                if int(linelist[2]) >=9 and int(linelist[2]) <=10000:
                    ff.write(linelist[0] + ' ' + linelist[1] + ' ' + linelist[2] + '\n')
    def make_vacob(self):
        vocab=[]
        with open('data/alter_vacob.txt','r',encoding='utf-8',errors='ignore') as f:
            for line in f.readlines():
                vocab.append(line.split()[1])
        return vocab
        #print(vocab)
    def form_vector(self,filepath,vocab):
        vector=[]
        with open(filepath,'r',encoding='utf-8',errors='ignore') as f:
            words = f.readline().strip().split(' ')
        for word in vocab:
            if word in words:
                vector.append(1)
            else:
                vector.append(0)
        return vector
    def get_vectors(self):
        vocab = self.make_vacob()
        train=[]
        test=[]
        with open('data/train.txt','r',encoding='utf-8',errors='ignore') as f:
            for line in f.readlines():
                line = line.strip('\n')
                train.append(line)
        with open('data/test.txt','r',encoding='utf-8',errors='ignore') as ff:
            for line in ff.readlines():
                line = line.strip('\n')
                test.append(line)
        #print(test)
        #print(len(test))
        #print(train)
        #print(len(train))
        with open('data/train_vector.txt','w',encoding='utf-8',errors='ignore') as f1:
            for file in train:
                vector =self.form_vector(file,vocab)
                f1.write(file+' '+'%s'%vector+'\n')
        with open('data/test_vector.txt','w',encoding='utf-8',errors='ignore') as ff1:
            for file in test:
                vector =self.form_vector(file,vocab)
                ff1.write(file+' '+'%s'%vector+'\n')
        print('Finish!')
if __name__=='__main__':

    p=Vsm()


    ##p.make_vacob()
    #p.All_data()
    #p.Divide_data()
    #p.alter_vacob()
    #p.Create_dict()
    p.get_vectors()