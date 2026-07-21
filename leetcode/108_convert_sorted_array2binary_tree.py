# Input: nums = [-10,-3,0,5,9]
# Output: [0,-3,9,-10,null,5]
# Explanation: [0,-10,5,null,-3,null,9]

# Input: nums = [1,3]
# Output: [3,1]
# Explanation: [1,null,3] and [3,1] are both height-balanced BSTs.

from typing import List, Optional
from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        if not nums:
            return None
        mid = len(nums) // 2
        root = TreeNode(nums[mid])
        root.left = self.sortedArrayToBST(nums[:mid])
        root.right = self.sortedArrayToBST(nums[mid+1:])
        return root

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

# quick check
s = Solution()
print(s.sortedArrayToBST([-10,-3,0,5,9]))
print_tree(s.sortedArrayToBST([-10,-3,0,5,9]))
print(level_order(s.sortedArrayToBST([-10,-3,0,5,9])))


