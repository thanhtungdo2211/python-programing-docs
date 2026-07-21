# You are climbing a staircase. It takes n steps to reach the top.

# Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

class Solution:
    def climbStairs(self, n: int) -> int:
        ways = [0] * (n + 1)

        if n == 0 or n == 1:
            return 1
        
        ways[0], ways[1] = 1, 1

        for i in range(2, n + 1):
            print(i)
            print(ways)
            ways[i] = ways[i - 1] + ways[i - 2]

        return ways[n]

s = Solution()
n = 4
print(s.climbStairs(n=n))  # Output: 8