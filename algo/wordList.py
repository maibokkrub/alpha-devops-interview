from collections import Counter

def solve(list_input, target):
    lookup = set(list_input)

    for i in range(1,len(list_input)):
        front, back = target[:i], target[i:]

        if front in lookup and back in lookup: 
            if front != back: 
                return (front, back)
            # Check for cases where 'aaaa' from ['aa','bb'] should not return
            elif Counter(list_input)[front] > 1: 
                return (front, back)
    return None


print(solve(['aa', 'cd', 'ef', 'gh', 'aa'], 'aaaa'))