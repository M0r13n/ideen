# Swap

The swap is a storage area for anonymous pages,  that have no backing store to fall back to when being purged from memory (e.g. application data), that allows us to page them out to a storage device on demand. Reclaimable pages are not swapped, because they can be restored from disk.

Can be controlled by either `vm.swappiness` (systemwide) or cgroups v2 (per application).

1. **Swappiness Value:**
   - **Lower Values (0-20):** This tells the kernel to avoid swapping anonymous memory (such as application data and stack) as much as possible. This is useful for systems where swapping is significantly slower, like those using spinning disks.
   - **Higher Values (60-100):** This suggests to the kernel that the cost of swapping anonymous memory and file-backed memory (like file caches) is similar. This can be beneficial for systems with faster storage like SSDs, where the penalty for swapping is less severe.
2. **Impact on Memory Types:**
   - **Anonymous Memory:** Includes dynamically allocated memory (e.g., via `malloc`), stack memory, and other memory not associated with file-backed storage.
   - **File-Backed Memory:** Includes file caches, memory-mapped files, and other pages that can be re-read from disk if needed.
3. **Memory "Hotness":**
   - The kernel prefers to keep "hot" (frequently accessed) memory pages in RAM. Swappiness influences the kernel's decision when it needs to choose between swapping out anonymous pages or reclaiming file-backed pages that are not "hot."

Since SSDs provide fast random access reads, the performance penalty for swapping is less severe. Thus, setting `vm.swappiness` to a higher value (e.g., 60-100) makes sense. This allows the kernel to use swap more freely, potentially improving the overall system performance by keeping more file-backed pages in memory.