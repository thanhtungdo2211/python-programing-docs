class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        convert_num = str(x)
        if convert_num == convert_num[::-1]:
            return True
        
        return False