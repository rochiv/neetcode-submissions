class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # l, r = 0, len(prices) - 1
        # best_buy, best_sell, max_profit = 0, 0, 0

        # while l < r:
        #     buy = prices[l]
        #     sell = prices[r]
        #     profit = sell - buy

        #     if trade > max_profit:
        #         max_profit = trade

        #     if buy < best_buy:
        #         best_buy = buy
        #     else:
        #         l += 1

        #     if sell > best_sell:
        #         best_sell = sell
        #     else:
        #         r -= 1

        max_profit = 0

        for i in range(len(prices)):
            for j in range(len(prices)):
                if j > i:
                    trade = prices[j] - prices[i]
                    if trade > max_profit:
                        max_profit = trade

        return max_profit


