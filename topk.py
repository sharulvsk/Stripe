class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        d={}
        for i in nums:
            d[i]=d.get(i,0)+1
        h=[]
        for k,v in d.items():
            heapq.heappush(h,(v,k))
        print(h)