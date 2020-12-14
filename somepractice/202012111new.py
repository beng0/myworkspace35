# 特殊方法__new__()是一种负责创建类实例的静态方法，new方法的调用优先于init
class InstanceCountingClass:
    instances_created = 0

    def __new__(cls, *args, **kwargs):
        print('__new__() called with:', cls, args, kwargs)
        instance = super().__new__(cls)
        instance.number = cls.instances_created
        print(cls.instances_created)
        cls.instances_created += 1
        return instance

    def __init__(self, attribute):
        print('__init__() called with:', self, attribute)
        self.attribute = attribute


instance1 = InstanceCountingClass('abc')
# print(instance1)
instance2 = InstanceCountingClass('abc')
print(instance1.number, instance1.instances_created)
print(instance2.number, instance2.instances_created)
