from typing import List

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        k = 0  # Position to place next element not equal to val
        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]
                k += 1
        return k

s = Solution()
nums = [3,2,2,3]
val = 3
print(s.removeElement(nums, val))
# Output: 2
print(nums[:2])  # First k elements: [2,2]