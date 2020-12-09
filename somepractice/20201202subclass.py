# 子类化内置类型

# 1.子类化dict
class DistinctError(ValueError):
    """如果向distinctdict添加重复值，则引发这个错误"""

class distinctdict(dict):
    """不接受重复值的字典"""
    def __setitem__(self, key, value):
        if value in self.values():
            if((key in self and self[key] !=value) or key not in self):
                raise DistinctError(
                    "this value already exists for different key"
                )
        super().__setitem__(key,value)

my = distinctdict()
my['key'] = 'value'
my['other_key'] = 'other_value'
print(my)
# my['other_key'] = 'value'
my["other_key"] = "other_value"
print(my)

# 2.处理序列，子类化list
# class Folder(list):
#     def __init__(self,name):
#         self.name = name
#
#     def dir(self,nesting=0):
#         offset = " " * nesting
#         print('%s%s'%(offset,self.name))
#
#         for element in self:
#             print("ele:"+str(element))
#             if hasattr(element,'dir'):
#                 element.dir(nesting + 1)
#             else:
#                 print("%s   %s"%(offset,element))
#
# tree = Folder('project')
# tree1 = Folder("src")
# tree.append('readme.md')
# tree.append(1)
# tree.append("ff")
# tree.append(tree1)
# tree1.append("hh")
# tree.dir()








































