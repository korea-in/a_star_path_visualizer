from math import sqrt
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from random import randint
import copy

WIDTH_SIZE = 40
HEIGHT_SIZE = 40
TILE_SIZE = 8
WALL_COUNT = 10
WALL_SIZE = 8

map_array = [[0 for _ in range(WIDTH_SIZE)] for _ in range(HEIGHT_SIZE)]
distance_array = [[-1 for _ in range(WIDTH_SIZE)] for _ in range(HEIGHT_SIZE)]
g_array = [[-1 for _ in range(WIDTH_SIZE)] for _ in range(HEIGHT_SIZE)]
closed = [[False for _ in range(WIDTH_SIZE)] for _ in range(HEIGHT_SIZE)]
node_queue = []

def q_push(v):
    node_queue.append(v)

def q_pop(idx):
    global node_queue, closed
    r = node_queue[idx]
    node_queue = node_queue[:idx] + node_queue[idx+1:]
    closed[r.y][r.x] = True
    return r

def euclidean_distance(x, y):
    return sqrt( ( (x - (WIDTH_SIZE-1) )**2 ) + ( (y - (HEIGHT_SIZE-1) )**2 ) )

def get_h(x, y):
    global distance_array
    if(distance_array[y][x] == -1):
        distance_array[y][x] = euclidean_distance(x, y)
    return distance_array[y][x]

def extend_node(x, y, g):
    global g_array, node_queue, closed
    if(closed[y][x]): return
    new_node = Node(x, y, g)
    if(g_array[y][x] == -1) :
        g_array[y][x] = g
        q_push(new_node)
    elif(g_array[y][x] > g) :
        g_array[y][x] = g
        for idx, n in enumerate(node_queue):
            if(n.x == x and n.y == y): q_pop(idx)
        q_push(new_node)
    return


class Node():
    def __init__(self, x, y, g):
        self.x = x
        self.y = y
        self.g = g

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.boxes = [[None for _ in range(WIDTH_SIZE)] for _ in range(HEIGHT_SIZE)]
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(grid)

        for h in range(HEIGHT_SIZE):
            for w in range(WIDTH_SIZE):
                label = QLabel(self)
                label.setFixedSize(TILE_SIZE, TILE_SIZE)
                label.setStyleSheet("background-color: #fafafa;")
                self.boxes[h][w] = label
                grid.addWidget(label, h, w)

        self.setWindowTitle('BFS Path Finding')
        self.show()
    
    def updateMap(self, map_array):
        for h in range(HEIGHT_SIZE):
            for w in range(WIDTH_SIZE):
                if(map_array[h][w] == 1): # 시작
                    self.boxes[h][w].setStyleSheet("background-color: #d84141;")
                elif(map_array[h][w] == 2): # 도착
                    self.boxes[h][w].setStyleSheet("background-color: #4b41d8;")
                elif(map_array[h][w] == 3): # 탐색중
                    self.boxes[h][w].setStyleSheet("background-color: #eeee00;")
                elif(closed[h][w]): # 탐색중
                    self.boxes[h][w].setStyleSheet("background-color: #eeee00;")
                elif(map_array[h][w] == 4): # 탐색완료
                    self.boxes[h][w].setStyleSheet("background-color: #aaaaaa;")
                elif(map_array[h][w] == 5): # 최종 경로
                    self.boxes[h][w].setStyleSheet("background-color: #00cc66;")
                elif(map_array[h][w] == 9): # 장애물
                    self.boxes[h][w].setStyleSheet("background-color: #111111;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()

    # 시작지점과 종료지점
    map_array[0][0] = 1
    map_array[HEIGHT_SIZE-1][WIDTH_SIZE-1] = 2

    # 시작지점 초기화
    node_queue=[Node(0, 0, 0)]
    g_array[0][0] = 0

    # 장애물 랜덤 생성
    for i in range(WALL_COUNT):
        obstacle_width = randint(1, WALL_SIZE)
        obstacle_height = randint(1, WALL_SIZE)
        obstacle_x = randint(0, WIDTH_SIZE-1)
        obstacle_y = randint(0, HEIGHT_SIZE-1)
        for j in range(obstacle_height):
            if(obstacle_y + j >= HEIGHT_SIZE): break
            for k in range(obstacle_width):
                if(obstacle_x + k >= WIDTH_SIZE): break

                if(obstacle_y + j < 3 and obstacle_x + k < 3): continue
                if(obstacle_y + j > HEIGHT_SIZE-3 and obstacle_x + k > WIDTH_SIZE-3): continue
                map_array[obstacle_y + j][obstacle_x + k] = 9

    ex.updateMap(map_array)

    #while True:
    while True:
        if(len(node_queue) == 0): break
        # 탐색할 노드 찾기
        min_f = float('inf')
        min_h = float('inf')
        min_idx = -1
        for idx, n in enumerate(node_queue):
            h = get_h(n.x, n.y)
            f = n.g + h
            if (f < min_f) or (f == min_f and h < min_h):
                min_f = f
                min_h = h
                min_idx = idx

        # 탐색 노드 꺼내기
        n = q_pop(min_idx)
        #print(get_h(n.x, n.y), n.g, n.x, n.y)
        
        if(n.x == WIDTH_SIZE-1 and n.y == HEIGHT_SIZE-1): break

        # 확장 가능한 방향 확인
        left_side = True
        right_side = True
        up_side = True
        down_side = True
        if(n.x == 0): left_side = False
        if(n.x == WIDTH_SIZE-1): right_side = False
        if(n.y == 0): up_side = False
        if(n.y == HEIGHT_SIZE-1): down_side = False

        # 가로세로 확장
        if(left_side  and (map_array[n.y][n.x-1] != 9)): extend_node(n.x-1, n.y, n.g+1)
        if(right_side and (map_array[n.y][n.x+1] != 9)): extend_node(n.x+1, n.y, n.g+1)
        if(up_side    and (map_array[n.y-1][n.x] != 9)): extend_node(n.x, n.y-1, n.g+1)
        if(down_side  and (map_array[n.y+1][n.x] != 9)): extend_node(n.x, n.y+1, n.g+1)
        
        # 대각선 확장
        if(left_side  and up_side   and (map_array[n.y-1][n.x-1] != 9)): extend_node(n.x-1, n.y-1, n.g+sqrt(2))
        if(left_side  and down_side and (map_array[n.y+1][n.x-1] != 9)): extend_node(n.x-1, n.y+1, n.g+sqrt(2))
        if(right_side and up_side   and (map_array[n.y-1][n.x+1] != 9)): extend_node(n.x+1, n.y-1, n.g+sqrt(2))
        if(right_side and down_side and (map_array[n.y+1][n.x+1] != 9)): extend_node(n.x+1, n.y+1, n.g+sqrt(2))

        ex.updateMap(map_array)
        QApplication.processEvents()


    sys.exit(app.exec_())
