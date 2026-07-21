from typing import List

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        # Chỉ số cuối cùng của mảng nums1 sau khi trộn
        last = m + n - 1
        
        # Chỉ số cuối cùng của phần có giá trị trong nums1 và nums2
        i = m - 1  # index cho nums1
        j = n - 1  # index cho nums2
        
        # Trộn từ cuối về đầu (phần tử lớn nhất được đặt ở cuối)
        while i >= 0 and j >= 0:
            if nums1[i] > nums2[j]:
                nums1[last] = nums1[i]
                i -= 1
            else:
                nums1[last] = nums2[j]
                j -= 1
            last -= 1
        
        # Nếu còn phần tử trong nums2, copy vào nums1
        # (Nếu còn phần tử trong nums1, chúng đã ở đúng vị trí)
        while j >= 0:
            nums1[last] = nums2[j]
            j -= 1
            last -= 1
        
        return nums1


s = Solution()

nums1 = [1,2,3,0,0,0]
m = 3
nums2 = [2,5,6]
n = 3

print(s.merge(nums1=nums1,
              m=m,
              nums2=nums2,
              n=n))