import collections
from queue import PriorityQueue
import copy
import pygame
import time
import sys
from time import sleep

"""
    Kí hiệu ở file text
    @: agent
    $: box
    .: destination
    #: wall/object
    *: box on destination
    +: agent on destination
"""


GRAY = (100, 100, 100)
# các hướng đi trong game
'0-------------------------->'
'|                          y'
'|'
'|'
'|'
'|'
'|'
'|'
'v  x'
possibleMoves = {'U': [-1, 0], 'R': [0, 1], 'D': [1, 0], 'L': [0, -1]}


def bfs(filename):
    board = []  # board 2 chiều dùng để input map
    boardBoxAgent = []  # board 2 chiều chỉ chứa box và agent
    boardWallDestination = []  # board 2 chiều chỉ chứa tường và đích
    maxHeightBoard = 0  # height của board
    lines = 0  # width của board

    # đọc và input map từ file
    with open(filename, 'r') as f:
        for row in f.read().splitlines():
            board.append(row)
            lines += 1
            if len(row) > maxHeightBoard:
                maxHeightBoard = len(row)

    # fill 2 board trên với các kí tự "-"
    for i in range(0, lines):
        boardBoxAgent.append([])
        boardWallDestination.append([])
        for j in range(0, maxHeightBoard):
            boardBoxAgent[-1].append('-')
            boardWallDestination[-1].append('-')

    # fill height ở mỗi dòng của board cho đủ tránh bị out of range nếu ở file text thiếu kí tự khi xuống dòng
    for i in range(0, len(board)):
        if len(board[i]) < maxHeightBoard:
            for j in range(len(board[i]), maxHeightBoard):
                board[i] += ' '

    # fill 2 board cần làm việc tương ứng với từng kí tự input
    for i in range(0, len(board)):
        for j in range(0, maxHeightBoard):
            if board[i][j] == '$' or board[i][j] == '@':
                boardBoxAgent[i][j] = board[i][j]
                boardWallDestination[i][j] = ' '
            elif board[i][j] == '.' or board[i][j] == '#':
                boardWallDestination[i][j] = board[i][j]
                boardBoxAgent[i][j] = ' '
            elif board[i][j] == ' ':
                boardBoxAgent[i][j] = ' '
                boardWallDestination[i][j] = ' '
            elif board[i][j] == '*':
                boardBoxAgent[i][j] = '$'
                boardWallDestination[i][j] = '.'
            elif board[i][j] == '+':
                boardBoxAgent[i][j] = '@'
                boardWallDestination[i][j] = '.'

    "Bắt đầu giải thuật BFS từ đây"
    time_start = time.time()  # tính thời gian chạy, bắt đầu từ đây
    node_explored = 0  # đếm số node đã đi
    movesList = []  # list chứa các bước di chuyển
    visitedMoves = []  # list chứa các board chỉ gồm box và agent, dùng để check trùng lặp board
    # 2 board trùng nhau nếu vị trí người và các hộp là trùng nhau
    # thêm source vô queue
    queue = collections.deque([])
    # list chứa board boxAgent và movesList
    source = [boardBoxAgent, movesList]
    # kiểm tra xem board hiện tại đã có chưa, nếu chưa thì thêm vào
    if boardBoxAgent not in visitedMoves:
        visitedMoves.append(boardBoxAgent)
    queue.append(source)
    node_explored += 1
    # khởi tạo biến toạ độ x,y và biến bool completed
    agent_x = -1
    agent_y = -1
    completed = 0
    while (len(queue) != 0) and completed == 0:
        # lấy item đầu tiên ở queue
        temp = queue.popleft()
        current = temp[0]  # current chứa board Box Agent hiện tại
        movesListNow = temp[1]  # chứa list move hiện có
        # lấy toạ độ của Agent
        for i in range(0, lines):
            for j in range(0, maxHeightBoard):
                if current[i][j] == '@':
                    agent_y = j
                    agent_x = i
                    break
            else:
                continue
            break
        for move in possibleMoves:
            # kiểm tra 4 hướng của agent
            agentNew_x = agent_x + possibleMoves[move][0]
            agentNew_y = agent_y + possibleMoves[move][1]
            # tạo bản sao
            currentCopy = copy.deepcopy(current)
            movesListNowCopy = copy.deepcopy(movesListNow)
            if currentCopy[agentNew_x][agentNew_y] == '$':
                # Nếu khi di chuyển mà vị trí Agent trùng với vị trí hộp, kiểm tra phía sau hộp
                boxNew_x = agentNew_x + possibleMoves[move][0]
                boxNew_y = agentNew_y + possibleMoves[move][1]
                if currentCopy[boxNew_x][boxNew_y] == '$' or boardWallDestination[boxNew_x][boxNew_y] == '#':
                    # nếu phía sau hộp là 1 hộp khác, hoặc là 1 cái tường, thì skip hướng này
                    continue
                else:
                    # agent có thể đẩy hộp
                    currentCopy[boxNew_x][boxNew_y] = '$'
                    currentCopy[agentNew_x][agentNew_y] = '@'
                    currentCopy[agent_x][agent_y] = ' '
                    # kiểm tra xem board vừa đẩy có nằm trong visitMoves không
                    if currentCopy not in visitedMoves:
                        node_explored += 1
                        matches = 1  # biến kiểm tra tất cả các hộp có nằm trên các đích không
                        # nếu có bất kì đích nào không có hộp, matches = 0
                        for k in range(0, lines):
                            for l in range(0, maxHeightBoard):
                                if boardWallDestination[k][l] == '.':
                                    if currentCopy[k][l] != '$':
                                        matches = 0
                        # thêm move vừa đi vào cuối list
                        movesListNowCopy.append(move)
                        # nếu tất cả các hộp đã nằm trên đích
                        # kết thúc giải thuật
                        if matches == 1:
                            completed = 1
                            break
                        else:
                            # thêm vào queue và visitedMove
                            queue.append([currentCopy, movesListNowCopy])
                            visitedMoves.append(currentCopy)
            else:
                # nếu agent đi chạm phải tường, skip
                if boardWallDestination[agentNew_x][agentNew_y] == '#':
                    continue
                else:
                    # agent đi tới 1 ô trống khác
                    currentCopy[agentNew_x][agentNew_y] = '@'
                    currentCopy[agent_x][agent_y] = ' '
                    if currentCopy not in visitedMoves:
                        node_explored += 1
                        movesListNowCopy.append(move)
                        queue.append([currentCopy, movesListNowCopy])
                        visitedMoves.append(currentCopy)

    if completed == 0:
        print("UNSOLVED")

    print(movesListNowCopy)
    print("Cost: " + str(len(movesListNowCopy)))
    print("Explorer nodes: " + str(node_explored))
    time_end = time.time()
    print("Run time: " + str(time_end - time_start))
    return movesListNowCopy

