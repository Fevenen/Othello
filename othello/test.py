import random
#
# lst = [(1, 0, 1), (1, 1, 2), (2, 4, 3)]
# for x in lst:
#     print(x[2])
indexes=[]
lst2=[1,3,5,6,4,6,5]
for i in range(lst2.count(max(lst2))):
    indexes.append(lst2.index(max(lst2)) + i)
    lst2.remove(max(lst2))
print(indexes)