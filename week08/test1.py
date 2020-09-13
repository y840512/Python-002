# 作业一：

# 区分以下类型哪些是容器序列哪些是扁平序列，哪些是可变序列哪些是不可变序列：

# list 列表
# tuple  元祖，数组
# str  字符串
# dict 字典
# collections.deque 


# 扁平序列:tuple,str,collections.deque 
# 可变序列:dict,list


a=(1,2,3)
print(type(a))

b=[1,2,3]
print(type(b))

c="yang bin"
print(type(c))

d={'name':'yang bin','age':36}
print (type(d))

import time
from collections import deque


e=deque(maxlen=10)
print (e)
e.append(1)
e.append(2)
e.appendleft('a')
e.appendleft('b')
print (e)
print (e.pop())
print (e.pop())
print (e.popleft())
print (e.popleft())
print (e)