#hàm đơn giản chỉ kiểm tra deadlock ở các góc
def isDeadlock(board1, board2, lines, height):
    for i in range(0, lines):
        for j in range(0, height):
            if(board1[i][j] == '$' and board2[i][j] != '.'):
                b_u_l = (board1[i-1][j] == '$' or board2[i-1][j] == '#') and (board1[i][j-1] == '$' or board2[i][j-1] == '#')
                b_u_r = (board1[i-1][j] == '$' or board2[i-1][j] == '#') and (board1[i][j+1] == '$' or board2[i][j+1] == '#')
                b_d_l = (board1[i+1][j] == '$' or board2[i+1][j] == '#') and (board1[i][j-1] == '$' or board2[i][j-1] == '#')
                b_d_r = (board1[i+1][j] == '$' or board2[i+1][j] == '#') and (board1[i][j+1] == '$' or board2[i][j+1] == '#')
                if (b_u_l or b_u_r or b_d_l or b_d_r):
                    return sys.maxsize
    return 0

def a_Star(filename):
    board = []  # board 2 chiều dùng để input map
    boardBoxAgent = []  # board 2 chiều chỉ chứa box và agent
    boardWallDestination = []  # board 2 chiều chỉ chứa tường và đích
    maxHeightBoard = 0  # height của board
    lines = 0  # width của board

    # đọc và input map từ file
    with open(filename, 'r') as f:
        for row in f.read().splitlines():
            board.append(row)
            lines += 1
            if len(row) > maxHeightBoard:
                maxHeightBoard = len(row)

    # fill 2 board trên với các kí tự "-"
    for i in range(0, lines):
        boardBoxAgent.append([])
        boardWallDestination.append([])
        for j in range(0, maxHeightBoard):
            boardBoxAgent[-1].append('-')
            boardWallDestination[-1].append('-')

    # fill height ở mỗi dòng của board cho đủ tránh bị out of range nếu ở file text thiếu kí tự khi xuống dòng
    for i in range(0, len(board)):
        if len(board[i]) < maxHeightBoard:
            for j in range(len(board[i]), maxHeightBoard):
                board[i] += ' '

    # fill 2 board cần làm việc tương ứng với từng kí tự input
    for i in range(0, len(board)):
        for j in range(0, maxHeightBoard):
            if board[i][j] == '$' or board[i][j] == '@':
                boardBoxAgent[i][j] = board[i][j]
                boardWallDestination[i][j] = ' '
            elif board[i][j] == '.' or board[i][j] == '#':
                boardWallDestination[i][j] = board[i][j]
                boardBoxAgent[i][j] = ' '
            elif board[i][j] == ' ':
                boardBoxAgent[i][j] = ' '
                boardWallDestination[i][j] = ' '
            elif board[i][j] == '*':
                boardBoxAgent[i][j] = '$'
                boardWallDestination[i][j] = '.'
            elif board[i][j] == '+':
                boardBoxAgent[i][j] = '@'
                boardWallDestination[i][j] = '.'

    # lập 1 list chứa các điểm đến phục vụ tính manhattan distance
    destinations = []
    for i in range(0, lines):
        for j in range(0, maxHeightBoard):
            if boardWallDestination[i][j] == '.':
                destinations.append([i, j])

    # heuristic
    def manhattan(state):
        distance = 0
        for i in range(0, lines):
            for j in range(0, maxHeightBoard):
                if state[i][j] == '$':
                    temp = sys.maxsize
                    for destination in destinations:
                        distanceToNearest = abs(
                            destination[0]-i) + abs(destination[1]-j)
                        if temp > distanceToNearest:
                            temp = distanceToNearest
                    distance += temp
        # return distance
        return distance

    "Bắt đầu giải thuật A* từ đây"
    time_start = time.time()  # tính thời gian chạy, bắt đầu từ đây
    movesList = []  # list chứa các bước di chuyển
    visitedMoves = []  # list chứa các board chỉ gồm box và agent, dùng để check trùng lặp board
    # 2 board trùng nhau nếu vị trí người và các hộp là trùng nhau
    node_explored = 0  # đếm node đã duyệt
    queue = PriorityQueue()
    source = [boardBoxAgent, movesList]
    # kiểm tra xem board hiện tại đã có chưa, nếu chưa thì thêm vào
    if boardBoxAgent not in visitedMoves:
        visitedMoves.append(boardBoxAgent)
    queue.put((manhattan(boardBoxAgent), source))
    node_explored += 1
    # khởi tạo biến toạ độ x,y và biến bool completed
    agent_x = -1
    agent_y = -1
    completed = 0

    while (not queue.empty()) and completed == 0:
        temp = queue.get()
        current = temp[1][0]  # current chứa board Box Agent hiện tại
        # print(current)
        movesListNow = temp[1][1]  # chứa list move hiện có
        cost = len(movesListNow)  # g(n)
        for i in range(0, lines):  # xác định toạ độ của agent
            for j in range(0, maxHeightBoard):
                if current[i][j] == '@':
                    agent_x = i
                    agent_y = j
                    break
            else:
                continue
            break
        for move in possibleMoves:
            # kiểm tra 4 hướng của agent
            agentNew_x = agent_x + possibleMoves[move][0]
            agentNew_y = agent_y + possibleMoves[move][1]
            # tạo bản sao
            currentCopy = copy.deepcopy(current)
            movesListNowCopy = copy.deepcopy(movesListNow)
            if currentCopy[agentNew_x][agentNew_y] == '$':
                # Nếu khi di chuyển mà vị trí Agent trùng với vị trí hộp, kiểm tra phía sau hộp
                boxNew_x = agentNew_x + possibleMoves[move][0]
                boxNew_y = agentNew_y + possibleMoves[move][1]
                if currentCopy[boxNew_x][boxNew_y] == '$' or boardWallDestination[boxNew_x][boxNew_y] == '#':
                    # nếu phía sau hộp là 1 hộp khác, hoặc là 1 cái tường, thì skip hướng này
                    continue
                else:
                    # agent có thể đẩy hộp
                    currentCopy[boxNew_x][boxNew_y] = '$'
                    currentCopy[agentNew_x][agentNew_y] = '@'
                    currentCopy[agent_x][agent_y] = ' '
                    # kiểm tra xem board vừa đẩy có nằm trong visitMoves không
                    if currentCopy not in visitedMoves:
                        node_explored += 1
                        matches = 1  # biến kiểm tra tất cả các hộp có nằm trên các đích không
                        # nếu có bất kì đích nào không có hộp, matches = 0
                        for k in range(0, lines):
                            for l in range(0, maxHeightBoard):
                                if boardWallDestination[k][l] == '.':
                                    if currentCopy[k][l] != '$':
                                        matches = 0
                        # thêm move vừa đi vào cuối list
                        movesListNowCopy.append(move)
                        # nếu tất cả các hộp đã nằm trên đích
                        # kết thúc giải thuật
                        if matches == 1:
                            completed = 1
                            break
                        else:
                            queue.put(
                                (manhattan(currentCopy) + cost + isDeadlock(currentCopy, boardWallDestination, lines, maxHeightBoard), [currentCopy, movesListNowCopy]))
                            visitedMoves.append(currentCopy)
            else:  # di chuyển mà không gặp hộp
                # nếu agent đi chạm phải tường, skip
                if boardWallDestination[agentNew_x][agentNew_y] == '#' or currentCopy[agentNew_x][agentNew_y] != ' ':
                    continue
                else:
                    # agent đi tới ô trống khác
                    currentCopy[agentNew_x][agentNew_y] = '@'
                    currentCopy[agent_x][agent_y] = ' '
                    if currentCopy not in visitedMoves:
                        node_explored += 1
                        movesListNowCopy.append(move)
                        queue.put((manhattan(currentCopy) + cost + isDeadlock(currentCopy, boardWallDestination, lines, maxHeightBoard),
                                  [currentCopy, movesListNowCopy]))
                        visitedMoves.append(currentCopy)

    if completed == 0:
        print("UNSOLVED")

    print(movesListNowCopy)
    print("Cost: " + str(len(movesListNowCopy)))
    print("Explorer node: " + str(node_explored))
    time_end = time.time()
    print("Run time: " + str(time_end - time_start))
    return movesListNowCopy


