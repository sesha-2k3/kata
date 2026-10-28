"""
Explanation:
- keep a variable for current sum, max sum and pointers left and right.
- set the max sum to -infinity (since it is integers).
- iterate through the array and update the current sum.
- when window is larger than the given 'k', move the left and subtract the 
  leftmost element from the current sum.
- if the window is equal to k, then store the max_sum at that point, and continue.
- return the average of max sum.
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

# solution 2:
class Solution1:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        window_sum = 0
        for i in range(k):
            window_sum += nums[i]
        max_sum = window_sum
        for right in range(k, len(nums)):
            left = right - k
            window_sum -= nums[left]
            window_sum += nums[right]
            max_sum = max(max_sum, window_sum)
        return max_sum / k