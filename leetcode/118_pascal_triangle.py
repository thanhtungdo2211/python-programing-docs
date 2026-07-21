from typing import List
class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        triangle = []
        for i in range(numRows):
            row = [None for _ in range(i+1)]
            row[0] = 1
            row[i] = 1
            for j in range(1, i):
                row[j] = triangle[i-1][j-1] + triangle[i-1][j]
            triangle.append(row)
        return triangle
    
if __name__ == "__main__":
    s = Solution()
    print(s.generate(5))