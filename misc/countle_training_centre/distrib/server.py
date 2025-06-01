#!/usr/local/bin/python

from re import match
from sys import exit
from time import sleep
from countle_puzzle import generateSolvablePuzzle

def format(s):
    return (s.replace('~E',"\033[0m").replace('~R',"\033[0;1;31m").replace('~N',"\033[0;1;7;31m")
      .replace('~w',"\033[7;37m").replace('~u',"\33[4;31m").replace('~Gr',"\33[0;90m").replace('~r',"\33[0;31m")
      .replace('~G',"\033[0;1;32m").replace('~B',"\033[1;34m")).replace('~W',"\033[1;4;37m")

def banner():
    return format(r"""
  ~R(     *   )    (    
  )\  ` )\  /(   )\   
 (((_)  ( )(_))(((_)  
)\\~E___ ~R(~E_~R(~E_~R()) )\\~E___
~R((~w/ __|~E ~w|_   _|~R((~w/ __|~E
 ~w| (~E__    ~w| |~E   ~w| (~E
  ~w\___|~E   ~w|_|~E    ~w\___|~E

     ~RWelcome to the~E
~NCountle Training Centre!~E
""")

def goal():
    return format(r"""
~RToday's Goal:~E
 ╔════════════════════╗
 ║ ~u1,000,000~E problems ║
 ╚════════════════════╝ 
            ~Gr^consecutive~E
""")

def menu():
    return ("""
Menu:
 [S] Start Challenge
 [H] Help
 [B] Blacklist
 [Q] Quit
 """)

def help():
    return format(r"""~WHow to play?~E

Combine the given numbers using 
  ~Baddition (+)~E, 
  ~Bsubtraction (-)~E, 
  ~Bmultiplication (*)~E, and 
  ~Bdivision(/)~E
to reach the target.

~R!! No negative numbers or fractions allowed !!~E

For e.g.
  ~BTarget: 947
  Nums: 100 7 4 5 9 7~E
  
  Valid solution:
  ~G((100 + 7) * (4 + 5) - 9 - 7)~E
""")

# Blacklisted word, not allowed in input
BLACKLIST = ['breakpoint', 'builtins' 'cat', 'compile', 'dict', 'eval', 'exec', 'getframe',
             'help', 'import', 'input', 'inspect', 'open', 'os', 'sh', 'signal' 'subprocess', 'system']

def blacklist():
    return format(r"""~RBlacklist:~E
 ~rbreakpoint
 builtins
 cat
 compile
 dict
 eval
 exec
 getframe
 help
 import
 input
 inspect
 open
 os
 sh
 signal
 subprocess
 system~E
""")

# Remove breakpoint and help, too powerful
__builtins__.__dict__.pop('breakpoint')
__builtins__.__dict__.pop('help')

def checkAnswer(expr, target):
    result = eval(expr, {'FLAG':"no flag for you", "__builtins__": None})
    return result == target

def challenge():
    for _ in range(1000000):
        n,t = generateSolvablePuzzle()
        print("╔════════════════╗")
        print("║ Puzzle #" + str(_+1).ljust(6) + " ║")
        print("╚════════════════╝")
        print(format(r" ~BTarget: " + str(t) + "\n Nums:"), *n, format(r"~E"), "\n")
        expr = input(" Your Answer:\n > ")
        print()

        if (not match(r"[0-9+\-*/()]+", expr)):
            return (print(format("~RThat is not a valid expression. Read 'Help' for more info.~E")))
        elif (len(expr) > 160):
            return (print(format("~RWhat are you doing with so many characters? Read 'Help' for more info.~E")))
        for _ in BLACKLIST + [str(t)]:
            if _ in expr:
                return (print(format("~RBlacklisted word is not allowed: "+_+"~E")))
        if (not checkAnswer(expr, t)):
            print(format(" ~Rtsk tsk tsk...\n Your answer is wrong!\n I'm dissapointed...~E"))
            exit(0)
        else:
            print(format(" ~GCorrect!~E\n"))
            sleep(0.1) # rate limit
        if (_ == 2): 
            print(format(" ~GCongrats!! Here is your flag:\n   " + FLAG + "~E"))
            exit(0)


FLAG = "flag{placeholder}}"

if __name__ == "__main__":
    print(banner())
    print(goal())
    while (1):
        print(menu())
        choice = input("> ").upper()[0]
        print()
        if (choice == 'S'):
            challenge()
        elif (choice == 'H'):
            print(help())
        elif (choice == 'B'):
            print(blacklist())
        elif (choice == 'Q'):
            exit(0)