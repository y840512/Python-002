# 作业二：
# 自定义一个 python 函数，实现 map() 函数的功能。

#1
def seq(x):
    return x * x


list=(1,2,5,10)
rst_list=map(seq,list)
for i in rst_list:
    print (i)

print ('#1 end','#'*20)

#2
def seq(x,y):
    return x + y


# list1=(1,2,5,10)
list1=(5,)
list2=(3,2,5,10,12)
rst_list1=map(seq,list1,list2)
for i in rst_list1:
    print (i)

print ('#2 end','#'*20)