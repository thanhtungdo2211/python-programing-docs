from typing import Optional
from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        
        def height(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            return 1 + max(height(node.left), height(node.right))
        
        return abs(height(root.left) - height(root.right)) <= 1 and self.isBalanced(root.left) and self.isBalanced(root.right)

def print_tree(root):
    if not root:
        print("None")
        return
    
    # Pretty ASCII print (root, left, right)
    def ascii(node, prefix="", is_left=True):
        if not node:
            print(prefix + ("├─ " if is_left else "└─ ") + "None")
            return
        print(prefix + ("" if prefix == "" else ("├─ " if is_left else "└─ ")) + str(node.val))
        child_prefix = prefix + ("│  " if is_left and prefix != "" else ("   " if prefix != "" else ""))
        ascii(node.left, child_prefix, True)
        ascii(node.right, child_prefix, False)
    ascii(root)

def level_order(root):
    if not root:
        return []
    q = deque([root])
    out = []
    while q:
        node = q.popleft()
        if node:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
        else:
            out.append(None)
    # trim trailing None for a cleaner view
    while out and out[-1] is None:
        out.pop()
    return out

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(2)
root.left.left = TreeNode(3)
root.left.right = TreeNode(3)
root.left.left.left = TreeNode(4)
root.left.left.right = TreeNode(4)

s = Solution()
print(s.isBalanced(root))
print_tree(root)
print(level_order(root))