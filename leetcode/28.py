class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if not needle:
            return 0
        
        n = len(needle)
        m = len(haystack)
        
        for i in range(m - n + 1):
            if haystack[i:i + n] == needle:
                return i
        return -1

haystack = "sadbutsad"
neddle = "sad"

print(len(haystack), len(neddle), len(haystack) - len(neddle) + 1)  # Output: 5

solution = Solution()
print(solution.strStr(haystack, neddle))  # Output: 2