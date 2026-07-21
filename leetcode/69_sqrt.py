class Solution:
    def mySqrt(self, x: int) -> int:
        if x == 0:
            return 0
        
        left, right = 1, x
        
        # Binary search để tìm căn bậc hai
        while left <= right:
            mid = left + (right - left) // 2
            
            # Kiểm tra mid²
            if mid <= x // mid:  # Viết thế này để tránh tràn số
                left = mid + 1
            else:
                right = mid - 1
        
        # right là giá trị lớn nhất thỏa mãn right² ≤ x
        return right

s = Solution()
x = 8

print(s.mySqrt(x=x))