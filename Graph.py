import time 
import random

def generated_maze():
    rows=int(input("enter row"))
    cols=int(input("enter cols"))
    probability=float(input("enter obstacle probability from 0 to 1"))
    maze=[["#" if random.random()<probability else "." for c in range(cols)] for r in range(rows)]

    maze[0][0]="S"
    maze[rows-1][cols-1]="E"
    maze=["".join(row) for row in maze]        ###remember this line
    for row in maze:
        print(row)
    return maze,(0,0),(rows-1,cols-1)

def get_neighbors(pos):
    r,c=pos
    result=[]
    for cr,cc in [(-1,0),(1,0),(0,1),(0,-1)]:
        nr=cr+r
        nc=cc+c
        if 0<=nr<len(maze) and 0<=nc<len(maze[0]):
            if maze[nr][nc]!="#":
                result.append((nr,nc))
    return result

def bfs(start,end):
    queue=[[start]]
    visited=[start]
    ex=0
    while len(queue)>0:
        path=queue.pop(0)
        node=path[-1]
        ex+=1
        if node==end:
            return path,ex
        for n in get_neighbors(node):
            if n not in visited:
                queue.append(path+[n])
                visited.append(n)
    return None,ex

def dfs(start,end):
    stack=[[start]]
    visited=[start]
    ex=0
    while len(stack)>0:
        path=stack.pop()
        node=path[-1]
        ex+=1
        if node==end:
            return path,ex
        for n in get_neighbors(node):
            if n not in visited:
                stack.append(path+[n])
                visited.append(n)
    return None,ex

def show_path(path):
    if path is None:
        print("path not found")
        return
    grid=[list(row) for row in maze]
    for r,c in path:
        if grid[r][c]==".":      ###  == hota hai naki !=
            grid[r][c]="*"

    for row in grid:
        print("".join(row))

######remember the code 

def print_adjacency_list():
    print("\Ajacency list")
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            node=(r,c)
            neighbors=get_neighbors(node)
            print(node,":",neighbors)

def main():
    global maze
    maze,start,end=generated_maze()
    t1=time.perf_counter()
    bfs_path,bfs_nodes=bfs(start,end)
    bfs_time=(time.perf_counter()-t1)*1000

    t2=time.perf_counter()
    dfs_path,dfs_nodes=dfs(start,end)
    dfs_time=(time.perf_counter()-t2)*1000
    print(len(bfs_path) if bfs_path else print(0), bfs_nodes,bfs_time)           ###don't forget if and else condition
    print(len(dfs_path) if dfs_path else print(0), dfs_nodes,dfs_time)    
    print_adjacency_list()
    
    print("bfs maze")
    show_path(bfs_path)
    print("dfs maze")
    show_path(dfs_path)

main()







import time
import random
from collections import deque


def generated_maze():
    rows = int(input("Enter rows: "))
    cols = int(input("Enter cols: "))
    probability = float(input("Enter obstacle probability (0 to 1): "))

    maze = [
        ["#" if random.random() < probability else "." for c in range(cols)]
        for r in range(rows)
    ]

    maze[0][0] = "S"
    maze[rows - 1][cols - 1] = "E"

    maze = ["".join(row) for row in maze]

    for row in maze:
        print(row)

    return maze, (0, 0), (rows - 1, cols - 1)


# NEW: Convert maze into a graph (Adjacency List)
def build_graph(maze):
    graph = {}

    rows = len(maze)
    cols = len(maze[0])

    for r in range(rows):
        for c in range(cols):

            if maze[r][c] != "#":

                node = (r, c)
                graph[node] = []

                for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                    nr = r + dr
                    nc = c + dc

                    if 0 <= nr < rows and 0 <= nc < cols:
                        if maze[nr][nc] != "#":
                            graph[node].append((nr, nc))

    return graph


# BFS using Graph
def bfs(graph, start, end):
    queue = deque([[start]])
    visited = {start}
    ex = 0

    while queue:
        path = queue.popleft()
        node = path[-1]
        ex += 1

        if node == end:
            return path, ex

        for n in graph[node]:
            if n not in visited:
                queue.append(path + [n])
                visited.add(n)

    return None, ex


# DFS using Graph
def dfs(graph, start, end):
    stack = [[start]]
    visited = {start}
    ex = 0

    while stack:
        path = stack.pop()
        node = path[-1]
        ex += 1

        if node == end:
            return path, ex

        for n in graph[node]:
            if n not in visited:
                stack.append(path + [n])
                visited.add(n)

    return None, ex


def show_path(maze, path):
    if path is None:
        print("Path not found")
        return

    grid = [list(row) for row in maze]

    for r, c in path:
        if grid[r][c] == ".":
            grid[r][c] = "*"

    for row in grid:
        print("".join(row))


def main():
    maze, start, end = generated_maze()

    # NEW: Create graph from maze
    graph = build_graph(maze)

    # Display graph representation
    print("\nGraph (Adjacency List):")
    for node, neighbors in graph.items():
        print(node, "->", neighbors)

    # BFS
    t1 = time.perf_counter()
    bfs_path, bfs_nodes = bfs(graph, start, end)
    bfs_time = (time.perf_counter() - t1) * 1000

    # DFS
    t2 = time.perf_counter()
    dfs_path, dfs_nodes = dfs(graph, start, end)
    dfs_time = (time.perf_counter() - t2) * 1000

    # Performance comparison
    print("\nAlgorithm Comparison")
    print("-" * 60)
    print("Algorithm | Path Length | Nodes Explored | Time (ms)")
    print("-" * 60)

    bfs_length = len(bfs_path) - 1 if bfs_path else 0
    dfs_length = len(dfs_path) - 1 if dfs_path else 0

    print("BFS       |", bfs_length, "|", bfs_nodes, "|", bfs_time)
    print("DFS       |", dfs_length, "|", dfs_nodes, "|", dfs_time)

    print("\nBFS Maze:")
    show_path(maze, bfs_path)

    print("\nDFS Maze:")
    show_path(maze, dfs_path)


main()

