class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_p = 0
        min_buy = prices[0]

        for sell in prices:
            trade = sell - min_buy
            max_p = max(max_p, trade)
            min_buy = min(sell, min_buy)

        return max_p