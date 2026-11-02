class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        map = dict()

        for s in strs:
            count = [[chr(i), 0] for i in range(ord("a"), ord("z") + 1)]

            for ch in s:
                count[ord(ch) - 97][1] += 1

            count_tup = [tuple(count[i]) for i in range(len(count))]
            count_tup_tup = tuple(count_tup)

            if count_tup_tup in map:
                map[count_tup_tup].append(s)

            else:
                map[count_tup_tup] = [s]

        return list(map.values())