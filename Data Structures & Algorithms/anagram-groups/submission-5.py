class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        map = {}

        for word in strs:
            char_count_map = {chr(i): 0 for i in range(ord("a"), ord("z") + 1)}
            for char in word:
                char_count_map[char] += 1

            map.setdefault(str(char_count_map), []).append(word)

        return list(map.values())