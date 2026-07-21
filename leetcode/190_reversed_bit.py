# Reverse bits of a given 32 bits signed integer.
# Example 1:
# Input: n = 43261596
# Output: 964176192
# Explanation:
# Integer	Binary
# 43261596	00000010100101000001111010011100
# 964176192	00111001011110000010100101000000

class Solution:
    def reverseBits(self, n: int) -> int:
        res = 0
        for _ in range(32):
            res = (res << 1) | (n & 1)
            n >>= 1
        return res & 0xFFFFFFFF

class Solution:
    def reverseBits(self, n: int) -> int:
        res = 0
        
        for i in range(32):
            # Step 1: Extract the rightmost bit of n
            rightmost_bit = n & 1
            # This is like asking: "Is the rightmost bit 0 or 1?"
            # n & 1 returns:
            #   - 1 if rightmost bit is 1
            #   - 0 if rightmost bit is 0
            
            # Step 2: Make room in result by shifting left
            res = res << 1
            # This shifts all bits in res one position to the left
            # Example: 0010 << 1 becomes 0100
            
            # Step 3: Add the extracted bit to result
            res = res | rightmost_bit
            # The | (OR) operator combines bits:
            #   - If rightmost_bit is 1, it sets the rightmost bit of res to 1
            #   - If rightmost_bit is 0, it keeps the rightmost bit of res as 0
            
            # Step 4: Move to next bit of n by shifting right
            n = n >> 1
            # This removes the rightmost bit we just processed
            # Example: 1101 >> 1 becomes 0110
        
        # Step 5: Ensure result fits in 32 bits (for Python)
        return res & 0xFFFFFFFF

n = 43261596
s = Solution()
res = s.reverseBits(n)
print(res, type(res))