import typing as t
import heapq
import dataclasses

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

@dataclasses.dataclass(order=True)
class HeapNode:
    """Helper class to make ListNodes comparable, so that they can be placed in a heap."""
    val : int
    node : ListNode = dataclasses.field(compare=False)

def heappush(heap, node: ListNode):
    heapq.heappush(heap, HeapNode(node.val, node))

def heappop(heap):
    node = heapq.heappop(heap)
    return node.node


class Solution:
    def mergeKLists(self, lists: t.List[t.Optional[ListNode]]) -> t.Optional[ListNode]:
        if not len(lists):
            return None
        
        min_heap = []

        # Put the start of each linked list in a min heap
        for start in lists:
            if start:
                heappush(min_heap, start)

        # Select the node with lowest value.
        # Append its successors to to the solution while their value is smaller
        # than the value of the smallest node in the queue.
        # As soon as there is a smaller node in the queue, place the current node into the queue.
        # Continue with the smallest node.
        head = last = None

        while len(min_heap):
            nxt: ListNode = heappop(min_heap)
            if head is None:
                head = nxt
                last = nxt
            else:
                last.next = nxt
                last = nxt
            
            if nxt.next:
                heappush(min_heap, nxt.next)

        return head


def stringify(node: ListNode):
    if not node:
        return ""

    s = f"{node.val}"
    while node.next:
        node = node.next
        s += f" -> {node.val}"
    
    return s


if __name__ == "__main__":
    lists = [[1,4,5],[1,3,4],[2,6]]
    linked_lists = []
    for l in lists:
        cur = ListNode(val=l[0])
        linked_lists.append(cur)

        for nxt in l[1:]:
            nxt = ListNode(val=nxt)
            cur.next = nxt
            cur = nxt
    
    solution = Solution().mergeKLists(linked_lists)
    print(stringify(solution))