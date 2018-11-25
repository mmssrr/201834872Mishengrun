#!usr/bin/env python
#-*- coding:utf-8 _*-

import os
import math
import random

class NBC:
    def __init__(self):
        self.vocab = self.load_voab()
        self.dic, self.all_words_num = self.statistic()
        self.all_classes = self.get_all_classes()
        pass

    def load_voab(self):
        vocab = []
        with open('data/alter_vacob.txt', 'r', encoding='utf-8') as f:
            for line in f:
                vocab.append(line.strip().split(' ')[1])
        print(vocab)
        return vocab

    def statistic(self):
        path = 'data/train/'
        dic = {}
        all_words_num = 0
        for class_ in os.listdir(path):
            dic[class_] = {}
            print(class_)
            for file_name in os.listdir(path+class_+'/'):
                file_path = path + class_ + '/' + file_name
                words = []
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    words.extend(f.readline().strip().split(' '))
                for word in words:
                    if word not in self.vocab:
                        continue
                    else:
                        dic[class_][word] = dic[class_].get(word, 0) + 1

            current_class_words = 0
            for word in dic[class_]:
                current_class_words += dic[class_][word]
            dic[class_]['<<all>>'] = current_class_words
            all_words_num += current_class_words

        return dic, all_words_num


    def get_all_classes(self):
        path = 'data/train/'
        return os.listdir(path)

    def test(self, path):
        label = path.split('/')[-2]

        words = []

        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            words.extend(f.readline().strip().split(' '))

        max_p_index, max_p = 0, -9999999999999999999999999999999999

        for i, class_ in enumerate(self.all_classes):
            p = 0.0
            # print(class_, self.dic[class_].get('<<all>>'), self.all_words_num)
            p += math.log((self.dic[class_].get('<<all>>')+1) / self.all_words_num)

            # print(class_, self.dic[class_].get('<<all>>'))
            for word in words:
                p += math.log((self.dic[class_].get(word, 0) + 1) / (self.dic[class_].get('<<all>>') + self.all_words_num))
                # print(word, (self.dic[class_].get(word, 0) + 1)/ (self.dic[class_].get('<<all>>') + self.all_words_num))
            # print(class_, p)
            if p > max_p:
                max_p = p
                max_p_index = i
        print(label+'  =test=  '+self.all_classes[max_p_index])

        if (label == self.all_classes[max_p_index]):
            return 1
        return 0




if __name__ == '__main__':
    nbc = NBC()
    nbc.load_voab()

    path = 'data/test/'
    test_paths = []
    for class_ in os.listdir(path):
        for file_name in os.listdir(path+class_+'/'):
            file_path = path + class_ + '/' + file_name
            test_paths.append(file_path)

    #print(test_paths)


    nbc = NBC()
    correct = 0

    for test_path in test_paths:
        correct += nbc.test(test_path)
        print()
    print(correct / len(test_paths))