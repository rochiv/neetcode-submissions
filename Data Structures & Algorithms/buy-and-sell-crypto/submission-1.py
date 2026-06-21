class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_p = 0
        min_buy = prices[0]

        for sell in prices:
            max_p = max(max_p, sell - min_buy)
            min_buy = min(min_buy, sell)

        return max_p

        # ----
        # brute force
        # time complexity: O(n^2)
        # space complexity: O(1)
        # ----
        # max_profit = 0

        # for i in range(len(prices)):
        #     for j in range(len(prices)):
        #         if j > i:
        #             trade = prices[j] - prices[i]
        #             if trade > max_profit:
        #                 max_profit = trade

        # return max_profit


