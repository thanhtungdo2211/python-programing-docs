from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        ...

s = Solution()
head = [1,2,6,3,4,5,6]
val = 6
Output: [1,2,3,4,5]