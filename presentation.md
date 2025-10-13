---
marp: true
theme: default
paginate: true
---

# Quick Sort Algorithm Explanation

---

# Quick Sort: Fundamental Concepts

- Quick Sort is an efficient, comparison-based, in-place sorting algorithm.
- It operates by partitioning an array into two sub-arrays and recursively sorting these sub-arrays.
- A 'pivot' element is selected from the array to facilitate the partitioning process.

---

# Quick Sort Algorithm: Pseudocode

- The core recursive structure of Quick Sort is as follows:
- ```
function quickSort(array, left, right):
  if left < right:
    pivotIndex = partition(array, left, right)
    quickSort(array, left, pivotIndex - 1)
    quickSort(array, pivotIndex + 1, right)
```

---

# The Partition Process: Overview

- The partition routine is the heart of the Quick Sort algorithm.
- Its primary goal is to rearrange elements such that all values less than a chosen pivot are on its left.
- Conversely, all elements greater than the pivot are placed on its right.
- The pivot itself is positioned in its final sorted place within the current sub-array, and its index is returned.

---

# Partition Implementation: Pointer Movement

- Typically, two pointers, 'i' and 'j', are used to manage the partitioning.
- Pointer 'i' tracks the boundary of elements smaller than the pivot.
- Pointer 'j' iterates through the array, comparing elements with the pivot.
- When an element smaller than the pivot is found by 'j', it is swapped with the element at 'i+1', effectively expanding the 'less than pivot' section.

---

# Partition Example Walkthrough

- Let's consider an unsorted array: [4, 3, 1, 7, 9, 11, 8, 2, 5].
- If we select '7' as the pivot element.
- After one pass of the partition routine, the array will be rearranged.
- The array becomes: [4, 3, 1, 2, 5, 7, 9, 11, 8], with '7' now in its correct sorted position.

---

# Recursive Calls on Sub-arrays

- Upon successful partitioning, Quick Sort is then applied recursively to the resulting sub-arrays.
- For our example [4, 3, 1, 2, 5, 7, 9, 11, 8], the pivot '7' is fixed.
- The left sub-array [4, 3, 1, 2, 5] is sorted independently.
- Concurrently, the right sub-array [9, 11, 8] is also sorted through further recursive calls.

---

# Base Case and Algorithm Termination

- The recursion terminates when a sub-array contains zero or one element.
- Arrays with zero or one element are inherently sorted and require no further processing.
- This base case ensures that the algorithm eventually stops and returns the fully sorted array.
- The overall process combines these sorted sub-arrays, without explicit merging, due to the in-place nature.

---

# Pivot Selection Strategies

- The choice of pivot significantly impacts Quick Sort's performance.
- Common strategies include selecting the first, last, or a random element.
- The 'median-of-three' approach, choosing the median of the first, middle, and last elements, is often used to mitigate worst-case scenarios.
- A poorly chosen pivot can lead to unbalanced partitions and degraded performance, approaching O(n^2) time complexity.

---

# Quick Sort: Advantages and Disadvantages

- Advantages include its high efficiency with an average time complexity of O(n log n).
- It is an in-place algorithm, requiring minimal additional space (O(log n) for recursion stack in average case).
- Disadvantages arise in the worst-case scenario, where its time complexity can degrade to O(n^2).
- Quick Sort is also an unstable sorting algorithm, meaning the relative order of equal elements may not be preserved.
