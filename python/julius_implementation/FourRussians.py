import numpy as np
import itertools

def delta(a,b):
    if a==b: return 1
    else: return 0


def russian_backtrack(s,t,i,j,T):
    #Generates strings of t-square based on entry coordinate (i,j)
    s_align, t_align = [], []
    while i > 0 and j > 0:
        if T[i, j] == T[i, j - 1] + 0:
            j -= 1
            t_align.insert(0, "-")
            s_align.insert(0, s[j])
        elif T[i, j] == T[i - 1, j] + 0:
            i -= 1
            s_align.insert(0, "-")
            t_align.insert(0, t[i])
        else:
            j -= 1
            i -= 1
            s_align.insert(0, s[j])
            t_align.insert(0, t[i])
    return((i,j),(s_align,t_align))

def gen_LUT(t,backtrack):
    #generates lookup table
    LUT = {}
    dna_strings = ["".join(x) for x in itertools.product("ACGT", repeat=t)]
    binary_strings = list(itertools.product(range(2), repeat=t))
    T = np.zeros((t + 1, t + 1))

    for bx in binary_strings:
        for j, binary in enumerate(bx):
            T[0, j + 1] = T[0, j] + binary
        for by in binary_strings:
            for i, binary in enumerate(by):
                T[i + 1, 0] = T[i, 0] + binary
            for dx in dna_strings:
                for dy in dna_strings:
                    for i, s_i in enumerate(dy):
                        for j,t_j in enumerate(dx):
                            T[i+1,j+1]=max(T[i+1,j],T[i,j+1],T[i,j]+delta(s_i,t_j))

                    back_tracking_ht = {}
                    if backtrack:
                        #generate all possible alignments and endpoints depending on entry point
                        for i in range(1,t+1):
                            j=t
                            (coords),(alignments)=russian_backtrack(dx,dy,i,j,T)
                            back_tracking_ht[i,j] = (coords,alignments)
                        for j in range(1,t):
                            i =t
                            (coords), (alignments) = russian_backtrack(dx, dy, i, j, T)
                            back_tracking_ht[i,j] = (coords,alignments)

                    ox = get_binary_differences(T[t,:]) #last row binary
                    sumbx = sum(bx)
                    oy = get_binary_differences(T[:,t]) #last collumn binary
                    sumby1 = sum(oy)


                    LUT[(dx,dy,bx,by)] = (ox,oy,sumbx,sumby1,back_tracking_ht)
    return(LUT)

def get_binary_differences(s):
    s = tuple(int(m-n) for n,m in zip(s,s[1:]))
    return(s)


def paste_bts(bts,t_length,strS,strT):
    # pretty messy function
    # I got s and t mixed up at some point but it works so whatever
    # backtracks by selecting the right backtracking path and t_square based on the end point of the path through the last t_square
    s = []
    t=[]
    n=len(strS)
    index = len(bts)-1
    side_length=int(n//t_length)
    start,alignment=(bts[index][t_length, t_length])

    s = alignment[1]+s
    t=alignment[0]+t

    while index>0:

        if start==(0,0):
            if index - (side_length+1) < 0:
                break
            index-=(side_length+1)
            start = (t_length,t_length)
            start,alignment = bts[index][start]
            s = alignment[1] + s
            t = alignment[0] + t

        elif start[0]==0:
            start = (t_length, start[1])
            if index - side_length < 0:

                break
            index-=side_length
            start, alignment = bts[index][start]
            s = alignment[1] + s
            t = alignment[0] + t
        else:
            if (index -1)%side_length==0:
                break
            index -= 1
            start = (start[0], t_length)
            start, alignment = bts[index][start]
            s = alignment[1] + s
            t = alignment[0] + t
    #fixes the beginning of alignment
    temp_s= "".join(s).replace("-","")
    temp_t = "".join(t).replace("-","")
    i = strT.find(temp_s)
    j = strS.find(temp_t)
    ss = strT[:i] + "".join(s)
    tt = strS[:j] +"".join(t)
    s_dif = len(ss) - len(tt)
    t_dif= len(tt) - len(ss)
    if s_dif > 0: tt = "-"*s_dif + tt
    if t_dif > 0: ss = "-" * t_dif + ss
    return (tt, ss)


def russian_align(strS,strT,t,backtrack=False, precomputedLUT=None):
    #tried to speed this up as much as possible
    bt_matrices=[]
    if precomputedLUT == None:
        LUT = (gen_LUT(t,backtrack)) #generate lookup table
    else:
        LUT = precomputedLUT


    dx_dic = {i:strS[i:i+t] for i in range(0,len(strS),t)} #for speed
    bx_vec = [(0,)*t]*(len(strS)//t)

    F_vec = [0]*(len(strS)//t + 1)
    for j in range(0,len(strT),t):
        dy = strT[j:j + t]
        by=(0,)*t
        for i in range(0,len(strS),t):
            index = i//t
            A = F_vec[index]

            bx = bx_vec[index]
            dx = dx_dic[i]
            bx,by,sumbx,sumby1,back_tracking_ht = LUT[(dx,dy,bx,by)]
            bt_matrices.append(back_tracking_ht)

            F_vec[index] = A + sumbx + sumby1
            bx_vec[index]=bx
        F_vec = [0] + F_vec[:-1]

    if backtrack:
        aligned_s, aligned_t=paste_bts(bt_matrices,t,strS,strT)
        print(aligned_s)
        print(aligned_t)
    # print("Final Score:")
    #print(M[len(strT),len(strS)])
    return F_vec[-1]
