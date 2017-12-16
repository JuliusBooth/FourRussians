# Usage

To run Four Russians speedup to pairwise global alignment:

./run_GA length_of_sequence t [backtrack] [preprocess]

example:

./run_GA 1002 3
./run_GA 100 2 backtrack
./run_GA 4800 3 preprocess

Note that length of sequence assumed to be multiple of t.

To run Four-Russians speedup to nussinov RNA folding:

./run_nussinov length_of_sequence q [backtrack]

./run_nussinov 900 5
./run_nussinov 100 4 backtrack

Note that length of sequence is assumed to be multiple of q.
