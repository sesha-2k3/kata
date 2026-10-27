"""
Explanation:
- keep a set for tracking the characters currently inside the window.
- use right pointer to iterate over the string.
- use left pointer to maintain the start of the current substring.
- use a variable to keep hold of the max length of substr.
- while the character at the right pointer is in set,
  then remove the left pointer's element from set.
- move the left pointer one step forward, add right pointer'e element to set
- update the max length variable by window size (right - left + 1).
- return the max length.
"""
# solution 1:
def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        left, best = 0, 0
        for right in range(len(s)):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            seen.add(s[right])
            best = max(best, right - left + 1)
        return best