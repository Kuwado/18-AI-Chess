class Rule:
    
    
    
    
    
    # Vị trí mà quân tốt có thể đi
    def getPMove(self, board, row, col, move):
        # Nếu là tốt trắng 
        if board[row][col][0] == 'w':
            # Nếu tốt ở hàng đầu có thể tiến 1 hoặc 2 ô
            if row == 6 and board[row-1][col] == '--':  
                move.append((row-1, col))
                if board[row-2][col] == '--':
                    move.append((row-2, col))
            # Nếu tốt khác hàng đầu và hàng cuối -> tiến 1 ô
            elif row > 0 and board[row-1][col] == '--':
                move.append((row-1, col))
            # Các vị trí tốt có thể ăn
            if row > 0 and col > 0 and board[row-1][col-1][0] == 'b':
                move.append((row-1, col-1))     #Chéo trái
            if row > 0 and col < 7 and board[row-1][col+1][0] == 'b':
                move.append((row-1, col+1))     #Chéo phải
        # nếu là tốt đen        
        else:
            # Nếu tốt ở hàng đầu có thể tiến 1 hoặc 2 ô
            if row == 1 and board[row+1][col] == '--':
                move.append((row+1, col))
                if board[row+2][col] == '--':
                    move.append((row+2, col))
            # Nếu tốt khác hàng đầu và hàng cuối -> tiến 1 ô
            elif row < 7 and board[row+1][col] == '--':
                move.append((row+1, col))
            # Các vị trí tốt có thể ăn
            if row < 7 and col > 0 and board[row+1][col-1][0] == 'w':
                move.append((row+1, col-1))     #Chéo trái
            if row < 7 and col < 7 and board[row+1][col+1][0] == 'w':
                move.append((row+1, col+1))     #Chéo phải


   # def getRMove(self, board, row, col, move):
    #    if board[row][col] 