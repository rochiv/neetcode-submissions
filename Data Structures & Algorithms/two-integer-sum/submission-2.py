class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        map_dict = {}

        for i in range(len(nums)):
            if (target - nums[i]) in map_dict:
                return [map_dict[target - nums[i]][0], i]

            if nums[i] not in map_dict:
                map_dict[nums[i]] = [i]
            else:
                map_dict[nums[i]].append(i)