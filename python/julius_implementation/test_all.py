import numpy as np
import matplotlib.pyplot as plt
import random
import timeit
import math
from sys import argv
from GlobalAlignment import global_align
from FourRussians import russian_align, gen_LUT

def wrapper(func, *args):
    def wrapped():
        return func(*args)
    return wrapped

# t = int(argv[1])
# preprocess = False if len(argv) < 3 else (argv[2] == 'True')
# preprocess = True
backtrack = False

x = []
y1 = []
y2 = []
y3 = []
y4 = []

LUT2 = (gen_LUT(2,backtrack))
LUT3 = (gen_LUT(3,backtrack))
LUT4 = (gen_LUT(4,backtrack))

# LUT2 = None
# LUT3 = None

# if preprocess:
# 	LUT = (gen_LUT(t,backtrack))#generate lookup table
# else:
# 	LUT = None


for l in range(600, 6000, 300):
    str1 = ''.join(random.choice("AGTC") for x in range(l))#Number needs to be divisible by t
    str2 = ''.join(random.choice("AGTC") for x in range(l))
    x += [l]
    wrapped_regular = wrapper(global_align,str1,str2,backtrack)
    y1 += [timeit.timeit(wrapped_regular,number=1)]
    wrapped_russian = wrapper(russian_align,str1,str2,2,backtrack,LUT2)
    y2 += [timeit.timeit(wrapped_russian,number=1)]
    wrapped_russian = wrapper(russian_align,str1,str2,3,backtrack,LUT3)
    y3 += [timeit.timeit(wrapped_russian,number=1)]
    wrapped_russian = wrapper(russian_align,str1,str2,4,backtrack,LUT4)
    y4 += [timeit.timeit(wrapped_russian,number=1)]
    print('length ' + str(l) + ' done!')

print(x)
print(y1)
print(y2)
print(y3)
print(y4)

xx = np.array(x)
yy1 = np.array(y1)
yy2 = np.array(y2)
yy3 = np.array(y3)
yy4 = np.array(y4)

# plot the data
plt.plot(xx,yy1, label='standard global')
plt.plot(xx,yy2, label='t=2')
plt.plot(xx,yy3, label='t=3')
# plt.plot(xx,yy4, 't=4')
plt.xlabel("Sequence Length")
plt.ylabel('Time')

plt.legend()
plt.show()
plt.savefig('frga_p.jpg')
