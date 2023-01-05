#/usr/bin/env python3
"""452. Minimum Number of Arrows to Burst Balloons"""
import typing

class Solution(object):
    def findMinArrowShots(self, points: typing.List[typing.List[int]]) -> int:
        """
        :type points: List[List[int]]
        :rtype: int
        """
        # sort the balloons after their stand & end values
        balloons = sorted(points)
        num_arrows = 0
        i = 0
        # store the length in a variable for quicker repeated access
        length = len(balloons)

        # basic idea: greedy algorithm
        # for each balloon, hit all overlapping balloons.
        # because the list is sorted, I know that for each balloon X all
        # balloons behind X start at the same or a greater x_start than X.
        # I also know that two balloons can not be hit, if: xi_end < xj_start.
        # This means that for each balloon X, I can hit all of his successors
        # until there is a balloon whose x_start is bigger that the smallest
        # x_end of all the currently hit balloons.
        while i < length:
            cur = balloons[i]
            e = cur[1]
            num_arrows += 1
            i += 1

            for nxt in balloons[i:]:
                if e < nxt[0]:
                    break

                e = min(e, nxt[1])
                i += 1

        return num_arrows


if __name__ == "__main__":
    import time
    now = time.time()
    points = [[9,12],[1,10],[4,11],[8,12],[3,9],[6,9],[6,7]] * 500000
    solution = Solution().findMinArrowShots(points)
    assert solution == 2
    then = time.time()

    points = [[10,16],[2,8],[1,6],[7,12]]
    solution = Solution().findMinArrowShots(points)
    assert solution == 2

    points = [[1,2],[3,4],[5,6],[7,8]]
    solution = Solution().findMinArrowShots(points)
    assert solution == 4

    points = [[1,2],[2,3],[3,4],[4,5]]
    solution = Solution().findMinArrowShots(points)
    assert solution == 2

    points = [[-2147483646,-2147483645],[2147483646,2147483647]]
    solution = Solution().findMinArrowShots(points)
    assert solution == 2

    points = [[1,2]]
    solution = Solution().findMinArrowShots(points)
    assert solution == 1

    points = [[1,2], [1,2]]
    solution = Solution().findMinArrowShots(points)
    assert solution == 1

    points = []
    solution = Solution().findMinArrowShots(points)
    assert solution == 0

