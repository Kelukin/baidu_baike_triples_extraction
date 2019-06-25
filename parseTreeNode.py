relationMap = { #中文表述的关系到实际三元组当中的映射关系
    '主谓关系':1,
    '动宾关系':2,
    '间宾关系':3,
    '前置宾语':4,
    '兼语':5,
    '定中关系':6,
    '状中结构':7,
    '动补结构':8,
    '并列关系':9,
    '介宾关系':10,
    '右附加关系':11,
    '左附加关系':12,
    '独立结构':13,
    '标点符号':14,
    '核心关系':15
}
class TreeNode:
    def __init__(self, sentence_word=None):
        self.fa = None
        self.fa_id = 0
        self.relation_to_fa = 0
        self.content = ""
        self.tagging = ""
        self.son = []
        if sentence_word != None:
            self.tagging = sentence_word.POSTAG
            self.content= sentence_word.LEMMA
            self.relation_to_fa = relationMap[sentence_word.DEPREL]
            self.fa_id = sentence_word.HEAD.ID
    def add_son(self, sonNode):
        self.son.append(sonNode)
        sonNode.fa = self
    def __str__(self):
        return self.content + self.tagging
