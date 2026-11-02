class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = dict()
        top_k = list()

        for num in nums:
            counts[num] = counts.get(num, 0) + 1
                    
        sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
        
        for key, val in sorted_counts.items():
            if len(top_k) >= k:
                break
            top_k.append(key)

        return top_k
