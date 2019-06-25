class Triple:
    def __init__(self, obj = "", relation = "", value =""):
        self.obj = obj
        self.relation = relation
        self.value = value

    def __str__(self):
        if self.obj=="" or self.relation == "" or self.value == "" :
            return ""
        return str((self.obj, self.relation, self.value))