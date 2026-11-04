from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagrams = defaultdict(list)

        for s in strs:
            counts = [0 for i in range(26)]
            for c in s:
                counts[ord(c) - ord('a')] += 1

            anagrams[tuple(counts)].append(s)


        return list(anagrams.values())