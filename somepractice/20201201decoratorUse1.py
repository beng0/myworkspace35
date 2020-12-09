
# 参数检查
rpc_info = {}

def xmlrpc(in_=(),out=(type(None),)):
    def _xmlrpc(function):
        # 注册签名
        func_name = function.__name__
        rpc_info[func_name] = (in_,out)
        def _check_types(elements,types):
            """用来检查类型的子函数"""
            if len(elements) != len(types):
                raise TypeError('argument count is wrong')
            typed = enumerate(zip(elements,types))
            for index,couple in typed:
                arg,of_the_right_type = couple
                if isinstance(arg,of_the_right_type):
                    continue
                raise TypeError(
                    'arg #%d should be %s'%(index,of_the_right_type)
                )
        # 包装过的函数
        def __xmlrpc(*args): #没有允许的关键词
            # 检查输入的内容
            checkable_args = args[1:] # 去掉self
            _check_types(checkable_args,in_)
            # 运行函数
            res = function(*args)
            # 检查输出的内容
            if not type(res) in (tuple,list):
                checkable_res = (res,)
            else:
                checkable_res = res
            _check_types(checkable_res,out)
            # 函数及其类型检查成功
            return res
        return __xmlrpc
    return _xmlrpc

class RPCView:
    @xmlrpc((int,int))
    def meth1(self,int1,int2):
        print('received %d and %d'%(int1,int2))

    @xmlrpc((str,),(int,))
    def meth2(self,phrase):
        print('received %s'%phrase)
        return 1
print(rpc_info)

my = RPCView()
my.meth1(1,2)
my.meth2("2")











