import numpy as np
import matplotlib.pyplot as plt
import random
import timeit
import math
from sys import argv
from nussinov import nussinov
from RNA_4_russians import four_russian_fold

def wrapper(func, *args):
    def wrapped():
        return func(*args)
    return wrapped

# t = int(argv[1])
# preprocess = False if len(argv) < 3 else (argv[2] == 'True')
# preprocess = False
backtrack = False

x = []
y1 = []
y2 = []
y3 = []
y4 = []


for l in range(60, 900, 60):
    s = ''.join(random.choice("AGUC") for x in range(l))#Number needs to be divisible by t
    x += [l]
    wrapped_regular = wrapper(nussinov,s,backtrack)
    y1 += [timeit.timeit(wrapped_regular,number=1)]
    wrapped_russian = wrapper(four_russian_fold,s,3,backtrack)
    y2 += [timeit.timeit(wrapped_russian,number=1)]
    wrapped_russian = wrapper(four_russian_fold,s,4,backtrack)
    y3 += [timeit.timeit(wrapped_russian,number=1)]
    wrapped_russian = wrapper(four_russian_fold,s,5,backtrack)
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
plt.plot(xx,yy1, label='standard')
plt.plot(xx,yy2, label='q=3')
plt.plot(xx,yy3, label='q=4')
plt.plot(xx,yy4, label='q=5')

plt.xlabel('Sequence length')
plt.ylabel('Time')

plt.legend()
plt.show()
plt.savefig('frfa.jpg')
