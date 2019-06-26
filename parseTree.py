from parseTreeNode import TreeNode
from pyhanlp import *
from triple import Triple
from relationMap import relationMap

class Template:
    def __init__(self, name, text, entity, seg, mid):
        self.template_name = name
        s = text.repalce(entity, "我")
        self.tree = Tree(text,entity)
        self.entity_path = self.__calculate_path("我") #路径从下到上
        self.seg_path = self.__calculate_path(seg)
        self.mid_path = self.__calculate_path(mid, True)
        self.usable = True
        if(self.entity_path == None or self.seg_path == None or self.mid_path == None):
            self.usable = False

    def __calculate_path(self, keyword, is_in = False):
        path = []
        if is_in == True:
            node = self.tree.find_node_logic_in(keyword)
        else:
            node = self.tree.find_node(keyword)
        if node == None:
            return None
        while(node != self.tree.root):
            path.append([node.tagging, node.relation_to_fa])
            node = node.fa
        return path

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
        self.__calculate_depth(self.root, 1)


    def get_node(self,index):
        return self.lst[index]

    def find_node(self, content):
        for node in self.lst:
            if node != None and node.content ==content:
                return node
        return None

    def find_node_logic_in(self, content):
        for node in self.lst:
            if node != None and content in node.content:
                return node
        return None
    

    def __calculate_depth(self, node, depth):#遍历整课书以计算深度
        node.depth = depth
        for son in node.sons:
            self.__calculate_depth(son, depth +1)


    def get_sub_obj_text(self, treeNode, return_id = False):
        text = treeNode.content
        id =  treeNode.id
        for son in treeNode.sons[::-1]:
            if son.relation_to_fa == 6 and son.id == id-1:
                tmp, id = self.get_sub_obj_text(son,True) 
                text = tmp + text
            else:
                break
        if return_id== False:
            return text
        else:
            return (text, id)
    

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

    def __extract_objects_of_one_relation(self, node:TreeNode, tmp_objects:list):
        objectsList = []
        for son in node.sons:
            if son.relation_to_fa == 2:
                objectsList.append(self.get_sub_obj_text(son))
            if son.relation_to_fa == 9:#处理并列关系
                self.__extract_objects_of_one_relation(son, tmp_objects)
            if son.relation_to_fa == 8:
                for son_s_son in son.sons:
                    if son_s_son.relation_to_fa == 10:
                        objectsList.append(self.get_sub_obj_text(son_s_son))
        tmp_objects.append((node.content, objectsList))

    def extractTriples(self):
        tmp_objects = []
        subjects = []
        resultList = []
        # if self.root.content == "是":
        tmpTriple = Triple()
        # tmpTriple.relation = "是"
        tmpTriple.relation = self.root.content
        if tmpTriple.relation in relationMap:
            tmpTriple.relation = relationMap[tmpTriple.relation]
        self.__extract_objects_of_one_relation(self.root,tmp_objects)
        for son in self.root.sons:
            if son.relation_to_fa == 1:#找主语
                subjects.append(self.get_sub_obj_text(son))
        
        for x in subjects:
            if x in self.subject or x == '我':
                for relation,obj_lst in tmp_objects:
                    tmpTriple.relation = relation
                    for y in obj_lst:
                        tmpTriple.obj = x
                        tmpTriple.value = y
                        result = str(tmpTriple)
                        result = result.replace("我", self.subject)
                        result = result.replace("它", self.subject)
                        resultList.append(result)
            
        return resultList


    def extract_by_template(self, template:Template):
        ##使用模板对三元组进行解压
        if template.usable == False:
            return None
        objects = []
        found_entity = False
        found_mid = False
        resultList = []
        relation = template.template_name
        for ele in self.lst:
            if ele == None:
                continue
            if found_entity == False and ele.content == "我" and verify_path(ele, template.entity_path):
                found_entity =True
            if verify_path(ele, template.seg_path):
                objects.append(ele.content)
            if found_mid == False and verify_path(ele, template.mid_path):
                found_mid = True
        if found_entity and found_mid:
            for obj in objects:
                resultList.append(str(Triple(self.subject, relation, obj)))
        return resultList

def verify_path(node:TreeNode, path:list):
    if node.depth != len(path)+1:
        return False
    for tag, relation_to_fa in path:
        if tag != node.tagging or \
            node.relation_to_fa != relation_to_fa:
            return False
        node = node.fa
    return True

