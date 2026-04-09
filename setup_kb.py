import os

files = {
    "knowledge_base/bug_patterns/off_by_one.md": """# Off-By-One Error

## Description
An off-by-one error occurs when a loop or range uses an incorrect boundary, causing it to iterate one too many or one too few times.

## Common Causes
- Using < instead of <= or vice versa in a loop condition
- Forgetting that Python ranges are zero-indexed
- Miscounting list indices (e.g., accessing index n when the last valid index is n-1)

## Example (Buggy)
for i in range(1, 10):  # misses index 0
    print(items[i])

## Example (Fixed)
for i in range(0, 10):
    print(items[i])

## How to Fix
- Double-check loop boundaries against the actual size of your list or range
- Use len(list) to dynamically get the correct upper bound
- Print loop indices during debugging to verify iteration count
""",
    "knowledge_base/bug_patterns/infinite_loop.md": """# Infinite Loop

## Description
An infinite loop occurs when the loop's exit condition is never met, causing the program to run forever or freeze.

## Common Causes
- The loop variable is never updated inside the loop
- The exit condition is always true due to a logic error
- A break statement is missing or unreachable

## Example (Buggy)
i = 0
while i < 10:
    print(i)
    # i never increments

## Example (Fixed)
i = 0
while i < 10:
    print(i)
    i += 1

## How to Fix
- Make sure the loop variable is modified inside the loop body
- Check that the condition will eventually become false
- Use a counter or flag variable as a safety exit if needed
""",
    "knowledge_base/bug_patterns/wrong_comparison.md": """# Wrong Comparison Operator

## Description
Using the wrong comparison operator causes incorrect branching logic.

## Common Causes
- Using = instead of == in a condition
- Confusing > with >= or < with <=
- Comparing a string to an integer without converting types

## Example (Buggy)
if guess > secret:  # should be >= if equal counts as too high
    print("Too high!")

## Example (Fixed)
if guess >= secret:
    print("Too high!")

## How to Fix
- Always use == for equality checks inside conditions
- Carefully re-read boundary conditions against your intended logic
- Add print statements to log compared values during testing
""",
    "knowledge_base/error_types/index_error.md": """# IndexError

## Description
Raised when you try to access a list at an index that doesn't exist.

## Common Causes
- Accessing index n when the list only has n elements (valid: 0 to n-1)
- Hardcoded index that breaks when list size changes
- Off-by-one errors in loops

## Example (Buggy)
items = [1, 2, 3]
print(items[3])  # IndexError

## Example (Fixed)
items = [1, 2, 3]
print(items[2])

## How to Fix
- Check index is less than len(list)
- Use enumerate() instead of manual indexing
- Add bounds checking before accessing elements
""",
    "knowledge_base/error_types/type_error.md": """# TypeError

## Description
Raised when an operation is applied to a value of the wrong type.

## Common Causes
- Adding a string and integer without converting
- Wrong number or type of function arguments
- Iterating over a non-iterable

## Example (Buggy)
guess = input("Enter a number: ")
if guess > 50:  # TypeError: str vs int
    print("Too high!")

## Example (Fixed)
guess = int(input("Enter a number: "))
if guess > 50:
    print("Too high!")

## How to Fix
- Convert input() results with int() or float()
- Check function signatures for expected types
- Use type() or isinstance() to inspect variables
""",
    "knowledge_base/error_types/name_error.md": """# NameError

## Description
Raised when you use a variable or function that hasn't been defined.

## Common Causes
- Typo in a variable name
- Using a variable before it's assigned
- Variable referenced outside its scope

## Example (Buggy)
print(scroe)  # NameError: 'scroe' is not defined
score = 10

## Example (Fixed)
score = 10
print(score)

## How to Fix
- Check for typos, names are case-sensitive
- Make sure the variable is assigned before use
- Pass variables as parameters if needed inside functions
""",
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"wrote {path}")

print("done")
