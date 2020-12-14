# 使用property作为装饰器
class Rectangle:
    def __init__(self,x1,y1,x2,y2):
        self.x1,self.y1 = x1,y1
        self.x2,self.y2 = x2,y2

    @property
    def width(self):
        """rectangle height measured from top"""
        return self.x2 - self.x1

    @width.setter
    def width(self,value):
        self.x2 = self.x1 + value

    @property
    def height(self):
        """rectangle height measured from top"""
        return self.y2 - self.y1

    @height.setter
    def height(self,value):
        self.y2 = self.y1 + value

    def __repr__(self):
        return "{}({},{},{},{})".format(self.__class__.__name__,self.x1,self.y1,self.x2,self.y2)

rectangle = Rectangle(10,10,20,30)
print(rectangle.width,rectangle.height)
rectangle.width = 100
print(rectangle)