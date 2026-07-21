# Given an array nums of size n, return the majority element.
# The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.
# Example 1:

# Input: nums = [3,2,3]
# Output: 3
# Example 2:

# Input: nums = [2,2,1,1,1,2,2]
# Output: 2
from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        freq_map = {}
        n = len(nums)
        majority_count = n // 2
        # Count frequency of each element
        for num in nums:
            print(num)
            print(freq_map)
            print(freq_map.get(num, 0))
            freq_map[num] = freq_map.get(num, 0) + 1
            print(freq_map[num])
        # Find element with frequency > n/2
        for num, count in freq_map.items():
            if count > majority_count:
                return num


s = Solution()
nums = [2, 2, 1, 1, 1, 2, 2]
res = s.majorityElement(nums)
# print(res)
