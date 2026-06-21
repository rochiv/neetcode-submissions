class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        # nums_dict = dict()
        # for i in nums:
        #     if i in nums_dict: 
        #         return True
        #     else:
        #         nums_dict[i] = 1

        # return False 

        if len(nums) > len(set(nums)):
            return True
        else: 
            return False
