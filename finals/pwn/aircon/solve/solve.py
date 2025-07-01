"""
1. Spot that it is possible to buffer flow from `temperature` into `aircon_id`
2. Understand that the check function validates the display temperature on the REMOTE, not the ACTUAL air-con itself
3. Figure out that remote 5 can always be "changed" to 25 degree Celsius since that was its original value
"""

for i in range(10):
    print(1)
    print(5)
    print(int(str(i)+"0019",16))
print("")

"""
1
5
25
1
5
65561
1
5
131097
1
5
196633
1
5
262169
1
5
327705
1
5
393241
1
5
458777
1
5
524313
1
5
589849

"""
