# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 20:17:20 2020

@author: dell

"""
#导入文件操作
import os

#定义分类器类
class MailClassfier:

    #初始化
    def __init__(self,trainpath):

        self.spam_count=0   #垃圾邮件计数
        self.nspam_count=0  #非垃圾邮件
        self.word_count=0   #词计数
        self.word_set=set() #保存词的set
        self.spamword_dict={}   #保存对应概率
        self.nspamword_dict={}
        self.train(trainpath)

    #训练
    def train(self,path):

        mail_name = os.listdir(path)

        #读取所有邮件
        for name in mail_name:
            with open(path+"\\"+name) as f:
                word_list = f.read().split()

            if name[0]=="s":
                self.spam_count += 1
                for word in word_list:
                    if word.isalpha(): #判断是否包含非字符
                        if word in self.spamword_dict:
                            self.spamword_dict[word]+=1
                        else:
                            self.word_set.add(word)
                            self.spamword_dict[word]=1
            else:
                self.nspam_count += 1
                for word in word_list:
                    if word.isalpha():
                        if word in self.nspamword_dict:
                            self.nspamword_dict[word]+=1
                        else:
                            self.word_set.add(word)
                            self.nspamword_dict[word]=1

        spamword_count=sum(self.spamword_dict.values())
        nspamword_count = sum(self.nspamword_dict.values())
        self.word_count=len(self.word_set)

        #求对应的概率
        for word in self.spamword_dict:
            self.spamword_dict[word]=(1+self.spamword_dict[word])/(spamword_count+self.word_count)
        for word in self.nspamword_dict:
            self.nspamword_dict[word]=(1+self.nspamword_dict[word])/(nspamword_count+self.word_count)

    def test(self,path):

        with open(path) as f:
            word_list = f.read().split()

        #通过商来比较是否为垃圾邮件
        result=1;
        spam_pro=self.spam_count/(self.spam_count+self.nspam_count)
        nspam_pro=self.nspam_count/(self.spam_count+self.nspam_count)
        result*=spam_pro/nspam_pro


        for word in word_list:
            if word in self.word_set:
                if word in self.spamword_dict:
                    spam_pro=self.spamword_dict[word]
                else:
                    spam_pro=1/self.word_count

                if word in self.nspamword_dict:
                    nspam_pro=self.nspamword_dict[word]
                else:
                    nspam_pro=1/self.word_count
                result*=spam_pro/nspam_pro

        if result>=1:
            return 0
        else:
            return 1

if __name__ == '__main__':
    classfier=MailClassfier("train-mails")
    testmail= os.listdir("test-mails")
    confusion_matrix=[[0 for col in range(2)] for row in range(2)]

    for name in testmail:
        if name[0]=="s":
            label=0
        else:
            label=1
        confusion_matrix[classfier.test("test-mails" + "\\" + name)][label]+=1

    #precision，recall，fsore
    precision=confusion_matrix[0][0]/(confusion_matrix[0][0]+confusion_matrix[1][0])
    recall=confusion_matrix[0][0]/(confusion_matrix[0][0]+confusion_matrix[0][1])
    f_score=2*precision*recall/(precision+recall)
    print("confusion_matrix\n",confusion_matrix)
    print("precision\n",precision)
    print("recall\n",recall)
    print("f_score\n",f_score)













