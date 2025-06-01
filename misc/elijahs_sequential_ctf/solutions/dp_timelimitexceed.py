n = int(input())
A = list(map(int, input().split()))

dp = [-100000000 for i in range(3)]

dp[A[0]] = 0
for x in A[1:]:
 if x == 0:
  dp[0] = max(dp[0], max(dp[1] + 4, dp[2] + 1))
 if x == 1:
  dp[1] = max(dp[0] + 2, max(dp[1], dp[2] + 6))
 if x == 2:
  dp[2] = max(dp[0] + 3, max(dp[1] + 5, dp[2]))
  
print(max(dp))
