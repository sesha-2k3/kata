"""
Explanation:
"""
# solution:
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        max_len = 0
        left = 0
        char_dict = {}
        max_count = 0
        for right in range(len(s)):
            char_dict[s[right]] = char_dict.get(s[right], 0) + 1
            max_count = max(max_count, char_dict[s[right]])
            while (right - left + 1) - max_count > k:
                char_dict[s[left]] -= 1
                left += 1
            max_len = max(max_len, right - left + 1)
        return max_len