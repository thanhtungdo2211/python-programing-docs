class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        output = []
        for i in range(len(nums)):
            for j in range(i+1,len(nums)):
                if nums[i] + nums[j] == target :
                    output.append(i)
                    output.append(j)
                    break
        return output
print(Solution().twoSum([2,7,11,15],11))    