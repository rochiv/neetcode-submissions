class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        map = {}
        for i in nums:
            map[i] = map.get(i, 0) + 1

        freq_arr = []
        for num, count in map.items():
            freq_arr.append([count, num])
        freq_arr.sort()

        top_k = []
        i = 0
        while len(top_k) < k:
            top_k.append(freq_arr.pop()[1])

        print(f"frequency {freq_arr}")
        print(f"top_k {top_k}")

        return top_k

