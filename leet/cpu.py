from heapq import heappush, heappop
import time

class Job:
    def __init__(self, i,a,d):
        self.index = i
        self.arr_time =a
        self.duration = d

    def __lt__(self, other):
        if self.duration < other.duration:
            return True
        if self.duration == other.duration:
            return self.index < other.index
        return False

class Solution(object):
    def getOrder(self, tasks):
        # Order tasks after their arrival time & processing time
        sorted_tasks = sorted((Job(x[0], x[1][0], x[1][1]) for x in enumerate(tasks)), key=lambda x: (x.arr_time, x.duration) )

        solution = []
        job_queue = []
        cur_time = 0
        i = 0

        while len(solution) < len(sorted_tasks):
            # Check which jobs can be scheduled for execution
            while i < len(sorted_tasks):
                job = sorted_tasks[i]
                if job.arr_time <= cur_time:
                    heappush(job_queue, job)
                    i += 1
                else:
                    break
            
            if not len(job_queue):
                # Check how long the next job needs to wait
                cur_time = sorted_tasks[i].arr_time
                continue

            # Select the shortest job from all scheduled jobs
            job = heappop(job_queue) 
            solution.append(job.index)
            cur_time += job.duration
                

        return solution


if __name__ == "__main__":
    tasks = [[1000000000,1000000000]]
    solution = Solution().getOrder(tasks)
    assert solution == [0,]

    tasks = [[1,2],[2,4],[3,2],[4,1]]
    solution = Solution().getOrder(tasks)
    assert solution == [0,2,3,1]

    tasks = [[7,10],[7,12],[7,5],[7,4],[7,2]]
    solution = Solution().getOrder(tasks)
    assert solution == [4,3,2,0,1]

    tasks = [[19,13],[16,9],[21,10],[32,25],[37,4],[49,24],[2,15],[38,41],[37,34],[33,6],[45,4],[18,18],[46,39],[12,24]]
    solution = Solution().getOrder(tasks)
    assert solution == [6,1,2,9,4,10,0,11,5,13,3,8,12,7]
    
    now = time.time()
    solution = Solution().getOrder(tasks)
    print(time.time() - now)