class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        map = {}

        for word in strs:
            char_count_map = {chr(i): 0 for i in range(ord("a"), ord("z") + 1)}
            for char in word:
                char_count_map[char] += 1

            if str(char_count_map) in map:
                map[str(char_count_map)].append(word)
            else:
                map[str(char_count_map)] = [word]

        return [v for v in list(map.values())]