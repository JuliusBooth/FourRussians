import numpy as np
import itertools

def delta(a,b):
    if a==b: return 1
    else: return 0

def compute_backtrack(s,t,T):
    i,j= len(s), len(t)
    s_align, t_align = [], []
    while i > 0 or j > 0:
        if T[i, j] == T[i, j - 1] + 0:
            j -= 1
            s_align.insert(0, "-")
            t_align.insert(0, t[j])
        elif T[i, j] == T[i - 1, j] + 0:
            i -= 1
            t_align.insert(0, "-")
            s_align.insert(0, s[i])
        else:
            j -= 1
            i -= 1
            s_align.insert(0, s[i])
            t_align.insert(0, t[j])
    while j > 0:
        t_align.insert(0, "-")
        j -= 1
    while i > 0:
        s_align.insert(0, "-")
        i -= 1
    return("".join(s_align),"".join(t_align))

def global_align(s,t,backtrack=False):
    T = np.zeros((len(s)+1, len(t)+1))
    for i in range(len(s)):
        for j in range(len(t)):
            T[i+1,j+1] = max(T[i+1,j],T[i,j+1],T[i,j]+delta(s[i],t[j]))

    if backtrack:
        aligned_s,aligned_t=compute_backtrack(s,t,T)
        print(aligned_s)
        print(aligned_t)
    # print("Final Score:")
    return T[len(s), len(t)]



#TESTING


# def wrapper(func, *args):
#     def wrapped():
#         return func(*args)
#     return wrapped

# import random
# import timeit
# str1 = ''.join(random.choice("AGTC") for x in range(4002))#Number needs to be divisible by t
# str2 = ''.join(random.choice("AGTC") for x in range(4002))
# #print(str1,str2)


# wrapped_regular = wrapper(global_align,str1,str2,False)

# print(timeit.timeit(wrapped_regular,number=1))
