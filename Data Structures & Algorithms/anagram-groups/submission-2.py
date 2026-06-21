class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        group_dict = dict()

        for word in strs: 
            count = [0] * 26
            for char in word: 
                count[ord(char) - ord("a")] += 1 
            key = tuple(count)
            if key in group_dict: 
                group_dict[key].append(word)
            else: 
                group_dict[key] = [word]
        
        return group_dict.values()