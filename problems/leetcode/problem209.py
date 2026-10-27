"""
Explanation:
- keep a variable for current sum of sub array.
- keep two pointers (left and right) to maintain a sliding window.
- set the initial minimum length as infinity.
- loop through the array and add elements to the current sum variable.
- while the current sum >= target, update the minimum length variable 
  using the window size (right - left + 1), subtract the leftmost element, 
  and move the left pointer ahead
- return the minimum length if found, or else return 0.
(since all the numbers are positive, the sum will only increase or 
stay the same when we add elements)
"""
# solution 1 (O(n)):
def minSubArrayLen(self, target: int, nums: list[int]) -> int:
    current_sum = 0
    left = 0
    min_len = float('inf')
    for right in range(len(nums)):
        current_sum += nums[right]
        while current_sum >= target:
            min_len = min(min_len, right - left + 1)
            current_sum -= nums[left]
            left += 1
    return 0 if min_len == float('inf') else min_len