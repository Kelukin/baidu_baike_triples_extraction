from parseTree import Tree
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