from parse_abstracts import BaiduCard
from pyhanlp import *
from parseTree import Tree
from parseTreeNode import TreeNode
from parseTree import dic_to_template
import json
CustomDictionary = JClass("com.hankcs.hanlp.dictionary.CustomDictionary") #暂时使用中心词条的方式还没有想好
def process_one_sentence(sentence, title ,template_set = None,output = None):
    tree = Tree(sentence, title)
    resultList = tree.extractTriples(template_set)
    if resultList != []:
        if(output != None) :
            output.write(str(resultList))
            output.write("\n")
        else:
            print(str(resultList))

def load_template():
    template_set = []
    with open("template.json", "r") as f:
        temp = json.loads(f.read())
        for dic in temp:
            template_set.append(dic_to_template(dic))
    return template_set


if __name__ == "__main__":
    inputFile = "sampleResult_5000.txt"
    outputFile = "triples.txt"
    output = open(outputFile,"w",encoding = "utf-8")
    template_set = load_template()
    with open(inputFile,'r') as file:
        cnt = 0
        while cnt < 500:
            line = file.readline()
            cnt +=1
            # print(line)
            # output.write(line)
            line = line.replace("<a>","")
            line = line.replace("</a>","")
            current_card = BaiduCard(line)
            for sentence in current_card.sentences:
                process_one_sentence(sentence, current_card.title,template_set,output)
    output.close()