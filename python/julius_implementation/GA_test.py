import random
import timeit
import math
from sys import argv
from GlobalAlignment import global_align
from FourRussians import russian_align, gen_LUT

timeit.template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        retval = {stmt}
    _t1 = _timer()
    return retval, _t1 - _t0
"""

def wrapper(func, *args):
    def wrapped():
        return func(*args)
    return wrapped


l = 4098 if len(argv) < 2 else int(argv[1])
t = int(math.log2(l) / 4) if len(argv) < 3 else int(argv[2])

preprocess = False if len(argv) < 5 else (argv[4] == 'preprocess')
preprocess = False if len(argv) < 4 else (argv[3] == 'preprocess')

backtrack = False if len(argv) < 5 else (argv[4] == 'backtrack')
backtrack = False if len(argv) < 4 else (argv[3] == 'backtrack')



str1 = ''.join(random.choice("AGTC") for x in range(l))#Number needs to be divisible by t
str2 = ''.join(random.choice("AGTC") for x in range(l))

if l < 200:
	print(str1)
	print(str2)
	print()

print("Regular Global Alignment")
wrapped_regular = wrapper(global_align,str1,str2,backtrack)
res = timeit.timeit(wrapped_regular,number=1)
print('Final Score:', res[0])
print('Time:', res[1])


print("*"*60)

print("Four-Russians Global Alignment")
LUT = (gen_LUT(t,backtrack)) if preprocess else None #generate lookup table
wrapped_russian = wrapper(russian_align,str1,str2,t,backtrack,LUT)
res = timeit.timeit(wrapped_russian,number=1)
print('Final Score:', res[0])
print('Time:', res[1])
