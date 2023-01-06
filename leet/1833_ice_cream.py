
import typing as t


class Solution:
    def maxIceCream(self, costs: t.List[int], coins: int) -> int:
        costs = sorted(costs)
        num_bars = 0
        i = 0
        while i < len(costs):
            nxt = costs[i]
            i += 1
            if nxt <= coins:
                num_bars +=1
                coins -= nxt

        return num_bars

if __name__ == "__main__":
    costs, coins = [1,3,2,4,1], 7
    solution = Solution().maxIceCream(costs, coins)
    assert solution == 4

    costs, coins = [10,6,8,7,7,8],  5
    solution = Solution().maxIceCream(costs, coins)
    assert solution == 0

    costs, coins = [1,6,3,1,2,5],  20
    solution = Solution().maxIceCream(costs, coins)
    assert solution == 6

    from random import randint
    import time
    costs = [randint(1, 1000) for _ in range(200000)]
    coins = 2**32
    start = time.time()
    solution = Solution().maxIceCream(costs, coins)
    assert solution == 200000
    print(time.time() - start)
