from collections import defaultdict

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        s_map, t_map = defaultdict(int), defaultdict(int)

        for s_char in s: 
            s_map[s_char] += 1

        for t_char in t:
            t_map[t_char] += 1

        return s_map == t_map