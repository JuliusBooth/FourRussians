import numpy as np
import itertools
delta = {('A', 'A'):0,('C', 'C'):0,('G', 'G'):0,('U', 'U'):0,('A', 'C'):0, ('A', 'G'):0, ('A', 'U'):1,  ('C', 'A'):0, ('C', 'G'):1, ('C', 'U'):0,  ('G', 'A'):0, ('G', 'C'):1, ('G', 'U'):0,  ('U', 'A'):1, ('U', 'C'):0, ('U', 'G'):0}

def get_binary_differences(s):
    s = tuple(int(m - n) for n, m in zip(s, s[1:]))
    return (s)

def backtrack(T,n,s):
    stack=[]
    fold = [[]]*n
    stack.append((0,n-1))

    while stack:
        i,j = stack.pop()

        if i>j:
            continue
        elif i<n-1 and T[i+1,j] == T[i,j]:
            stack.append((i+1,j))
            fold[i] = s[i]
        elif j>0 and T[i , j- 1] == T[i, j]:
            stack.append((i , j- 1))
            fold[j] = s[j]
        elif T[i+1,j-1]+ delta[(s[i],s[j])] == T[i, j]:
            stack.append((i+1 , j- 1))
            fold[i] = "("+s[i]
            fold[j] = s[j] +")"
        else:
            for k in range(i+1, j):
                if T[i, k] + T[k + 1, j] == T[i, j]:
                    stack.append((i,k))
                    stack.append((k+1, j))

                    break
    fold = "".join(char for char in fold)
    print(fold)


def decode(b):
    x = [0] * (len(b) + 1)
    for i in range(1, len(b) + 1):
        x[i] = x[i - 1] + b[i - 1]
    a = np.array(x)
    return (a)

def binary_strings_hash(b):
    h = {}
    for v_i, v in enumerate(b):
        h[v] = v_i
    return h

def four_russian_fold(s, t, bt=False):
    binary_strings = list(itertools.product(range(2), repeat=t - 1))
    decoded_bi_strings = [decode(s) for s in binary_strings] #for performance
    bi_strings_hash = binary_strings_hash(binary_strings)

    n = len(s)
    T = np.zeros((n, n))
    R = {(0, 0, (0,)):1,(0, 0, (1,)):1}
    for j in range(2, n):
        binary_vectors = {}
        for i in range(j - 1):
            T[i, j] = max(T[i + 1, j - 1] + delta[(s[i], s[j])],
                          T[i, j - 1])
        initialG = (j - 1 )// t
        for i in range(j - 1, -1, -1): # reversed(range(j)): #reverse can be removed
            T[i, j] = max(T[i, j],
                          T[i + 1, j])
            rowG = initialG
            currentG = (i-1)//t
            while rowG >= currentG:
                if rowG < initialG and rowG > currentG:
                    v_i = binary_vectors[rowG]
                    k_star = R[(i, rowG, v_i)]
                    T[i, j] = max(T[i, j],
                                  T[i, k_star-1] + T[k_star, j])
                elif rowG == initialG:
                    if initialG==currentG:break
                    max_val = max([T[i, r-1] + T[r, j] for r in range(initialG*t+1,j+1)])
                    T[i, j] = max(T[i, j], max_val)
                else:
                    if i%t ==0:
                        break
                    max_val = max([T[i, r - 1] + T[r, j] for r in range(i,rowG*t+t)])
                    T[i, j] = max(T[i, j], max_val)
                    break
                rowG -= 1

            #get the binary difference vector after every t rows
            if (i-1) % t == 0 and i+t <= j:
                Vg = T[i:i + t, j]
                vg = get_binary_differences(list(reversed(Vg)))
                binary_vectors[currentG] = bi_strings_hash[vg]

        #generate LUT after every t columns
        if j % t == t - 1 and j!=n:
            g = j // t
            for v_i, v in enumerate(binary_strings):
                V_prime = decoded_bi_strings[v_i]

                for i in range(j):
                    max_val = -100
                    k_star = None

                    for k in range(t):
                        val = T[i, k + g * t] + V_prime[t-k-1]
                        if val > max_val:
                            k_star = k+g*t+1
                            max_val = val

                    R[(i, g, v_i)] = k_star


    if bt:
        backtrack(T,n,s)

    return(T[0, n - 1])
