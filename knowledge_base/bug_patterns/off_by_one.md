# Off-By-One Error

An off-by-one error occurs when a loop uses an incorrect boundary.

Common Causes:
- Using < instead of <= in a loop
- Forgetting Python ranges are zero-indexed

Example Buggy:
for i in range(1, 10):
    print(items[i])

Example Fixed:
for i in range(0, 10):
    print(items[i])

How to Fix:
- Check loop boundaries against list size
- Use len(list) for upper bound
