import curses
from curses import wrapper
import time
import queue

maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", "#", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "X", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

def print_maze(maze, stdscr, path):
    RED = curses.color_pair(1)
    BLUE = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, val in enumerate(row):
            if (i,j) in path:
                stdscr.addstr(i, j*2, "X", RED)
            else:
                stdscr.addstr(i, j*2, val, BLUE)
    
def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, val in enumerate(row):
            if val==start:
                return i,j
    
    return None

def find_path(maze, stdscr):
    start = "O"
    end = "X"

    start_pos = find_start(maze, start)
    
    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()

    while not q.empty():
        curr_pos, path = q.get()
        row, col = curr_pos
        
        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.25)
        stdscr.refresh()
        
        
        if maze[row][col]==end:
            return path
        
        neighbours = find_neighbours(maze, row, col)
        for neighbour in neighbours:
            if neighbour in visited:
                continue

            r, c = neighbour
            if maze[r][c]=="#":
                continue

            new_path = path + [neighbour]
            q.put((neighbour, new_path))
            visited.add(neighbour)
            

def find_neighbours(maze, row, col):
    neighbours = []

    if row>0:
        neighbours.append((row-1, col))
    if row+1 < len(maze):
        neighbours.append((row+1, col))
    if col>0:
        neighbours.append((row, col-1))
    if col+1 < len(maze[0]):
        neighbours.append((row, col+1))

    return neighbours

def main(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)

    find_path(maze, stdscr)
    stdscr.getch()

wrapper(main)