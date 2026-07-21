from typing import List

class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        for i in range(len(digits) - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits
            digits[i] = 0
        return [1] + digits


s = Solution()
digits = [1, 1, 9, 9]
# digits = [9]
print(s.plusOne(digits))  # Output: [1, 2, 4]