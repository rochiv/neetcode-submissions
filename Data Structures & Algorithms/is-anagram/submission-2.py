class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        s_map, t_map = dict(), dict()

        if len(s) != len(t):
            return False

        for i in s:
            s_map[i] = s_map.get(i, 0) + 1

        for j in t:
            t_map[j] = t_map.get(j, 0) + 1

        if s_map == t_map:
            return True

        return False