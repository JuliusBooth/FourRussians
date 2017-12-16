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

timeit.template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        retval = {stmt}
    _t1 = _timer()
    return retval, _t1 - _t0
"""

l = 1002 if len(argv) < 2 else int(argv[1])
t = int(math.log(l, 3)) if len(argv) < 3 else int(argv[2])

backtrack = False if len(argv) < 4 else (argv[3] == 'backtrack')


s = ''.join(random.choice("AGUC") for x in range(l))#Number needs to be divisible by t

if l < 200:
	print(s)
	print()

print("Regular RNA Folding")
wrapped_regular = wrapper(nussinov,s,backtrack)
res = timeit.timeit(wrapped_regular,number=1)
print('Final Score:', res[0])
print('Time:', res[1])

print("*"*60)

print("Four-Russians RNA Folding")
wrapped_russian = wrapper(four_russian_fold,s,t,backtrack)
res = timeit.timeit(wrapped_russian,number=1)
print('Final Score:', res[0])
print('Time:', res[1])
