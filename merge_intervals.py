class Solution:
    def merge(self, i: List[List[int]]) -> List[List[int]]:
        i.sort(key=lambda i:i[0])
        o=[]
        for j in i:
            if not o or o[-1][1]<j[0]:
                o.append(j)
            else:
                o[-1]=[o[-1][0],max(o[-1][1],j[1])]
        return o
                



            

        