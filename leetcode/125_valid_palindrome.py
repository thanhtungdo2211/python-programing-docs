# A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.
# Given a string s, return true if it is a palindrome, or false otherwise.

# Example 1:

# Input: s = "A man, a plan, a canal: Panama"
# Output: true
# Explanation: "amanaplanacanalpanama" is a palindrome.
# Example 2:

# Input: s = "race a car"
# Output: false
# Explanation: "raceacar" is not a palindrome.
# Example 3:

# Input: s = " "
# Output: true
# Explanation: s is an empty string "" after removing non-alphanumeric characters.
# Since an empty string reads the same forward and backward, it is a palindrome.

class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.lower()
        print("1", s)
        
        filtered_chars = []

        for char in s:
            if char.isalnum():
                filtered_chars.append(char)
        print(filtered_chars)
        s = ''.join(filtered_chars)

        # s = ''.join(char for char in s if char.isalnum())
        print("2", s)

        print(s[::-1])

        return s == s[::-1]

solution = Solution()
print(solution.isPalindrome("A man, a plan, a canal: Panama"))
# print(solution.isPalindrome("race a car"))
# print(solution.isPalindrome(" "))