# CLI
This is the first task for the `Blockchain-DevOps` Interview.

## Requirements 
- Python 3.10 

## Algorithm Explanation
Since the task was to search a pair of strings in which, when combined (concatenated), results in the input string. 

The code requires support for any languages, and Python's native string is already unicode. 

There are two inputs in the programs: 
1. The target string (original string)
2. List of strings (will be called as elements)

Here are the basics of how this code works: 

1. Create a hash (set) of all input elements.
2. Split the original string in two halves, and test whether if both of them exists in the set.
3. If those two exist in the set, then the edge case where the splitted elements is identical has to be verified. (e.g. 'aaaa' from 'aa', 'ab') 
   - This could be done by generating counts of the elements, or search to the elements if it existed at least twice. 
4. Return the elemets found, or `None` if not one condition matched.

The output will be returned by the function.

## Testing 
Edit the file locally and run. No interface is provided.

## Time Complexity `O(m+n)`

1. To create a hash set: `O(m)`
2. To find an item in set: `O(1)`
3. To iterate over all possible split points: `O(n)`
4. To create a counting (if the splitted results are the same): `O(m)`

where `m` is the number of elements and `n` is the length of string.

## Space Complexity `O(m+n)`

1. To store a hash set: `O(m)`
2. To store items in set: `O(n)`
3. To create a counting (if the splitted results are the same): `O(m)`

where `m` is the number of elements and `n` is the length of string.

## Improvements
- When the results are identical, it could just iterate over the elements to find if there is at least two found in input elemnts instead of create a whole counting set. (I used counter for simplicity)
