class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        temp = dict() 

        for i in range(len(nums)): 
            x = target - nums[i]
            if x in temp: 
                return [temp[x], i]
            else:     
                temp[nums[i]] = i 
