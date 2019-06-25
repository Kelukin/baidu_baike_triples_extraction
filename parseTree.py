from parseTreeNode import TreeNode
from pyhanlp import *
class Tree:
    def __init__(self, sentence=None):
        # 解析当前句子当中的依存成分， 并且返回目前的中心词
        sentenceParseResult = HanLP.parseDependency(sentence).getWordArray()
        self.lst = []
        self.root = None
        for ele in sentenceParseResult:
            self.lst.append(TreeNode(ele))
        for ele in self.lst:
            if(ele.fa_id != 0):
                self.lst[ele.fa_id].add_son(ele)
            else:
                self.root = ele
    def get_node(self,index):
        return self.lst[index]