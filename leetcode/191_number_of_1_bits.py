# Example 1:
# Input: n = 11
# Output: 3
# Explanation:
# The input binary string 1011 has a total of three set bits.
# Example 2:
# Input: n = 128
# Output: 1
# Explanation:
# The input binary string 10000000 has a total of one set bit.
# Example 3:
# Input: n = 2147483645
# Output: 30
# Explanation:
# The input binary string 1111111111111111111111111111101 has a total of thirty set bits.
#
class Solution:
    def hammingWeight(self, n: int) -> int:
        # return bin(n).count('1')
        count = 0
        while n:
            count += n & 1  # Check if last bit is 1
            n >>= 1         # Right shift by 1 (divide by 2)
        print(count)
        return count
n = 128
s =  Solution()
res = s.hammingWeight(n)

print(res)
