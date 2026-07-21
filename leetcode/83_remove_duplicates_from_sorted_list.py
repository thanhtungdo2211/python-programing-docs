from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        
        current = head
        
        # Duyệt qua danh sách
        while current and current.next:
            # Nếu giá trị hiện tại trùng với giá trị tiếp theo
            if current.val == current.next.val:
                # Bỏ qua node tiếp theo
                current.next = current.next.next
            else:
                # Di chuyển đến node tiếp theo
                current = current.next
        
        return head

s = Solution()
# Helper function to convert a list to a ListNode
def array_to_listnode(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

head = array_to_listnode([1, 1, 3])

# Helper function to print all values in a ListNode
def print_listnode(head):
    values = []
    current = head
    while current:
        values.append(current.val)
        current = current.next
    print(values)

print_listnode(s.deleteDuplicates(head))

print(s.deleteDuplicates(head))