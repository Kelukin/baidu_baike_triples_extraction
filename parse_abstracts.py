from pyhanlp import *
from baike_sample import baike_sample
from parseTreeNode import TreeNode
import re
class BaiduCard: # 处理的范围当中不含有特殊的字符
    def __init__(self, line):
        tmp_line = line.split("\t")
        self.title = tmp_line[0]
        tmp_line[2]=tmp_line[2][:-2].replace(self.title,"我") # 把所有的当前词条的名字更改为我
        tmp_line[2] = tmp_line[2].replace("|||","")
        self.sentences = self.splitSentences(tmp_line[2])
        print(self.sentences)
        for i,text in enumerate(self.sentences):
            if "我" not in text:
                self.sentences[i] = "我，"+text
        print(self.sentences)
        #tmp_line[2][:-2].replace(self.title,"我").split("。") #需要实现将全部的感叹号、问号及分号转换为句号
        self.segments = []
        self.size = len(self.sentences)
    
    def segment(self):
        for s in self.sentences:
            lst = []
            for term in HanLP.segment(s):
                lst.append("{}\t{}".format(term.word, term.nature))
            self.segments.append(lst)
    def parseDependency(self):
        for s in self.sentences:
            print(list(HanLP.parseDependency(s).getWordArray()))


    def splitSentences(self,text):
        txts = re.split('。|{\|}+',text)
        ret = []
        for txt in txts:
            ret.append(txt.strip(' |')+'。')
        return ret

    def __str__(self):
        if len(self.segments) == 0:
            self.segment()
        result = self.title + "\n"
        for i in range(self.size):

            result += "{}\n{}\n\n".format(self.sentences[i],"\n".join(self.segments[i]))
        return result

if __name__ == "__main__":
    # inputFile = baike_sample(5000)
    inputFile = "sampleResult_5000.txt"
    with open(inputFile,'r') as file:
        cnt = 0
        while cnt < 5:
            line = file.readline()
            cnt +=1
            print(line)
            current_card = BaiduCard(line)
            current_card.segment()
            print(current_card)
            current_card.parseDependency()
            # print(line.split("\t"))
            # print(HanLP.parseDependency(line[2]))