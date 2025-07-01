This is kind of a dynamic programming problem.

Essentially, for each element $a_i$, we need to 'look back' at all indices less than i to see which previous element would be best to "append" $a_i$ to in the subsequence. 

`dp.cpp` shows a solution that uses 3 arrays to solve the problem, but we actually only need to remember the largest satisfaction for subsequences ending in 0, 1 and 2. This simpler solution is implemented in `simpler.cpp`.

I didn't manage to get a python solution working since python is slow, but it may still be possible to solve it in python :). `dp_timelimitexceeded.py` shows one such example of code that has the correct logic but is too slow.