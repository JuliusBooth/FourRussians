#!/usr/bin/env python
import optparse, sys, os, logging, math, numpy, timeit

optparser = optparse.OptionParser()
#optparser.add_option("-d", "--datadir", dest="datadir", default="data", help="data directory (default=data)")
optparser.add_option("-s", "--matchscore", dest="mScore", default=2, type="int", help="Scoring for a match (default=2)")
optparser.add_option("-m", "--mismatch", dest="mismatch", default=-1, type="int", help="Penalty for mismatching (default=-1)")
optparser.add_option("-p", "--gappenalty", dest="gPenalty", default=-1, type="int", help="Penalty for gap (default=-1)")
(opts, _) = optparser.parse_args()

def scoring(a1, a2):
    if a1 == a2:
        return opts.mScore
    elif a1 == '-' or a2 == '-':
    	return opts.gPenalty
    else:
        return opts.mismatch

string1 = raw_input("Enter String 1: ")
string2 = raw_input("Enter String 2: ")
m = len(string1)
n = len(string2)
sys.stderr.write("Initializing matrix... \n")
matrix = numpy.zeros(shape=(m+1,n+1))
# Creating gap value penalities all along 0th column and row
for i in range(0, m+1):
	matrix[i][0] = opts.gPenalty * i
for j in range(n+1, 0):
	matrix[0][j] = opts.gPenalty * j

sys.stderr.write("Calculating DP table... \n")

def wrapper():
	for i in range(1, m+1):
		for j in range(1, n+1):
			match = matrix[i-1][j-1] + scoring(string1[i-1], string2[j-1])
			delete = matrix[i-1][j] + opts.gPenalty
			insert = matrix[i][j-1] + opts.gPenalty
			matrix[i][j] = max(match, delete, insert)

checkalgo = timeit.timeit(wrapper,number=1)

# Traceback Algorithm
sys.stderr.write("Performing traceback... \n")
aligned1 = ''
aligned2 = ''
# start from bottom right of the matrix and move towards top left
i, j = m, n 
align_score = 0
while i > 0 and j > 0:
	score_current = matrix[i][j]
	score_diagonal = matrix[i-1][j-1]
	score_up = matrix[i][j-1]
	score_left = matrix[i-1][j]

	if score_current == score_diagonal + scoring(string1[i-1], string2[j-1]):
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

aligned1 = aligned1[::-1]
aligned2 = aligned2[::-1]

sys.stderr.write("Traceback comeplete... \n")

identity = 0 #for calculating percent identity
score = 0 # total alignment cost

# output alignment with score and identity %  
for x in range(0,len(aligned1)):
	if aligned1[x] == aligned2[x]:
		identity += 1
		score += scoring(aligned1[x], aligned2[x])
	elif aligned1[x] != aligned2[x] and aligned1[x] != '-' and aligned2[x] != '-':
		score += scoring(aligned1[x], aligned2[x])
	elif aligned1[x] == '-' or aligned2[x] == '-':
		score += opts.gPenalty
    
identity = float(identity) / len(aligned1) * 100
    
print aligned1
print aligned2
print 'Identity =', "%3.3f" % identity, 'percent'
print 'Score =', score
print 'DP time = ', checkalgo
