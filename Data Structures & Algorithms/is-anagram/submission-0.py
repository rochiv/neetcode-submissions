class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        temp_s = dict()
        temp_t = dict()
        
        for char_s in s: 
            if char_s not in temp_s: 
                temp_s[char_s] = 1
            else: 
                temp_s[char_s] += 1

        for char_t in t: 
            if char_t not in temp_t: 
                temp_t[char_t] = 1
            else: 
                temp_t[char_t] += 1

        print(temp_s, temp_t)

        return temp_s == temp_t
        