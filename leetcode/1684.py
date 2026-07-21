# You are given a string allowed consisting of distinct characters and an array of strings words. A string is consistent if all characters in the string appear in the string allowed.

# Return the number of consistent strings in the array words.
# Example 1:

# Input: allowed = "ab", words = ["ad","bd","aaab","baa","badab"]
# Output: 2
# Explanation: Strings "aaab" and "baa" are consistent since they only contain characters 'a' and 'b'.
# Example 2:

# Input: allowed = "abc", words = ["a","b","c","ab","ac","bc","abc"]
# Output: 7
# Explanation: All strings are consistent.
# Example 3:

# Input: allowed = "cad", words = ["cc","acd","b","ba","bac","bad","ac","d"]
# Output: 4
# Explanation: Strings "cc", "acd", "ac", and "d" are consistent.
#
class Solution:
    def countConsistentStrings(self, allowed: str, words: List[str]) -> int:
        """
        Time: O(n*m) where n = number of words, m = avg word length
        Space: O(1) since allowed set has max 26 characters
        """
        allowed_set = set(allowed)
        count = 0

        for word in words:
            # Check if all characters in word are in allowed_set
            if all(char in allowed_set for char in word):
                count += 1

        return count

    # Approach 2: Using issubset() (Cleaner)
    def countConsistentStrings_v2(self, allowed: str, words: List[str]) -> int:
        """
        Time: O(n*m)
        Space: O(1)
        """
        allowed_set = set(allowed)
        return sum(1 for word in words if set(word).issubset(allowed_set))

    # Approach 3: Using bit manipulation (Most Optimized for constraints)
    def countConsistentStrings_v3(self, allowed: str, words: List[str]) -> int:
        """
        Time: O(n*m)
        Space: O(1)
        Uses bit masking for even faster character checking
        """
        # Create bitmask for allowed characters
        allowed_mask = 0
        for char in allowed:
            allowed_mask |= 1 << (ord(char) - ord("a"))

        count = 0
        for word in words:
            word_mask = 0
            for char in word:
                word_mask |= 1 << (ord(char) - ord("a"))

            # If word_mask is subset of allowed_mask
            if (word_mask & allowed_mask) == word_mask:
                count += 1

        return count


allowed = "ab"
words = ["ad", "bd", "aaab", "baa", "badab"]

s = Solution()
res = s.countConsistentStrings(allowed, words)

print(res)
