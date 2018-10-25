#!usr/bin/env python
#-*- coding:utf-8 _*-
import os
from gensim import corpora,models,similarities
import gensim
import pickle as pkl
import matplotlib.pyplot as plt
class Knn():
    def Filter_word(self):#过滤词频少于N的word
        path = 'data/dict.txt'
        texts=[]
        filter_word=[]
        train = []
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
                    train.append(line)
            #print(train)
            current = 0
            count = 20000
            for file in train:
                current += 1
                if current > count:
                    break
                with open(file, 'r', encoding='utf-8', errors='ignore') as ff:
                    temp_vocab=[]
                    temp_vocab.extend(ff.readline().strip().split(' '))
                    #print(temp_vocab)
                    final_words = [i for i in temp_vocab if i not in filter_word]
                    print(final_words)
                    print(current,len(final_words))
                    texts.append(final_words)
            #print(texts)
            if not os.path.exists('data/texts.pkl'):
                file = open('data/texts.pkl', 'wb+')
                pkl.dump(texts, file)
                file.close()
            dictionary = corpora.Dictionary(texts)
            if not os.path.exists('data/dictionary.pkl'):
                file = open('data/dictionary.pkl', 'wb+')
                pkl.dump(dictionary, file)
                file.close()
            #print(dictionary.token2id)
    def Get_label(self,path):
        label = []
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f.readlines():
                line = line.strip('\n')
                label.append(line.split('/')[2])
        return label
    def Load_model(self):
        load_model=1
        if os.path.exists('data/corpus.pkl'):
            with open('data/corpus.pkl', 'rb') as f:
                corpus = pkl.load(f)

        else:  # 由文档向量以及频率构成文档向量
            corpus = [dictionary.doc2bow(text) for text in texts]
            file = open('data/corpus.pkl', 'wb+')
            pkl.dump(corpus, file)
            file.close()
        if load_model == 1:
            tfidf = models.TfidfModel.load("data/model.tfidf")
        else:
                # 计算tfidf权重,注意在gensim的tfidf算法中到文档频率的求解过程中对数之后+1了
            tfidf = models.TfidfModel(corpus)
            tfidf.save("data/model.tfidf")
        corpus_tfidf = tfidf[corpus]
        # for file in corpus_tfidf:
        #     print(file)
        path = 'data/dict.txt'
        texts = []
        true_label = []
        filter_word = []
        test = []
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f.readlines():
                linelist = line.strip().split(' ')
                # print(linelist)
                if int(linelist[2]) <= 10 or int(linelist[2]) >= 10000:
                    filter_word.append(linelist[1])
            # print(filter_word)
            # return filter_word
        with open('data/test.txt', 'r', encoding='utf-8', errors='ignore') as f:
            for line in f.readlines():
                line = line.strip('\n')
                test.append(line)
            #print(test)
            #print(true_label)
            #print(len(true_label))
        current = 0
        count = 10000
        for file in test:
            current += 1
            if current > count:
                break
            with open(file, 'r', encoding='utf-8', errors='ignore') as ff:
                temp_vocab = []
                temp_vocab.extend(ff.readline().strip().split(' '))
                # print(temp_vocab)
                final_words = [i for i in temp_vocab if i not in filter_word]
                print(final_words)
                print(current, len(final_words))
                texts.append(final_words)

        with open('data/dictionary.pkl', 'rb') as f:
            dictionary = pkl.load(f)
        query = [dictionary.doc2bow(text) for text in texts]
        if not os.path.exists('data/query.pkl'):
            file = open('data/query.pkl', 'wb+')
            pkl.dump(query, file)
            file.close()

    def test_model(self,k):
        results = []
        with open('data/corpus.pkl', 'rb') as f:
            corpus = pkl.load(f)
        tfidf = models.TfidfModel.load("data/model.tfidf")
        corpus_tfidf = tfidf[corpus]
        with open('data/query.pkl', 'rb') as ff:
            query = pkl.load(ff)

        query_tfidf = tfidf[query]
        index = gensim.similarities.MatrixSimilarity(corpus_tfidf)

        sims = index[query_tfidf]
        similarities = list(sims)
        right_flag = 0
        wrong_flag = 0
        print('Counting Similarites...:')
        for similarity in similarities:
            dict_similarity = []
            label = self.Get_label('data/train.txt')
            num = 0
            for i in similarity:
                dict_similarity.append((label[num], i))
                num += 1
            sorts = sorted(dict_similarity, key=lambda dict_similarity: dict_similarity[1], reverse=True)[0:k]
            #print(sorts)
            counts = {}
            for i in sorts:  # 初始化0
                counts[i[0]] = 0
            for i in sorts:  # 统计
                counts[i[0]] += 1
            max = 0
            for key in counts:
            #     print(key, counts[key])
                if counts[key] > max:
                    max = counts[key]
                    category = key
            print('The category is: ' + category)
            results.append(category)

        true_label=self.Get_label('data/test.txt')
        for i in range(0, len(true_label)):
            if true_label[i] == results[i]:
                right_flag += 1
            else:
                wrong_flag += 1
        accuracy = right_flag / (right_flag + wrong_flag)

        print('Accuracy: ' + str(accuracy))
        return accuracy
if __name__=='__main__':
    p=Knn()
    # p.Filter_word()
    #p.Load_model()
    draw_pict=[]
    x_value=[]
    y_value=[]
    k_total=[10,30,50,100,300,500,700,1000,1500,2000]
    for k in k_total:
        acc=p.test_model(k)
        draw_pict.append((k,acc))
    print(draw_pict)
    for i in range(0, 8):
        x_value.append(draw_pict[i][0])
        y_value.append(draw_pict[i][1])
    plt.axis([10, 2000, 0, 1])
    plt.plot(x_value,y_value,color="Red")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title("k值与准确率关系图")
    plt.xlabel("k-value")
    plt.ylabel("Accuracy-value")
    #plt.show()
    plt.savefig("data/k_and_acc.png")