# 每当在一个属性前加上__前缀，解释器就会将其重命名
class MyClass:
    __secret_value = 1

instance_of = MyClass()
# instance_of.__secret_value

print(dir(MyClass))
print(instance_of._MyClass__secret_value)


