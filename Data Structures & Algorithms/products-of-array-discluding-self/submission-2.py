class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        products = []
        left = [1 for _ in range(len(nums))]
        right = [1 for _ in range(len(nums))]

        for i in range(n):
            if i == 0:
                continue
            left[i] = left[i - 1] * nums[i - 1]

        for i in range(n - 1, -1, -1):
            if i == n - 1:
                continue
            right[i] = right[i + 1] * nums[i + 1]

        for i in range(n):
            products.append(left[i] * right[i])

        return products
