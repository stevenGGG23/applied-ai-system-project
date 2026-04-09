# Wrong Comparison Operator

Using the wrong operator causes incorrect branching.

Common Causes:
- Using = instead of ==
- Confusing > with >=
- Comparing string to int

Example Buggy:
if guess > secret:
    print('Too high!')

Example Fixed:
if guess >= secret:
    print('Too high!')

How to Fix:
- Use == for equality checks
- Re-read boundary conditions carefully
