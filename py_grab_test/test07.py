str = "kf;jfks;"
lis = str.split(";")
print(lis)
lis.pop(-1)
print(lis)

# lis1 = []
# lis1.pop()
#
# print(lis1)
str1 = ""

lis3 = str1.split(";")
lis3.pop()
print(lis3)

for li in lis3:
    lis.append(li)

print(lis)
