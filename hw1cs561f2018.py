from collections import Counter
import numpy as np
import time
import sys



with open("input47.txt","r") as inpfile:
    content =  inpfile.readlines()
outfile = open("output.txt","w")

inputs = [x.strip() for x in content]
N = int(inputs[0])
police = int(inputs[1])
scooters = int(inputs[2])

points = [[0 for col in range(N)] for row in range(N)]

del inputs[0:3]


inp = []
for i in inputs:
    list = map(int, i.split(","))
    inp.append(tuple(list))

c = Counter(inp)

for i in range(N):
    for j in range(N):
        thiscoord = (i,j)

        if thiscoord in c.keys():
            points[i][j] = c[thiscoord]

list = []
for i in range(N):
    templist = []
    for j in range(N):
        templist.append(points[j][i])
    list.append(max(templist))


a = np.asarray(points)
a = a.argsort(axis=0).argsort(axis=0) + 1

a =  np.transpose(a)
a = np.array(a).tolist()

access = []
for i in range(len(a)):
    mydict = {}
    for j in range(len(a)):
        mydict[a[i][j]] = j
    access.append(mydict)


def check_coord_safe(coord, placed_police_coords):
    if len(placed_police_coords) == 0:
        return True

    row = coord[0]
    col = coord[1]
    for coords in placed_police_coords:
        if row == coords[0] or col == coords[1] or row - col == coords[0] - coords[1] or row + col == coords[0] + coords[1]:
            return False

    return True



number_of_solutions = 0
MAX = 0
timeout = 175
timeout_start = time.time()

def solveNQueens(board, column, countqueens, tot,N, points, placed_police_coords, min_police, list,access):
    global number_of_solutions
    global MAX
    global timeout
    global timeout_start

    if time.time() > timeout_start + timeout:
        string = "\n"
        outfile.write(str(MAX) + string)
        outfile.close()
        sys.exit()

    if tot + sum(list[column:]) < MAX:
        return

    if countqueens == min_police:
        number_of_solutions += 1
        if (tot > MAX):
            MAX = tot
            print MAX
        return

    if column == N:
        return

    for i in range(N,0,-1):

        if  check_coord_safe((access[column][i], column),placed_police_coords):
            board[access[column][i]][column] = 1
            placed_police_coords.append((access[column][i],column))
            countqueens = countqueens + 1
            tot = tot + points[access[column][i]][column]
            solveNQueens(board, column + 1, countqueens, tot, N, points,placed_police_coords, min_police,list,access)
            countqueens = countqueens - 1
            board[access[column][i]][column] = 0
            placed_police_coords.remove((access[column][i],column))
            tot = tot - points[access[column][i]][column]

    if min_police - countqueens <= N - column:
        solveNQueens(board, column + 1, countqueens, tot, N, points,placed_police_coords, min_police, list,access)


board = [[0 for x in range(N)] for y in range(N)]
placed_police_coords = []
solveNQueens(board, 0, 0, 0, N, points, placed_police_coords, police, list, access)
string = "\n"
outfile.write(str(MAX) + string)
outfile.close()