"Từ đây xuống dưới là code Pygame"


def askSource():
    source = ''
    GRAY = (100, 100, 100)
    screen = pygame.display.set_mode((300, 300))
    screen.fill(GRAY)
    fontobject = pygame.font.Font(None, 32)
    # Select Micro or Mini
    done = False
    while not done:
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(80, 100, 165, 30)
        button_2 = pygame.Rect(80, 200, 165, 30)
        if button_1.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                source += 'Mini Cosmos/'
                done = True
        if button_2.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                source += 'Micro Cosmos/'
                done = True

        pygame.draw.rect(screen, (80, 80, 80), button_1)
        button_1_surface = fontobject.render('Mini Cosmos', True, (0, 0, 0))
        # Blit the text.
        screen.blit(button_1_surface, (button_1.x + 5, button_1.y + 5))

        pygame.draw.rect(screen, (80, 80, 80), button_2)
        button_2_surface = fontobject.render('Micro Cosmos', True, (0, 0, 0))
        # Blit the text.
        screen.blit(button_2_surface, (button_2.x + 5, button_2.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(fontobject.render('Select option: ',
                    True, (255, 255, 255)), (30, 20))
        pygame.display.flip()
    # Select level
    screen.fill(GRAY)
    input_box = pygame.Rect(40, 100, 140, 32)
    color = pygame.Color('lightskyblue3')
    input_text = ''
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # if active:
                if event.key == pygame.K_RETURN:
                    return source + 'level' + input_text + '.txt'
                else:
                    input_text += event.unicode
        txt_surface = fontobject.render(
            'Select level: %s' % input_text, True, color)
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()
    screen.lock()

def draw(filename):

    def getPlayerPosition():
        for i in range(0, len(matrix)):
            # Iterate all columns
            for k in range(0, len(matrix[i])-1):
                if matrix[i][k] == "@" or matrix[i][k] == "+":
                    return [k, i]

    def movePlayer(move):
        x = getPlayerPosition()[0]
        y = getPlayerPosition()[1]
        global target_found
        if move == "L":
            # print ("######### Moving Left #########")
            # if is_space
            if matrix[y][x-1] == " ":
                #print ("OK Space Found")
                matrix[y][x-1] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                    target_found = False
                else:
                    matrix[y][x] = " "

            # if is_box
            elif matrix[y][x-1] == "$":
                #print ("Box Found")
                if matrix[y][x-2] == " ":
                    matrix[y][x-2] = "$"
                    matrix[y][x-1] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                        target_found = False
                    else:
                        matrix[y][x] = " "
                elif matrix[y][x-2] == ".":
                    matrix[y][x-2] = "*"
                    matrix[y][x-1] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                        target_found = False
                    else:
                        matrix[y][x] = " "

            # if is_box_on_target
            elif matrix[y][x-1] == "*":
                #print ("Box on target Found")
                if matrix[y][x-2] == " ":
                    matrix[y][x-2] = "$"
                    matrix[y][x-1] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    target_found = True

                elif matrix[y][x-2] == ".":
                    matrix[y][x-2] = "*"
                    matrix[y][x-1] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    target_found = True

            # if is_target
            elif matrix[y][x-1] == ".":
                #print ("Target Found")
                matrix[y][x-1] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                target_found = True

        elif move == "R":
            # print ("######### Moving Right #########")
            # if is_space
            if matrix[y][x+1] == " ":
                #print ("OK Space Found")
                matrix[y][x+1] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                    target_found = False
                else:
                    matrix[y][x] = " "

            # if is_box
            elif matrix[y][x+1] == "$":
                #print ("Box Found")
                if matrix[y][x+2] == " ":
                    matrix[y][x+2] = "$"
                    matrix[y][x+1] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                        target_found = False
                    else:
                        matrix[y][x] = " "

                elif matrix[y][x+2] == ".":
                    matrix[y][x+2] = "*"
                    matrix[y][x+1] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                        target_found = False
                    else:
                        matrix[y][x] = " "

            # if is_box_on_target
            elif matrix[y][x+1] == "*":
                #print ("Box on target Found")
                if matrix[y][x+2] == " ":
                    matrix[y][x+2] = "$"
                    matrix[y][x+1] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    target_found = True

                elif matrix[y][x+2] == ".":
                    matrix[y][x+2] = "*"
                    matrix[y][x+1] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    target_found = True

            # if is_target
            elif matrix[y][x+1] == ".":
                #print ("Target Found")
                matrix[y][x+1] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                target_found = True

        elif move == "D":
            # print ("######### Moving Down #########")
            # if is_space
            if matrix[y+1][x] == " ":
                #print ("OK Space Found")
                matrix[y+1][x] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                    target_found = False
                else:
                    matrix[y][x] = " "

            # if is_box
            elif matrix[y+1][x] == "$":
                #print ("Box Found")
                if matrix[y+2][x] == " ":
                    matrix[y+2][x] = "$"
                    matrix[y+1][x] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                        target_found = False
                    else:
                        matrix[y][x] = " "

                elif matrix[y+2][x] == ".":
                    matrix[y+2][x] = "*"
                    matrix[y+1][x] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                        target_found = False
                    else:
                        matrix[y][x] = " "

            # if is_box_on_target
            elif matrix[y+1][x] == "*":
                #print ("Box on target Found")
                if matrix[y+2][x] == " ":
                    matrix[y+2][x] = "$"
                    matrix[y+1][x] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    target_found = True

                elif matrix[y+2][x] == ".":
                    matrix[y+2][x] = "*"
                    matrix[y+1][x] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    target_found = True

            # if is_target
            elif matrix[y+1][x] == ".":
                #print ("Target Found")
                matrix[y+1][x] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                target_found = True

        elif move == "U":
            # print ("######### Moving Up #########")

            # if is_space
            if matrix[y-1][x] == " ":
                #print ("OK Space Found")
                matrix[y-1][x] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                    target_found = False
                else:
                    matrix[y][x] = " "

            # if is_box
            elif matrix[y-1][x] == "$":
                #print ("Box Found")
                if matrix[y-2][x] == " ":
                    matrix[y-2][x] = "$"
                    matrix[y-1][x] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                        target_found = False
                    else:
                        matrix[y][x] = " "

                elif matrix[y-2][x] == ".":
                    matrix[y-2][x] = "*"
                    matrix[y-1][x] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                        target_found = False
                    else:
                        matrix[y][x] = " "

            # if is_box_on_target
            elif matrix[y-1][x] == "*":
                #print ("Box on target Found")
                if matrix[y-2][x] == " ":
                    matrix[y-2][x] = "$"
                    matrix[y-1][x] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    target_found = True

                elif matrix[y-2][x] == ".":
                    matrix[y-2][x] = "*"
                    matrix[y-1][x] = "@"
                    if target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    target_found = True

            # if is_target
            elif matrix[y-1][x] == ".":
                #print ("Target Found")
                matrix[y-1][x] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                target_found = True

        drawLevel(matrix, screen)

    def ask(screen):
        fontobject = pygame.font.Font(None, 32)
        while True:
            mx, my = pygame.mouse.get_pos()
            button_1 = pygame.Rect(WIDTH - 150, 70, 55, 30)
            button_2 = pygame.Rect(WIDTH - 150, 130, 55, 30)
            if button_1.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0] == 1:
                    return 1
            if button_2.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0] == 1:
                    return 2
            pygame.draw.rect(screen, (80, 80, 80), button_1)
            button_1_surface = fontobject.render('BFS', True, (0, 0, 0))
            # Blit the text.
            screen.blit(button_1_surface, (button_1.x + 5, button_1.y + 5))
            pygame.draw.rect(screen, (80, 80, 80), button_2)
            button_2_surface = fontobject.render('A*', True, (0, 0, 0))
            # Blit the text.
            screen.blit(button_2_surface, (button_2.x + 5, button_2.y + 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            screen.blit(fontobject.render('Select option: ',
                        True, (255, 255, 255)), (WIDTH - 190, 20))
            pygame.display.flip()

    def drawLevel(matrix, screen):
        wall = pygame.image.load('images/wall.png')
        box = pygame.image.load('images/box.png')
        box_on_target = pygame.image.load('images/box_on_target.png')
        space = pygame.image.load('images/space.png')
        target = pygame.image.load('images/target.png')
        player = pygame.image.load('images/player.png')
        player_on_target = pygame.image.load('images/player.png')

        # Just a Dictionary (associative array in python's lingua) to map images to characters used in level design
        images = {'#': wall, ' ': space, '$': box, '.': target,
                  '@': player, '*': box_on_target, '+': player_on_target}
        x = 0
        y = 0
        for row in matrix:
            for c in row:
                screen.blit(images[c], (x * 36, y * 36))
                x += 1
            x = 0
            y += 1
        pygame.display.update()
        global clicked
        if clicked == False:
            clicked = True
            return ask(screen)

    def display_end(screen):
        check = True
        while check:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # if active:
                    if event.key == pygame.K_r:
                        check = False
                        main()
            message = "You Win"
            fontobject = pygame.font.Font(None, 32)
            pygame.draw.rect(screen, (255, 0, 0),
                             ((screen.get_width() / 2 - 20),
                             (screen.get_height() / 2),
                             90, 24))
            pygame.draw.rect(screen, GRAY,
                             ((screen.get_width() / 2 - 20),
                              (screen.get_height() / 2),
                              90, 24), 1)
            screen.blit(fontobject.render(message, True, (255, 255, 255)),
                        ((screen.get_width() / 2 - 20), (screen.get_height() / 2)))
            pygame.display.flip()

    global clicked
    clicked = False
    x = 0
    y = 0
    matrix = []
    with open(filename, 'r') as f:
        for row in f.read().splitlines():
            matrix.append(list(row))
            y += 1
            if len(row) > x:
                x = int(len(row))

    for i in range(0, len(matrix)):
        if len(matrix[i]) < x:
            for j in range(len(matrix[i]), x):
                matrix[i] += ' '

    WIDTH = x * 36 + 200
    HEIGHT = y * 36
    global target_found
    with open(filename) as f:
        if '+' in f.read():
            target_found = True
        else:
            target_found = False
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(GRAY)
    option = drawLevel(matrix, screen)
    if option == 1:
        moveList = bfs(filename)
    if option == 2:
        moveList = a_Star(filename)

    for event in moveList:
        pygame.event.pump()
        sleep(0.05)
        movePlayer(event)
    display_end(screen)


def main():
    pygame.init()
    pygame.display.set_caption("Sokoban")
    source = askSource()
    draw(source)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
