"""
Explanation:
"""
# solution 1:
class Solution:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        current_sum = 0
        left, max_sum = 0, float('-inf')
        for right in range(len(nums)):
            current_sum += nums[right]
            if right - left + 1 > k:
                current_sum -= nums[left]
                left += 1
            if right - left + 1 == k:
                max_sum = max(max_sum, current_sum)
        return max_sum / k