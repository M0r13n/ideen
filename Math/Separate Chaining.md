# Separate Chaining
A different approach for collision resolution than [Open Adressing](Linear%20Probing.md). The process involves a **linked list** at each index in the underlying search array. Colliding items are chained together at the index through a linked list. When searching for a given key $k$ at index $i$ the linked list is traversed. Deletions are performed in a similar way; the key-value pair is removed from the linked list at index $i$.

![Example for separate chaining](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Hash_table_5_0_1_1_1_1_1_LL.svg/675px-Hash_table_5_0_1_1_1_1_1_LL.svg.png)

**Note**: Instead of using a linked list, it might be wise to use a different data structure if the **keys are ordered**. A binary search tree could be used for this. Its main advantage is a reduced lookup time of $O(log(n))$ compared to $O(n)$ of a linked list.
