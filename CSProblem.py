# SUDOKU
import math
import copy
#3/'קראדטגוןעליחעגכגדכסצחימעארקכ'דיחתליחעא
# import CSPSolver
# board - The variables' value are in a list of the (N*N)*(N*N) board cells
#            (a vector represenring a mat.).
# an empty cell contains 0.
#
# d - The domains are a list of lists - the domain of every var.
#
# The state is a list of 2 lists: the vars. and the domains.
N = 0
def create(fpath="sudoku.txt"):
    global N
    board = read_board_from_file(fpath)
    N = int(len(board) ** 0.25)
    # creating the domains for each place on the sudoku board
    p=[board,[]]
    for i in range(len(board)):
        if(board[i]!=0): #if there is a number there is not domain
            dom=[]
        else:
            dom=[1,2,3,4,5,6,7,8,9] #define the domain for every index
        p[1].append(copy.deepcopy(dom))
    # p is a list with 2 elements: The board and the list of domains
    BOARD = 0
    POSSIBILITIES = 1
    # going through each of the N^4 places on the sudoku board
    for i in range(N ** 4):
        if p[BOARD][
            i] != 0:  # if the place already has a number in it (not 0) then it's domain should have only that number in it
            p[POSSIBILITIES][i] = []
        else:  # if the place is blank (has a 0 in it)
            row = i // (N ** 2)  # finding which row this place is in (from 0 to N^2-1)
            column = i % (N ** 2)  # finding which column this place is in (from 0 to N^2-1)
            square = column // N + N * (
                        row // N)  # finding which N X N square this place is in (from 0 to N^2, counting starting from upper left corner to bottom right corner)
            square_starting_column = (square % N) * N  # finding the left most column of the square
            square_starting_row = (square // N) * N  # finding the upper row of the square
            # going through every place in the row of the current place, and removing from the domain of the current place any number that's already in one of the places in it's row
            for j in range(row * N ** 2, (row + 1) * N ** 2):
                if board[j] in p[1][i]:
                    p[1][i].remove(board[j])
                # going through every place in the column of the current place, and removing from the domain of the current place any number that's already in one of the places in it's column
            for j in range(column, N ** 4, N ** 2):
                if board[j] in p[1][i]:
                    p[1][i].remove(board[j])
                # going through every place in the N X N square that the current place is in, and removing from the domain of the current place any number that's already in one of the places in it's N X N square
            for j in range(square_starting_row, square_starting_row + N):
                for k in range(square_starting_column, square_starting_column + 3):
                    if board[square_starting_row * N ** 2 + square_starting_column] != 0 and board[square_starting_row * N ** 2 + square_starting_column] in p[1][i]:
                        p[1][i].remove(board[square_starting_row * N ** 2 + square_starting_column])

    return p


def read_board_from_file(fpath):
    f = open(fpath, "r")
    board = []
    s = f.readline()
    while s != "":
        for i in s.split():
            board += [int(i)]
        s = f.readline()
    f.close()
    return board


def domain(problem, v):
    # Returns the domain of v
    return problem[1][v][:]


def domain_size(problem, v):
    # Returns the domain size of v
    return len(problem[1][v])


def assign_val(problem, v, x):
    # Assigns x in var. v
    problem[0][v] = x


def get_val(problem, v):
    # Returns the val. of v
    return problem[0][v]


def erase_from_domain(problem, v, x):
    # Erases x from the domain of v
    problem[1][v].remove(x)


def get_list_of_free_vars(problem):
    # Returns a list of vars. that were not assigned a val.
    l = []
    for i in range(len(problem[0])):
        if problem[0][i] == 0:
            l += [i]
    return l


def is_solved(problem):
    # Returns True iff the problem is solved
    for i in range(len(problem[0])):
        if problem[0][i] == 0:
            return False
    return True

def is_consistent(problem, v1, v2, x1, x2):
    # Returns True iff v1=x1 and v2=x2 is consistent with all constraints
    # your code here
    # if x1 does not equal x2 then it for sure is consistant so return true
    if x1 not in problem[1][v1]:
        return False
    if x2 not in problem[1][v2]:
        return False
    if x1 != x2:
        return True
    v1_row = v1 // (N ** 2)  # the row that v1 is in
    v2_row = v2 // (N ** 2)  # the row that v2 is in
    v1_column = v1 % (N ** 2)  # the column that v1 is in
    v2_column = v2 % (N ** 2)  # the column that v2 is in
    v1_square = v1_column // N + N * (v1_row // N)  # the NxN square that v1 is in
    v2_square = v2_column // N + N * (v2_row // N)  # the NxN square that v2 is in
    # if x1=x2 and v1 and v2 are in the same row or same column or same NxN square return false
    if v1_row == v2_row or v1_column == v2_column or v1_square == v2_square:
        return False
    # otherwise return true
    else:
        return True


def list_of_influenced_vars(problem, v):
    # Returns a list of free vars. whose domain will be
    # influenced by assigning a val. to v
    r = list(range(N ** 4))
    r.remove(v)
    l = []
    for i in r:
        if problem[0][i] == 0 and not is_consistent(problem, v, i, 1, 1):
            l += [i]
    return l


def present(problem):
    for i in range(len(problem[0])):
        if i % (N * N) == 0:
            print()
        x = str(problem[0][i])
        pad = (math.ceil(math.log(N * N, 10)) - len(x))
        print(pad * " ", x, end="")
    print()

def sqr(b,n):
    v1_row = n // (N ** 2)  # the row that v1 is in
    v1_column = n % (N ** 2)  # the column that v1 is in
    v2_square = v1_column // N + N * (v1_row // N)  # the NxN square that v2 is in
    return v2_square
def sqr1(b,n):
    row = n // (N ** 2)
    column = n % (N ** 2)
    square = column // N + N * ( row // N)
    square_starting_column = (square % N) * N  # finding the left most column of the square
    square_starting_row = (square // N) * N  # finding the upper row of the square
    return(square,square_starting_column,square_starting_row)
    return()
p=create()
for i in range(81):
    print(sqr1(p[0],i),end='')

