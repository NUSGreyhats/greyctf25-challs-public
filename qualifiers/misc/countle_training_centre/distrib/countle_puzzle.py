from random import randint, random, sample, shuffle
import math

BIG_NUMBERS = [25, 50, 75, 100]
SMALL_NUMBERS = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]

def generateSolvablePuzzle():
    numBig = randint(1,4)
    numSmall = 6 - numBig
    numbers = sample(BIG_NUMBERS, numBig) + sample(SMALL_NUMBERS, numSmall)
    target = 0
    while (target < 101 or target > 1000):
        target = getRandValidTarget(numbers)

    return (numbers, int(target))

def getRandValidTarget(numbers):
    if (len(numbers) == 1):
        return numbers[0]
    
    i,j = sample(range(len(numbers)),2)
    left, right = numbers[i], numbers[j]
    if (left < right):
        left, right = right, left
    
    restNumbers = list(map(lambda x: x[1], filter(lambda x: x[0] not in [i,j], enumerate(numbers))))

    ops = [lambda a,b: a+b, lambda a,b: a-b, lambda a,b: a*b, lambda a,b: -1 if b==0 or a%b else a/b]
    shuffle(ops)
    while (1):
        newNum = ops.pop(0)(left,right)
        if (newNum == -1): continue

        nextNumbers = [newNum] + restNumbers
        return getRandValidTarget(nextNumbers)
