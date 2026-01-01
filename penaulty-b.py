class Solution:
    def bestClosingTime(self, c: str) -> int:
        p = 0
        for ch in c:
            if ch == 'Y':
                p += 1
        min_p = p
        ind = 0
        for i in range(len(c)):
            if c[i] == 'Y':
                p -= 1
            else:
                p += 1
            if p < min_p:
                ind = i + 1
                min_p = p
        return ind
