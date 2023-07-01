# Linear Probing

A scheme for resolving hash collisions in hash tables. It is a form of **open addressing**: each cell of the hash table stores a single key-value pair. If a collision occurs - the key maps to a cell that is already occupied - linear probing searches the next free cell. Lookups are performed in the same way; by starting at the index by the hash function until finding a matching key or an empty cell.

Lookups, Insertions and Deletions are performed in $$O(1)$$.

![Example collision](https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/HASHTB12.svg/450px-HASHTB12.svg.png)

Approaching a **load factor** $$lf \ge k$$ for some preset f $$k$$ causes the hash table to be resized. By using a new hash function the same existing key-value pairs will hash to entirely different slots. Thus, by **rehashing**, the number of collisions is reduced. Deleted keys can also be omitted if they still existed in the old hash table. Typically, the size of the hash table is doubled for every resize.

When a key is **deleted**, it may be necessary to also move another pair backwards into the emptied cell, to prevent searches for the moved key from incorrectly finding an empty cell: For every key-value pair that follows the emptied slot until the next empty slot, existing pairs need to be moved *upwards* to matching emptied cells according to their hashed key $$h(k)$$.

![Example deletion with moving of a pair](https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Linear_Probing_Deletion.png/825px-Linear_Probing_Deletion.png)

*(Note: The k-v pair at index 3 is not moved upwards, because its hash function does not allow it: $3 \gt 2$. But the pair a index 4 is moved, because its hash value allows for it: $1\lt2$)*