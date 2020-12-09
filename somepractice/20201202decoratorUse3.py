# 代理

class User(object):
    def __init__(self,roles):
        self.roles = roles

class Unauthorized(Exception):
    pass

def protect(role):
    def _protect(function):
        def __protect(*args,**kw):
            user = globals().get('user')
            if user is None or role not in user.roles:
                raise Unauthorized("I won`t tell you")
            return function(*args,**kw)
        return __protect
    return _protect

tarek = User(('admin','user'))
print(tarek.roles)
bill = User('admin')
print(bill.roles)
class MySecrets(object):
    @protect('admin')
    def waffle_recipe(self):
        print('use tons of butter!')
these_are = MySecrets()
user = bill
these_are.waffle_recipe()
print(globals().get('user'))

# 4.上下文提供者
