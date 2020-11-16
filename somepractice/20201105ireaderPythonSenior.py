# 字符串和字节
# 字符串可以保存的数据有非常明确的限制，就是Unicode文本
# 字符串：str
# 字节字符串：bytes
# 字符串用引号包围，字节有引号包围并且前面有个b或B前缀
print(bytes([102,111,112]))
# str
str1 = "adb"
str2 = 'jdk'
str3 = """fkjfkjkd"""
print(type(str3))
# bytes
b1 = b"abd"
print(type(b1))

print(list("foo bar"))
print(list(b"foo bar"))

# 可以使用str.encode或bytes(str)方法把字符串编码成字节数据
print(type(str1.encode()))
print(type(bytes(str2,'utf-8')))

# 可以使用bytes.decode或str(bytes) 方法把字节数据解码成字符串
print(type(b'abd'))
print(type(b'abd'.decode()))
print(type(str(b'abd')))