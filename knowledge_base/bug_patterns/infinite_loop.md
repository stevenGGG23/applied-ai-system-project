# Infinite Loop

Occurs when a loop condition is never false.

Common Causes:
- Loop variable never updated
- Break statement missing

Example Buggy:
i = 0
while i < 10:
    print(i)

Example Fixed:
i = 0
while i < 10:
    print(i)
    i += 1

How to Fix:
- Update loop variable inside loop body
- Ensure condition eventually becomes false
