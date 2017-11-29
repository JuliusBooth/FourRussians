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

-t", block of size t x t (default = 4)
-b", penalty for removing or inserting block (default = -1), will be automatically multiplied by t
-s, Scoring for a match (default = 2)
-m, Penalty for mismatching (default = -1)
-p, Penalty for gap (default = -1)

Uses Four Russians method to speed up global alignment by pre-calculating the matching score of 4^t x 4^t sized nucleotides in a look-up table (LUT). The LUT can then be used to find the score in log n time when calculating the dynamic programming matrix.

Current progress/ideas/comments:
-created LUT but only for nucleotides of lowercase (e.g can't use AAAA, only aaaa)
-trying to get block alignment to work, need to work on dp part to add/remove blocks without getting out of index error
-can get past dp matrix if strings matching (e.g. aaaa with aaaa), but then will get stuck in the while loop of traceback