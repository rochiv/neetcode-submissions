class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        
        s_map = {chr(c) : 0 for c in range(ord('a'), ord('z') + 1)}
        t_map = {chr(c) : 0 for c in range(ord('a'), ord('z') + 1)}
        
        for s_char in s:
            s_map[s_char] += 1

        for t_char in t:
            t_map[t_char] += 1

        return s_map == t_map