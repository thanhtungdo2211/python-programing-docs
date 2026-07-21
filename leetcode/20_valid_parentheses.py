class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        for c in s:
            if c in '([{':
                stack.append(c)
            elif c == ')':
                if not stack or stack.pop() != '(':
                    return False
            elif c == ']':
                if not stack or stack.pop() != '[':
                    return False
            elif c == '}':
                if not stack or stack.pop() != '{':
                    return False
        return not stack

# Time complexity: O(n)
# Space complexity: O(n)
# n is the length of the input string.

# The code above is a solution to the problem "Valid Parentheses" on LeetCode.
# The problem is to determine if the input string is valid parentheses. 
# An input string is valid if:
# 1. Open brackets must be closed by the same type of brackets.
# 2. Open brackets must be closed in the correct order.
# The input string consists of parentheses only '()[]{}'.
# Example:      
# Input: s = "()"
# Output: True

s = "()]"
s = "()"
results = Solution().isValid(s)
print(results) # True