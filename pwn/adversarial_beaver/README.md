# Details

It's so amazing how they [solved BB-5](https://www.youtube.com/watch?v=rmx3FBPzDuk).

Let's see how well each team can do on BB-100!

# Author

Lord\_Idiot

# Key concepts

TLDR of the challenge is: Given a turing machine that can trivially write OOB (using the infinite tape), how can we craft a turing machine program within 100 states that achieves our exploit objectives?

Since the tape is in global memory (.bss), we can quickly think of overwriting GOT entries (RELRO is disabled).

However, if you naively move the tape head using 1 state for each bit shift, it will take you 64(!) states to even move 8 bytes.
Clearly, this is not going to allow for an exploit under 100 states.

The *pwn* trick here is to remember that the last 3 nibbles of functions are not randomised even in presence of ASLR (due to page alignment).
We can use this idea to write a short turing program that detects a 2 byte chunk that has the 3 nibbles you want to search for.
This can be written in like ~50 states.

Next, you just need a ~<50 state program to perform binary addition, which is not too difficult.
This program will basically bump the victim GOT entry (libc address) into a one\_gadget.

Run the program and get a shell!

# Flag

`grey{congrats_on_solving_BB-100!}`

