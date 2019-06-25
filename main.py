from parse_abstracts import BaiduCard
from pyhanlp import *
from parseTree import Tree
from parseTreeNode import TreeNode
CustomDictionary = JClass("com.hankcs.hanlp.dictionary.CustomDictionary") #暂时使用中心词条的方式还没有想好


if __name__ == "__main__":
    inputFile = "sampleResult_5000.txt"
    with open(inputFile,'r') as file:
        cnt = 0
        while cnt < 5:
            line = file.readline()
            cnt +=1
            print(line)
            current_card = BaiduCard(line)
            for sentence in current_card.sentences:
                tree = Tree(sentence)
