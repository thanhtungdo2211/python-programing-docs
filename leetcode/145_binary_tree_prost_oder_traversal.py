# Input: root = [1,null,2,3]

# Output: [3,2,1]

from typing import Optional, List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        result = []
        
        def traverse(node):
            if not node:
                return
            
            traverse(node.left)       # Visit left
            traverse(node.right)      # Visit right
            result.append(node.val)   # Visit root
        
        traverse(root)
        return result

root = TreeNode(val=1)
root.left = None
root.right = TreeNode(val=2)
root.left = TreeNode(val=3)

s = Solution()
res = s.postorderTraversal(root=root)
print(res)