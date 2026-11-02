from collections import defaultdict

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        s_map, t_map = defaultdict(), defaultdict()

        for s_char in s: 
            s_map[s_char] = s_map.get(s_char, 0) + 1

        for t_char in t:
            t_map[t_char] = t_map.get(t_char, 0) + 1

        return s_map == t_map