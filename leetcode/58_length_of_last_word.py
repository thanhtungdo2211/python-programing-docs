class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        stack = []
        for char in s:
            if char == ' ':
                stack.append(0)
            else:
                if not stack or stack[-1] == 0:
                    # print(stack)
                    # exit()
                    stack.append(1)
                else:
                    stack[-1] +=1
        while stack and stack[-1] == 0:
            stack.pop()
        length_of_last_word = stack[-1]
        return length_of_last_word

sol = Solution()
s = "   fly me   to   the moon  "
print(sol.lengthOfLastWord(s))