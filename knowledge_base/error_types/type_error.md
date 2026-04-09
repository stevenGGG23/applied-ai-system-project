# TypeError

Raised when an operation is applied to the wrong type.

Common Causes:
- Adding string and int without converting
- Wrong argument types

Example Buggy:
guess = input('Enter number: ')
if guess > 50:
    print('Too high!')

Example Fixed:
guess = int(input('Enter number: '))
if guess > 50:
    print('Too high!')

How to Fix:
- Convert input() with int() or float()
- Use isinstance() to check types
