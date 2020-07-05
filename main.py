import random
from collections import deque

class Sudoku:

    def __init__(self):
        self.board = 0
        self.value = 0
        self.column = 0
        self.row = 0

    def getInput(self):
        command = input("Enter Position, Value: ")
        print()

        if command == "solve":
            solveSudoku(self.board)
        else:
            # parses the user input into usable position and value
            self.value = int(command.split()[1])
            self.row = ord(command.split()[0][0]) - 97
            self.column = int(command.split()[0][1]) - 1

    def modifyBoard(self):
        # modifies the position to the value specified by the user
        self.board[self.row][self.column] = self.value

    def printBoard(self):

        # prints column marker
        print(" ", end=" ")
        for i in range(9):
            if i == 2 or i == 5:
                print(i + 1, end="   ")
            else:
                print(i + 1, end=" ")
        print()

        row = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        # prints board and row markers
        k = 0
        for i in self.board:

            print(row[k], end=" ")
            x = 0
            for j in i:

                # if the value is a zero, print '.' instead
                if(j == 0):
                    displayValue = '.'
                else:
                    displayValue = j

                # checks when to draw the vertical divider
                if x == 2 or x == 5:
                    print(displayValue, end=" | ")
                else:
                    print(displayValue, end=" ")
                x = x + 1

            # checks when to draw the horizontal divider
            if k == 2 or k == 5:
                print("\n  ------+-------+------")
            else:
                print()

            k = k + 1
        print()

    def checkWin(self):

        # checks rows
        for row in self.board:
            rowSum = 0
            for col in row:
                rowSum = rowSum + col
            if rowSum != 45:
                return False

        # checks columns
        for col in range(9):
            colSum = 0
            for row in range(9):
                colSum = colSum + self.board[row][col]
            if colSum != 45:
                return False

        #  checks boxes
        for startRow in range(3):
            for startCol in range(3):
                boxSum = 0
                for row in range(0, 3):
                    for col in range(0, 3):
                        boxSum = boxSum + self.board[row + startRow * 3][col + startCol * 3]
                if boxSum != 45:
                    return False

        # if it did not return false anywhere, solution is valid
        return True

    def newBoard(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        solveSudoku(self.board)

        rotateFactor = random.randint(0,8)
        sign = random.randint(0,1)

        if sign == 0:
            rotateFactor = -1 * rotateFactor

        # shift the column positions
        for i in range(9):
            self.board[i] = deque(self.board[i])
            self.board[i].rotate(rotateFactor)
            self.board[i] = list(self.board[i])

        # shift the row positions
        for i in range(9):
            self.board = deque(self.board)
            self.board.rotate(rotateFactor)
            self.board = list(self.board)

        # remove extra clues
        numCluesToRemove = random.randint(4,6)

        for i in range(9):
            for j in range(numCluesToRemove):

                randomElement = random.randint(0, 8)
                while self.board[i][randomElement] == 0:
                    randomElement = random.randint(0, 8)
                self.board[i][randomElement] = 0


# checks if num is in a given row
def inRow(board, rowNum, num):
    for i in range(9):
        if board[rowNum][i] == num:
            return True
    return False

# checks if num is in a given column
def inColumn(board, colNum, num):
    for i in range(9):
        if board[i][colNum] == num:
            return True
    return False

# checks if num is in a given 3x3 box
def inBox(board, rowNum, colNum, num):
    for i in range(3):
        for j in range(3):
            if board[i + rowNum][j + colNum] == num:
                return True
    return False

# checks the legality of a given location (rowNum, colNum) for num
def legalLocation(board, rowNum, colNum, num):
    return not inRow(board, rowNum, num) and not inColumn(board, colNum, num) and not inBox(board, rowNum - rowNum % 3, colNum - colNum % 3, num)

# finds an empty location on the board
def findEmptyLocation(board, emptyLocation):
    for row in range(9):
        for col in range(9):
            if(board[row][col] == 0):
                emptyLocation[0] = row
                emptyLocation[1] = col
                return True
    return False

# uses the backtracking algorithm to solve the sudoku puzzle
def solveSudoku(board):

    # find an empty location on the board
    emptyLocation = [0,0]
    if not findEmptyLocation(board, emptyLocation):
        return True

    rowNum = emptyLocation[0]
    colNum = emptyLocation[1]

    # goes through numbers 1 - 9
    for num in range(1,10):
        # checks if there is a legal location for num at the empty location
        if(legalLocation(board, rowNum, colNum, num)):

            # if there is a legal location, assume it is correct and re-assign the position
            board[rowNum][colNum] = num

            # if the board is solved, return true
            if solveSudoku(board):
                return True

            # if returned here, that means the assumption was incorrect, tries another number
            board[rowNum][colNum] = 0

    return False




def main():



    game = Sudoku()
    game.newBoard()
    gameOver = False

    while not gameOver:
        game.printBoard()
        game.getInput()
        game.modifyBoard()
        gameOver = game.checkWin()

    if gameOver:
        print("Correct Solution!\n")
        game.printBoard()

if __name__ == "__main__":
    main()