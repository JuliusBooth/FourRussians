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

t = int(argv[1])
preprocess = False if len(argv) < 3 else (argv[2] == 'True')
backtrack = False

x = []
y1 = []
y2 = []

if preprocess:
	LUT = (gen_LUT(t,backtrack))#generate lookup table
else:
	LUT = None



for l in range(600, 4800, 300):
	str1 = ''.join(random.choice("AGTC") for x in range(l))#Number needs to be divisible by t
	str2 = ''.join(random.choice("AGTC") for x in range(l))
	x += [l]


	wrapped_regular = wrapper(global_align,str1,str2,backtrack)
	y1 += [timeit.timeit(wrapped_regular,number=1)]

	wrapped_russian = wrapper(russian_align,str1,str2,t,backtrack,LUT)
	y2 += [timeit.timeit(wrapped_russian,number=1)]

print(x)
print(y1)
print(y2)


xx = np.array(x)
yy1 = np.array(y1)
yy2 = np.array(y2)

# plot the data
plt.plot(xx,yy1)
plt.plot(xx,yy2)
plt.show()
