import numpy as np
import itertools

def delta(a,b):
    if a==b: return 1
    else: return 0

def global_align(s,t):
    T = np.zeros((len(s)+1, len(t)+1))
    for i in range(len(s)):
        for j in range(len(t)):

            T[i+1,j+1] = max(T[i+1,j],T[i,j+1],T[i,j]+delta(s[i],t[j]))
    #print(T)
    print(T[len(s), len(t)])


def gen_LUT(t):
    #generates lookup table
    LUT = {}
    dna_strings = ["".join(x) for x in itertools.product("ACGT", repeat=t)]
    binary_strings = list(itertools.product(range(2), repeat=t))

    for bx in binary_strings:
        for by in binary_strings:
            for dx in dna_strings:
                for dy in dna_strings:
                    T = np.zeros((t+1,t+1))
                    for i,binary in enumerate(by):
                        T[i+1,0]=T[i,0]+binary
                    for j,binary in enumerate(bx):
                        T[0,j+1]=T[0,j]+binary
                    for i, s_i in enumerate(dy):
                        for j,t_j in enumerate(dx):
                            T[i+1,j+1]=max(T[i+1,j],T[i,j+1],T[i,j]+delta(s_i,t_j))
                    ox = T[t,:]
                    oy = T[:,t]

                    LUT[(dx,dy,bx,by)] = (ox,oy)
    return(LUT)

def get_binary_differences(s):
    s = tuple(int(m-n) for n,m in zip(s,s[1:]))

    return(s)

def get_array(b,F):
    #NOT USED ANYMORE
    x= [0]*(len(b)) + [F]
    for i in reversed(range(len(b))):
        x[i] = x[i+1]-b[i]
    a = np.array(x)
    return(a)

def russian_align(strS,strT,t):

    LUT = (gen_LUT(t)) #This isn't the rate determining step
    M = np.zeros((len(strS) + 1, len(strT) + 1))


    for j in range(0,len(strT),t):
        dy = strT[j:j + t]
        y = M[j:j + t + 1, 0]
        for i in range(0,len(strS),t):

            A = M[j,i]
            x = M[j,i:i+t+1]

            dx = strS[i:i+t]

            #need to fix this
            bx= get_binary_differences(x) #These 2 calls contribute a lot of time
            by = get_binary_differences(y) #These 2 calls contribute a lot of time

            ox,oy = LUT[(dx,dy,bx,by)] #This is suprisingly fast. Maybe even O(1)
            ox = ox+A
            y = oy+A

            M[j+t,i:i+t+1] = ox
            M[j:j+t + 1, i+t] = y

    print(M[len(strS),len(strT)])





#TESTING


def wrapper(func, *args):
    def wrapped():
        return func(*args)
    return wrapped
import random
import timeit
str1 = ''.join(random.choice("AGTC") for x in range(2100))#Number needs to be divisible by t
str2 = ''.join(random.choice("AGTC") for x in range(2100))

wrapped_lut3 = wrapper(gen_LUT,3)
print(timeit.timeit(wrapped_lut3,number=2))
wrapped_russian = wrapper(russian_align,str1,str2,3)

wrapped_regular = wrapper(global_align,str1,str2)

print(timeit.timeit(wrapped_russian,number=2))
print(timeit.timeit(wrapped_regular,number=2))
