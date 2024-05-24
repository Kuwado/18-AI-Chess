import State
class Rule:
    # Vị trí mà quân tốt có thể đi
    def getPMove(self, board, row, col, move):
        state = State.State()
        # Nếu là tốt trắng
        if board[row][col][0] == 'w':
            # Nếu tốt ở hàng đầu có thể tiến 1 hoặc 2 ô
            if row == 6 and board[row-1][col] == '--':
                move.append(State.Move((row, col),(row-1, col), board))
                if board[row-2][col] == '--':
                    move.append(State.Move((row, col),(row-2, col), board))
            # Nếu tốt khác hàng đầu và hàng cuối -> tiến 1 ô
            elif row > 0 and board[row-1][col] == '--':
                move.append(State.Move((row, col), (row-1, col), board))
            # Các vị trí tốt có thể ăn
            if col - 1 >= 0:
                if board[row-1][col-1][0] == 'b':
                    move.append(State.Move((row, col), (row-1, col-1), board))     #Chéo trái
                elif (row-1, col-1) == state.enpassant:
                    print("here")
                    move.append(State.Move((row,col), (row-1, col-1), board, True))
            if col + 1 <= 7:
                if board[row-1][col+1][0] == 'b':
                    move.append(State.Move((row, col), (row-1, col+1), board))    #Chéo phải
                elif (row-1, col+1) == state.enpassant:
                    print("here")
                    move.append(State.Move((row,col), (row-1, col+1), board, True))
        # nếu là tốt đen
        else:
            # Nếu tốt ở hàng đầu có thể tiến 1 hoặc 2 ô
            if row == 1 and board[row+1][col] == '--':
                move.append(State.Move((row, col),(row+1, col), board))
                if board[row+2][col] == '--':
                    move.append(State.Move((row, col), (row+2, col), board))
            # Nếu tốt khác hàng đầu và hàng cuối -> tiến 1 ô
            elif row < 7 and board[row+1][col] == '--':
                move.append(State.Move((row, col),(row+1, col), board))
            # Các vị trí tốt có thể ăn
            if col - 1 >= 0:
                if board[row+1][col-1][0] == 'w':
                    move.append(State.Move((row, col),(row+1, col-1), board))     #Chéo trái
                elif (row + 1, col - 1) == state.enpassant:
                    print("here")
                    move.append(State.Move((row, col), (row + 1, col - 1), board, True))
            if col + 1 <= 7:
                if board[row+1][col+1][0] == 'w':
                    move.append(State.Move((row, col),(row+1, col+1), board))    #Chéo phải
                elif (row+1, col+1) == state.enpassant:
                    print("here")
                    move.append(State.Move((row,col), (row+1, col+1), board, True))

    def getRMove(self, board, row, col, moves):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))  # Các hướng di chuyển: lên, xuống, trái, phải
        for direction in directions:
            for i in range(1, 8):  # Quân xe có thể di chuyển tối đa 7 ô
                newRow = row + direction[0] * i
                newCol = col + direction[1] * i
                if 0 <= newRow < 8 and 0 <= newCol < 8:
                    if board[newRow][newCol] == "--":  # Ô trống
                        moves.append(State.Move((row, col), (newRow, newCol), board))
                    elif board[newRow][newCol][0] != board[row][col][0]:  # Quân đối phương
                        moves.append(State.Move((row, col), (newRow, newCol), board))
                        break
                    else:  # Quân cờ cùng màu
                        break
                else:  # Vượt ra khỏi biên bàn cờ
                    break

    def getNMove(self, board, row, col, moves):
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for direction in directions:
            newRow = row + direction[0]
            newCol = col + direction[1]
            if 0 <= newRow < 8 and 0 <= newCol < 8:
                if board[newRow][newCol] == "--" or board[newRow][newCol][0] != board[row][col][0]:
                    moves.append(State.Move((row, col), (newRow, newCol), board))

    def getBMove(self, board, row, col, moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Các hướng di chuyển: chéo trái trên, chéo phải trên, chéo trái dưới, chéo phải dưới
        for direction in directions:
            for i in range(1, 8):  # Quân tượng có thể di chuyển tối đa 7 ô
                newRow = row + direction[0] * i
                newCol = col + direction[1] * i
                if 0 <= newRow < 8 and 0 <= newCol < 8:
                    if board[newRow][newCol] == "--":  # Ô trống
                        moves.append(State.Move((row, col), (newRow, newCol), board))
                    elif board[newRow][newCol][0] != board[row][col][0]:  # Quân đối phương
                        moves.append(State.Move((row, col), (newRow, newCol), board))
                        break
                    else:  # Quân cờ cùng màu
                        break
                else:  # Vượt ra khỏi biên bàn cờ
                    break

    def getQMove(self, board, row, col, moves):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0),
                      (1, 1)]  # Các hướng di chuyển: 8 hướng xung quanh
        for direction in directions:
            for i in range(1, 8):  # Quân hậu có thể di chuyển tối đa 7 ô
                newRow = row + direction[0] * i
                newCol = col + direction[1] * i
                if 0 <= newRow < 8 and 0 <= newCol < 8:
                    if board[newRow][newCol] == "--":  # Ô trống
                        moves.append(State.Move((row, col), (newRow, newCol), board))
                    elif board[newRow][newCol][0] != board[row][col][0]:  # Quân đối phương
                        moves.append(State.Move((row, col), (newRow, newCol), board))
                        break
                    else:  # Quân cờ cùng màu
                        break
                else:  # Vượt ra khỏi biên bàn cờ
                    break

    def getKMove(self, board, row, col, moves):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0),
                      (1, 1)]  # Các hướng di chuyển: 8 hướng xung quanh
        for direction in directions:
            newRow = row + direction[0]
            newCol = col + direction[1]
            if 0 <= newRow < 8 and 0 <= newCol < 8:
                if board[newRow][newCol] == "--" or board[newRow][newCol][0] != board[row][col][0]:  # Ô trống hoặc chứa quân cờ đối phương
                    moves.append(State.Move((row, col), (newRow, newCol), board))
        #State.State().getCastleMoves(row, col, moves, allyColor)

