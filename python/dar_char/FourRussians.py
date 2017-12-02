#!/usr/bin/env python
import optparse, sys, os, logging, math, numpy

optparser = optparse.OptionParser()
#optparser.add_option("-d", "--datadir", dest="datadir", default="data", help="data directory (default=data)")
optparser.add_option("-t", "--blocksize", dest="tSize", default=0, type="int", help="block of size t x t (default=logn/4) where n = size of string")
optparser.add_option("-b", "--blockpenalty", dest="bPenalty", default=-1, type="int", help="penalty for removing or inserting block (default=(-1)*t)")
optparser.add_option("-s", "--matchscore", dest="mScore", default=2, type="int", help="Scoring for a match (default=2)")
optparser.add_option("-m", "--mismatch", dest="mismatch", default=-1, type="int", help="Penalty for mismatching (default=-1)")
optparser.add_option("-p", "--gappenalty", dest="gPenalty", default=-1, type="int", help="Penalty for gap (default=-1)")
(opts, _) = optparser.parse_args()

sys.stderr.write("INSERT ALL STRINGS IN LOWER CASE!!\n")
string1 = raw_input("Enter String 1: ")
string2 = raw_input("Enter String 2: ")

m = len(string1)
n = len(string2)

t = 0
if opts.tSize != 0: 
	t = opts.tSize
else:
	t = int(math.ceil(math.log10(max(len(string1),len(string2)))/4))

opts.bPenalty = opts.bPenalty * t
#-------------------------------------------------
# Generate lookup table for 4^t x 4^t
sys.stderr.write("Creating Lookup Table...\n")

def align (s1, s2): #scoring for LUT 
	score = 0
	for k in range(0, max(len(s1), len(s2))):
		if(s1[k] == s2[k]):
			score += opts.mScore
		else:
			score += opts.mismatch
	return score

nStrings=[] #nucleotide string
#init all possible blockstrings
for i in range(pow(4, t)):
	nStrings.append("")
#init scores to 0
lut=[]
for i in range(pow(4, t)):
	tscore=[]
	for j in range(pow(4, t)):
		tscore.append(0)
	lut.append(tscore)
#print(lut)
#generate all possible blockstrings, put into blockstrings list
for j in range(t, 0, -1):
	for i in range(pow(4, t)):
		if (i % pow(4,j)) in range(0, pow(4,j-1)):
			nStrings[i]+="a"	
		if (i % pow(4,j)) in range(pow(4,j-1), 2*pow(4,j-1)):
			nStrings[i]+="c"
		if (i % pow(4,j)) in range(2*pow(4,j-1), 3*pow(4,j-1)):
			nStrings[i]+="g"	
		if (i % pow(4,j)) in range(3*pow(4,j-1), (pow(4,j))):
			nStrings[i]+="t"
#print(nStrings)
#align all blockstrings to each other to generate LUT of scores
for i in range(0, pow(4, t)):
	for j in range(0, pow(4, t)):
		s = align(nStrings[i], nStrings[j])
		lut[i][j] = s
#print(lut)

# Hash Table for finding score of nucleotide1 with nucleotide2

hTable = {}
for i, n1 in enumerate(nStrings):
	for j, n2 in enumerate(nStrings):
		hTable[(n1,n2)] = lut[i][j]
#print hTable
sys.stderr.write("LUT complete...\n")
#-------------------------------------------------
def lut_search(i,j): #find LUT for ith block of v and jth block of u
	key = (i,j)
	return hTable[key]

def block_score(b1, b2): #scoring for regular block alignment
	bScore = 0
	for a in range(0,t):
		if b1[a] == b2[a]:
			bScore = opts.mScore
		elif b1[a] == '-' or b2[a] == '-':
			bScore = opts.gPenalty
		else:
			bScore = opts.mismatch
	return bScore

def reg_score(b1,b2): #scoring for global pairwise alignment
	if b1 == b2:
		return opts.mScore
	elif b1 == '-' or b2 == '-':
		return opts.gPenalty
	else: return opts.mismatch

sys.stderr.write("Initializing matrix... \n")
dpMatrix = numpy.zeros(shape=(m+1,n+1))
# Creating gap value penalities all along 0th column and row
for i in range(0, m+1):
	dpMatrix[i][0] = opts.gPenalty * i
for j in range(n+1, 0):
	dpMatrix[0][j] = opts.gPenalty * j

# Dividing up strings into t blocks
blocks1, blocks2 = [], []
for i in range (0,len(string1))[::t]:
	temp = str(string1[i:(i+t)])
	blocks1 = numpy.append(blocks1,temp)

for i in range (0,len(string2))[::t]:
	temp = str(string2[i:(i+t)])
	blocks2 = numpy.append(blocks2,temp)

sys.stderr.write("Calculating DP table... \n")
for i in range(1, len(blocks1)+1):
	for j in range(1, len(blocks2)+1):
		match = dpMatrix[i-1][j-1] + lut_search(blocks1[i-1], blocks2[j-1])
		delete = dpMatrix[i-1][j] + opts.bPenalty
		insert = dpMatrix[i][j-1] + opts.bPenalty
		dpMatrix[i][j] = max(match, delete, insert)
		#print dpMatrix[i][j]

# Traceback Algorithm
sys.stderr.write("Performing traceback... \n")
aligned1 = ''
aligned2 = ''
# start from bottom right of the matrix and move towards top left
i, j = m, n 
align_score = 0
while i > 0 and j > 0:
	score_current = dpMatrix[i][j]
	score_diagonal = dpMatrix[i-1][j-1]
	score_up = dpMatrix[i][j-1]
	score_left = dpMatrix[i-1][j]

	if score_current == score_diagonal + reg_score(string1[i-1], string2[j-1]):
		aligned1 += string1[i-1]
		aligned2 += string2[j-1]
		i -= 1
		j -= 1
	elif score_current == score_left + opts.gPenalty:
		aligned1 += string1[i-1]
		aligned2 += '-'
		i -= 1
	elif score_current ==  score_up + opts.gPenalty:
		aligned1 += '-'
		aligned2 += string2[j-1]
		j -= 1

sys.stderr.write("Traceback comeplete... \n")

aligned1 = aligned1[::-1]
aligned2 = aligned2[::-1]

identity = 0 #for calculating percent identity
score = 0 # total alignment cost

# output alignment with score and identity %  
for x in range(0,len(aligned1)):
	if aligned1[x] == aligned2[x]:
		identity += 1
		score += reg_score(aligned1[x], aligned2[x])
	elif aligned1[x] != aligned2[x] and aligned1[x] != '-' and aligned2[x] != '-':
		score += reg_score(aligned1[x], aligned2[x])
	elif aligned1[x] == '-' or aligned2[x] == '-':
		score += opts.gPenalty
    
identity = float(identity) / len(aligned1) * 100
    
print 'Identity =', "%3.3f" % identity, 'percent'
print 'Score =', score
print aligned1
print aligned2
