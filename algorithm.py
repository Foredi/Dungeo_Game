from time import time
from collections import deque
from Point import Point
import numpy as np
class Algorithm:
    def __init__(self, height, width, grid):
        self.height = height
        self.path = []
        self.width = width
        self.visited = set()
        self.grid = grid

    def find_path(self, node):
        while node.parent and node.parent.parent:
            self.path.append(node)
            node = node.parent
        return True
    def depth(self, node):
        cnt = 0
        while node.parent and node.parent.parent:
            # self.path.append(node)
            cnt +=1
            node = node.parent
        return  cnt
    def reset(self):
        self.path = []
        self.visited = set()

    def getNeighbours(self, x, y):
        return [
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
            (x + 1, y),
        ]

    def checkVisited(self, point):
        for p in self.visited:
            if p == point:
                return True
        return False

    def getPath(self, start, goal, method, maxdepth= 1000):
        if method == 'DFS':
            self.dfs(start, goal)
            self.path
            return [(p.x, p.y) for p in self.path]
        elif method == 'BFS':
            self.bfs(start, goal)
            self.path.reverse()
            return [(p.x, p.y) for p in self.path]
        elif method == 'DLS':
            self.DLS(start, goal, maxdepth)
            self.path
            return [(p.x, p.y) for p in self.path]
        elif method == 'IDS':
            self.IDS(start, goal)
            self.path
            return [(p.x, p.y) for p in self.path]
        elif method == 'greedy':
            self.greedy(start, goal)
            self.path
            return [(p.x, p.y) for p in self.path]
        elif method == 'astar':
            self.astar(start, goal)
            self.path
            return [(p.x, p.y) for p in self.path]

    def gameTimeOne(self, start, goal, method, maxdepth= 1000):
        if method == "DFS":
            start_time = time()
            self.dfs(start, goal)            
            return ["DFS", time() - start_time]
        elif method == "BFS":
            start_time = time()
            self.bfs(start, goal)
            return ["BFS", time() - start_time]
        elif method == "DLS":
            start_time = time()
            self.DLS(start, goal, maxdepth)
            return ["DLS", time() - start_time]
        elif method == "IDS":
            start_time = time()
            self.IDS(start, goal)
            return ["IDS", time() - start_time]
        elif method == "greedy":
            start_time = time()
            self.greedy(start, goal)
            return ["greedy", time() - start_time]
        elif method == "astar":
            start_time = time()
            self.astar(start, goal)
            return ["astar", time() - start_time]

    def getTimeAll(self, start, goal, maxdepth= 1000):
        methods = ["DFS", "BFS", 'DLS', 'IDS', 'greedy', 'astar']
        list_time = []
        print("Lượt tìm kiếm mới")
        for method in methods:
            time = self.gameTimeOne(start, goal, method, maxdepth)
            print(f'Method {method}: {time}')
            list_time.append(time)
        print("Kết thúc lượt tìm kiếm")
        # print(list_time)
        return list_time
    
    def dfs(self, start, goal):
        self.reset()
        S = Point(start[0], start[1])
        G = Point(goal[0], goal[1])
        stack = [S]
        self.visited.add((S.x, S.y))
                
        while stack:
            value = stack.pop()
            if value.x == G.x and value.y == G.y:
                return self.find_path(value)
            neighbours = self.getNeighbours(value.x, value.y)

            for nx, ny in neighbours:
                if (
                    (nx, ny) not in self.visited
                    and (nx >= 0 and nx < self.height and ny >= 0 and ny < self.width)
                    and (self.grid[nx][ny] != -1)
                ):
                    tmp = Point(nx, ny, par=value)
                    stack.append(tmp)
                    self.visited.add((tmp.x, tmp.y))
    def DLS(self, start, goal, maxdepth):
        self.reset()
        S = Point(start[0], start[1])
        G = Point(goal[0], goal[1])
        stack = [S]
        self.visited.add((S.x, S.y))
        depth_list= []
        while stack:
            value = stack.pop()
            if value.x == G.x and value.y == G.y:
                return self.find_path(value)
            neighbours = self.getNeighbours(value.x, value.y)
            d = self.depth(value)
            depth_list.append(d)
            if d < maxdepth:

                for nx, ny in neighbours:
                    if (
                        (nx, ny) not in self.visited
                        and (nx >= 0 and nx < self.height and ny >= 0 and ny < self.width)
                        and (self.grid[nx][ny] != -1)
                    ):
                        tmp = Point(nx, ny, par=value)
                        stack.append(tmp)
                        self.visited.add((tmp.x, tmp.y))
        return np.max(depth_list)
    def IDS(self, start, goal):
        maxdepth  = 0
        had_find_all = False
        depth_old = 0
        while had_find_all == False:
            result = self.DLS(start, goal, maxdepth)
            if  result == True:
                return result
            maxdepth += 1
            if depth_old == result:
                break
            depth_old  = result
    def greedy(self, start, goal):
        self.reset()
        S = Point(start[0], start[1])
        G = Point(goal[0], goal[1])
        open = [S]
        dist = [S.heuristic_function(G)]
        self.visited.add((S.x, S.y))
        while open:
            idx = dist.index(min(dist))
            value = open.pop(idx)
            dist.pop(idx)
            if value.x == G.x and value.y == G.y:
                return self.find_path(value)

            neighbours = self.getNeighbours(value.x, value.y)
            for nx, ny in neighbours:
                if (
                    (nx, ny) not in self.visited
                    and (nx >= 0 and nx < self.height and ny >= 0 and ny < self.width)
                    and (self.grid[nx][ny] != -1)
                ):
                    tmp = Point(nx, ny, par=value)
                    open.append(tmp)
                    dist.append(tmp.heuristic_function(G))
                    self.visited.add((tmp.x, tmp.y))

    def bfs(self, start, goal):
        self.reset()
        S = Point(start[0], start[1])
        G = Point(goal[0], goal[1])
        queue = deque([S])

        self.visited.add((S.x, S.y))
        while queue:
            value = queue.popleft()
            if value.x == G.x and value.y == G.y:
                return self.find_path(value)

            neighbours = self.getNeighbours(value.x, value.y)
            for nx, ny in neighbours:
                if (
                    (nx, ny) not in self.visited
                    and (nx >= 0 and nx < self.height and ny >= 0 and ny < self.width)
                    and (self.grid[nx][ny] != -1)
                ):
                    tmp = Point(nx, ny, par=value)
                    queue.append(tmp)
                    self.visited.add((tmp.x, tmp.y))
    def astar(self, start, goal):
        self.reset()
        S = Point(start[0], start[1])
        G = Point(goal[0], goal[1])
        open = [S]
        distance = [S.heuristic_function(G)]
        self.visited.add((S.x, S.y))
        while open:
            idx = distance.index(min(distance))
            value = open.pop(idx)
            distance.pop(idx)
            if value.x == G.x and value.y == G.y:
                return self.find_path(value)
            neighbours = self.getNeighbours(value.x, value.y)
            for nx, ny in neighbours:
                if (
                    (nx, ny) not in self.visited
                    and (nx >= 0 and nx < self.height and ny >= 0 and ny < self.width)
                    and (self.grid[nx][ny] != -1)
                ):  
                    tmp = Point(nx, ny, par=value, s=value.s + 1)
                    open.append(tmp)
                    distance.append(tmp.heuristic_function(G) + tmp.s)
                    self.visited.add((tmp.x, tmp.y))