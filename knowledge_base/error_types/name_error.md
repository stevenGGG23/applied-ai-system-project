# NameError

Raised when a variable or function has not been defined.

Common Causes:
- Typo in variable name
- Using variable before assignment
- Wrong scope

Example Buggy:
print(scroe)
score = 10

Example Fixed:
score = 10
print(score)

How to Fix:
- Check for typos, names are case-sensitive
- Assign variable before use
- Pass as parameter if inside a function
