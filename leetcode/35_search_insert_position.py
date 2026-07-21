from typing import List

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        
        low = 0
        high = len(nums) - 1
        
        while low <= high :
            mid = (low + high) // 2
            if nums[mid] > target:
                high = mid - 1
            elif nums[mid] < target:
                low = mid + 1
            else:
                return mid
        return low

s = Solution()
nums = [1, 3, 5, 6, 7, 10, 5]
target = 10
# print(nums[(2+3)//2])

print(s.searchInsert(nums=nums, target=target))