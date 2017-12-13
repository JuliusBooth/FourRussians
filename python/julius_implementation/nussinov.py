import numpy as np

delta = {('A', 'A'):0,('C', 'C'):0,('G', 'G'):0,('U', 'U'):0,('A', 'C'):0, ('A', 'G'):0, ('A', 'U'):1,  ('C', 'A'):0, ('C', 'G'):1, ('C', 'U'):0,  ('G', 'A'):0, ('G', 'C'):1, ('G', 'U'):0,  ('U', 'A'):1, ('U', 'C'):0, ('U', 'G'):0}
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
def nussinov(s,bt=False):
    n= len(s)
    T = np.zeros((n, n))
    for d in range(2,n):
        for i in range(n):
            j=i+d
            if j>= n:
                continue
            T[i,j] = max(T[i+1,j-1]+ delta[(s[i],s[j])],
                         T[i + 1, j],
                         T[i, j - 1],
                         max([T[i,k]+ T[k+1,j] for k in range(i+1,j)]))
    #print(T)
    if bt:
        backtrack(T,n,s)

        return(T[0,n-1])



