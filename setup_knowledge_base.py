import os

files = {
    "knowledge_base/bug_patterns/off_by_one.md": "# Off-By-One Error\n\nAn off-by-one error occurs when a loop uses an incorrect boundary.\n\nCommon Causes:\n- Using < instead of <= in a loop\n- Forgetting Python ranges are zero-indexed\n\nExample Buggy:\nfor i in range(1, 10):\n    print(items[i])\n\nExample Fixed:\nfor i in range(0, 10):\n    print(items[i])\n\nHow to Fix:\n- Check loop boundaries against list size\n- Use len(list) for upper bound\n",
    "knowledge_base/bug_patterns/infinite_loop.md": "# Infinite Loop\n\nOccurs when a loop condition is never false.\n\nCommon Causes:\n- Loop variable never updated\n- Break statement missing\n\nExample Buggy:\ni = 0\nwhile i < 10:\n    print(i)\n\nExample Fixed:\ni = 0\nwhile i < 10:\n    print(i)\n    i += 1\n\nHow to Fix:\n- Update loop variable inside loop body\n- Ensure condition eventually becomes false\n",
    "knowledge_base/bug_patterns/wrong_comparison.md": "# Wrong Comparison Operator\n\nUsing the wrong operator causes incorrect branching.\n\nCommon Causes:\n- Using = instead of ==\n- Confusing > with >=\n- Comparing string to int\n\nExample Buggy:\nif guess > secret:\n    print('Too high!')\n\nExample Fixed:\nif guess >= secret:\n    print('Too high!')\n\nHow to Fix:\n- Use == for equality checks\n- Re-read boundary conditions carefully\n",
    "knowledge_base/error_types/index_error.md": "# IndexError\n\nRaised when accessing a list at an index that does not exist.\n\nCommon Causes:\n- Accessing index n when list has n elements\n- Off-by-one in loops\n\nExample Buggy:\nitems = [1, 2, 3]\nprint(items[3])\n\nExample Fixed:\nprint(items[2])\n\nHow to Fix:\n- Check index < len(list)\n- Use enumerate() when iterating\n",
    "knowledge_base/error_types/type_error.md": "# TypeError\n\nRaised when an operation is applied to the wrong type.\n\nCommon Causes:\n- Adding string and int without converting\n- Wrong argument types\n\nExample Buggy:\nguess = input('Enter number: ')\nif guess > 50:\n    print('Too high!')\n\nExample Fixed:\nguess = int(input('Enter number: '))\nif guess > 50:\n    print('Too high!')\n\nHow to Fix:\n- Convert input() with int() or float()\n- Use isinstance() to check types\n",
    "knowledge_base/error_types/name_error.md": "# NameError\n\nRaised when a variable or function has not been defined.\n\nCommon Causes:\n- Typo in variable name\n- Using variable before assignment\n- Wrong scope\n\nExample Buggy:\nprint(scroe)\nscore = 10\n\nExample Fixed:\nscore = 10\nprint(score)\n\nHow to Fix:\n- Check for typos, names are case-sensitive\n- Assign variable before use\n- Pass as parameter if inside a function\n",
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"wrote {path}")

print("done")
