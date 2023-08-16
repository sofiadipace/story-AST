def isValid( s: str) -> bool:
    stack = []
    parenthesis = {")": "(", "]": "[", "}": "{"}
    for char in s:
        if char in "({[":

            stack.append(char)

        elif char in ")}]":
            # if not
            if not stack or stack[-1] != parenthesis[char]:
                return False
            stack.pop()

    return len(stack) == 0