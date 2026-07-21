from typing import Optional, List
from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:
            return True
        
        if not p or not q:
            return False

        if p.val != q.val:
            return False

        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)

s =  Solution()
p_tree = TreeNode(1)
p_tree.left = TreeNode(2)
p_tree.right = TreeNode(3)

q_tree = TreeNode(1)
q_tree.left = TreeNode(None)
q_tree.right = TreeNode(3)

result = s.isSameTree(p_tree, q_tree)
print(result)