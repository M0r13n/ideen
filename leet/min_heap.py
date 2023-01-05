"""
The following statements are true for a min-heap:
-   for any given node C, if P is a parent node of C, then the key (value) of P is
    less than or equal to the key of C.
-   node at the "top" of the heap is called the root node.
- there is no implied ordering between siblings (nodes on the same level)
- the heap relation only applies to nodes and their parents

A min heap could look like this:

       13
     /    \  
   16      31 
  /  \    /  \
41   51  100   41

-> [13, 16, 31, 41, 51, 100, 41]

A min heap can be implemented as a binary tree.
A binary tree can be represented as an array.
"""
#/usr/bin/env python3
import math

def is_leaf(arr, pos):
    """Return True if the node at index pos is a leaf node"""
    li = 2 * pos + 1 
    ri = 2 * pos + 2
    n = len(arr)
    if li < n:
        return False
    if ri < n:
        return False
    return True

def left_child(arr, pos):
    """Get the left child of the element as index pos."""
    return arr[2 * pos + 1]

def right_child(arr, pos):
    """Get the right children of the node at index pos"""
    return arr[2 * pos + 2]

def parent(arr, pos):
    """Get the parent of the node at index pos"""
    return arr[(pos -1 ) // 2 ]

def swap(arr, i, j):
    """swap two nodes in place"""
    arr[i], arr[j] = arr[j], arr[i]

def heapify(arr, i):
    """
    Arrange the current node and its children nodes according to the min-heap property.
    Complexity: O(log(N))
    """
    li = 2 * i + 1 
    ri = 2 * i + 2
    n = len(arr)

    if is_leaf(arr, i):
        return

    if li < n and arr[li] < arr[i]:
        # The left child violates the min-heap property.
        # Swap it with the current element.
        # Afterwards call heapify on the former left child.
        swap(arr,i, li )
        heapify(arr,  li)
    if ri < n and arr[ri] < arr[i]:
        # Same as above - but for the right child
        swap(arr,i, ri )
        heapify(arr, ri)

def heappush(arr, item):
    """Push a new item to the heap.
    Requires the heap to fulfill the heap property (invariant).
    Places the item as a leaf node at the bottom of the tree.
    Then compares it with every of its parents and restores the heap invariant.
    Complexity: O(log(N))
    """
    arr.append(item)
    cur = len(arr) - 1
    while 0 < cur and arr[cur] < parent(arr, cur):
        pi = (cur - 1 ) // 2
        swap(arr, cur, pi )
        cur = pi

def heappop(arr):
    """Pops the smallest node from the heap.
    Swaps the first and the last node.
    Then pops the last element (the former root).
    Afterwards restores the heap property for the new root.
    Complexity: O(log(N))
    """
    swap(arr, 0, len(arr) -1)
    elem = arr.pop()
    heapify(arr, 0)
    return elem

def prettyheap(arr):
    h = math.ceil(math.log(len(arr) , 2)) 
    prev = -1
    for i, j in enumerate(arr):
        layer = math.floor(math.log(i + 1 , 2))
        if layer != prev:
            prev = layer
            print('')
            print(' ' * ((h - layer) * 2), end='')
        
        print(j, end='') 
        print(' ',  end='')

if __name__ == "__main__":
    heap = []
    heappush(heap, 5)
    heappush(heap, 17)
    heappush(heap, 10)
    heappush(heap, 84)
    heappush(heap, 19)
    heappush(heap, 3)
    heappush(heap, 6)
    heappush(heap, 22)
    heappush(heap, 9)
    prettyheap(heap)

    # Heapify a unordered list.
    # In order to this, the heap property must be ensured for each node.
    # This can be achieved by calling `heapify` for every node once.
    # Thus the complexity is O(N * log(N))
    heap = [5,17,10,84,19,3,6,22,9]
    for i in range(len(heap) // 2, -1, -1):
        heapify(heap, i)
    prettyheap(heap)

    heappop(heap)
    prettyheap(heap)
