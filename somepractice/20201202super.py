print(super)

# 访问超类属性
# 不使用super
class Mama: #旧的写法
    def says(self):
        print('do your homework')

class Sister(Mama):
    def says(self):
        Mama.says(self)
        print('and clean you bedroom')

Sister().says()

# 使用super
class Sister1(Mama):
    def says(self):
        super(Sister1,self).says()
        print('and clean your bedroom')

# 或
class Sister2(Mama):
    def says(self):
        super().says()
        print('and clean your bedroom')

Sister1().says()
Sister2().says()