# IndexError

Raised when accessing a list at an index that does not exist.

Common Causes:
- Accessing index n when list has n elements
- Off-by-one in loops

Example Buggy:
items = [1, 2, 3]
print(items[3])

Example Fixed:
print(items[2])

How to Fix:
- Check index < len(list)
- Use enumerate() when iterating
