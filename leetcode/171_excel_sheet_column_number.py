# Given a string columnTitle that represents the column title as appears in an Excel sheet, return its corresponding column number.
# For example:
# A -> 1
# B -> 2
# C -> 3
# ...
# Z -> 26
# AA -> 27
# AB -> 28
# Example 1:
# Input: columnTitle = "A"
# Output: 1
# Example 2:
# Input: columnTitle = "AB"
# Output: 28
# Example 3:

# Input: columnTitle = "ZY"
# Output: 701


class Solution:
    def titleToNumber(self, columnTitle: str) -> int:
        result = 0
        for char in columnTitle:
            # Get the numeric value of character (A=1, B=2, ..., Z=26)
            print(char, ord(char), ord("A"))
            char_value = ord(char) - ord("A") + 1
            exit()
            # Multiply previous result by 26 and add current character value
            # This is like base-26 conversion
            result = result * 26 + char_value

        return result


s = Solution()
columnTitle = "ZY"
res = s.titleToNumber(columnTitle)

print(res)
