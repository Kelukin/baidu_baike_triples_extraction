from parseTreeNode import TreeNode
from pyhanlp import *
from triple import Triple

class Tree:
    def __init__(self, sentence=None, subject = ""):
        # 解析当前句子当中的依存成分， 并且返回目前的中心词
        sentenceParseResult = HanLP.parseDependency(sentence).getWordArray()
        # print(HanLP.parseDependency(sentence))
        self.subject = subject
        self.lst = [None]
        self.root = None
        for ele in sentenceParseResult:
            self.lst.append(TreeNode(ele))
        for ele in self.lst:
            if ele == None:
                continue

            if(ele.fa_id != 0):
                self.lst[ele.fa_id].add_son(ele)
            else:
                self.root = ele
    def get_node(self,index):
        return self.lst[index]

    def get_sub_obj_text(self, treeNode):
        text = treeNode.content
        id =  treeNode.id
        for son in treeNode.sons[::-1]:
            if son.relation_to_fa == 6 and son.id == id-1:
                text = self.get_sub_obj_text(son) + text
            else:
                break
        return text
    
    def get_object_text(self, treeNode):
        text = treeNode.content
        id =  treeNode.ID
        for son in treeNode.sons[::-1]:
            if son.relation_to_fa == 6 and son.id == id-1:
                id = son.ID
                text = son.content + text
            else:
                break
        return text

    def extractTriples(self):
        objects = []
        subjects = []
        resultList = []
        if self.root.content == "是":
            tmpTriple = Triple()
            tmpTriple.relation = "是"
            for son in self.root.sons:
                if son.relation_to_fa == 1:
                    subjects.append(self.get_sub_obj_text(son))
                
                if son.relation_to_fa == 2:
                    objects.append(self.get_sub_obj_text(son))
            
            for x in subjects:
                for y in objects:
                    tmpTriple.obj = x
                    tmpTriple.value = y
                    result = str(tmpTriple)
                    result = result.replace("我", self.subject)
                    result = result.replace("它", self.subject)
                    resultList.append(result)
            
        return resultList

                