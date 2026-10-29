"""
Explanation:
- since the array is sorted, duplicates are next to each other.
- keep a write pointer r starting at 1 (the first element is always unique).
- loop i from 1 to the end. If nums[i] != nums[i - 1], it's a new unique value:
  copy it to nums[r] and increment r.
- r is the number of unique elements; the first r positions of nums hold them in order.
"""

# solution:
from typing import list


class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        r = 1
        for i in range(1, len(nums)):
            if nums[i] != nums[i - 1]:
                nums[r] = nums[i]
                r += 1
        return r