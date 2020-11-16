# 字符串拼接
# 1. 效率低的方式
substrings = ["a","b","d"]
s = ""
for substring in substrings:
    s += substring

print(s)

# 2. 效率高的方式

substrings2 = ['d','e','f']
s1 = "".join(substrings2)
print(s1)

# 在字符串之间插入分隔符

substrs3 = ['some','word','haha']
s3 = ','.join(substrs3)
print(s3)

# 字符串格式化方法
str1 = "abc%s"%("def")
print(str1)
str2 = "hello{str3}".format(str3 = "world")
print(str2)