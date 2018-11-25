#!usr/bin/env python
#-*- coding:utf-8 _*-

import os
import shutil
train_path='data/train.txt'
test_path='data/test.txt'
# for name in os.listdir('data/20news-18828'):
#     print(name)
#     os.makedirs('data/train/%s'% name)
# with open(train_path,'r',encoding='utf-8',errors='ignore') as f:
#     for line in f.readlines():
#         linelist = line.strip().split(' ')
#
#         print(str(linelist).split('/')[2])
#         targetFile='data/train/'+str(linelist).split('/')[2]+'/'
#         print(targetFile)
#         shutil.copy(line.strip('\n'), targetFile)
for name in os.listdir('data/20news-18828'):
     print(name)
     os.makedirs('data/test/%s'% name)
with open(test_path,'r',encoding='utf-8',errors='ignore') as f:
    for line in f.readlines():
        linelist = line.strip().split(' ')

        print(str(linelist).split('/')[2])
        targetFile='data/test/'+str(linelist).split('/')[2]+'/'
        print(targetFile)
        shutil.copy(line.strip('\n'), targetFile)