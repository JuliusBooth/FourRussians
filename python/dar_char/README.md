# globalalign.py
-s, Scoring for a match (default = 2)  

-m, Penalty for mismatching (default = -1) 

-p, Penalty for gap (default = -1)  


Run
```
python globalalign.py
```
and follow instructions

Uses Needleman–Wunsch algorithm for finding pairwise global alignment of two strings

# FourRussians.py

-t, block of size t x t (default = 4)  

-b, penalty for removing or inserting block (default = -1), will be automatically multiplied by t

-s, Scoring for a match (default = 2)

-m, Penalty for mismatching (default = -1)

-p, Penalty for gap (default = -1)

-u, 1 for manual user string input, 0 is default for randomized 1000 nucleotide string

Run
```
python FourRussians.py
```
and follow instructions

Uses Four Russians method to speed up global alignment by pre-calculating the matching score of 4^t x 4^t sized nucleotides in a look-up table (LUT). The LUT can then be used to find the score in log n time when calculating the dynamic programming matrix.

Current progress/ideas/comments:  
-created LUT but only for nucleotides of uppercase (e.g can use AAAA, not aaaa)  
-block alignment works, and provides faster runtime for dp recurrence, however, gives different score than the global pairwise alignment 
