import numpy as np
def my_sort(s):
    print('sort_index')
    li = []
    sort_index = []
    for i in range(s.shape[1]):
        li.append([s[0,i], i])
        li.sort()
    for x in li:
        sort_index.append(x[1])
    return sort_index

