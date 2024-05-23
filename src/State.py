import rule
class State:
    def __init__(self):
        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]
        self.turn = True
        self.moveLog = []
        self.wKLocation = (7,4)
        self.bKLocation = (0,4)
        self.checkMate = False
        self.staleMate = False
        self.enpassant = ()
        self.curCastlingRights = CatsleRights(True, True, True, True)
        self.castleRightsLog = [CatsleRights(self.curCastlingRights.wks, self.curCastlingRights.bks, self.curCastlingRights.wqs, self.curCastlingRights.bqs )]
    def make_move(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.piece_move
        self.moveLog.append(move)
        self.turn = not self.turn
        #update king's location
        if move.piece_move == 'wk':
            self.wKLocation = (move.endRow, move.endCol)
        elif move.piece_move == 'bk':
            self.bKLocation = (move.endRow, move.endCol)
        #pawn promotion
        if move.pawnPromotion:
            self.board[move.endRow][move.endCol] = move.piece_move[0] + 'q'

        #en passant
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = '--' #cap

        #update enpassant var
        if move.piece_move[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassant = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassant = ()

        #castle move
        if move.isCastleMove:
            #print("here")
            if move.endCol - move.startCol ==  2: #kingside
                #print("here")
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] #moves the rock
                self.board[move.endRow][move.endCol+1] = '--'
            else: #queenside
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '--'

        #update castiling rights - not king or rook first move
        self.updateCatsleRights(move)
        self.castleRightsLog.append(CatsleRights(self.curCastlingRights.wks, self.curCastlingRights.bks, self.curCastlingRights.wqs, self.curCastlingRights.bqs ))

    def getPMove(self, row, col, move):
        # Nếu là tốt trắng
        if self.board[row][col][0] == 'w':
            # Nếu tốt ở hàng đầu có thể tiến 1 hoặc 2 ô
            if row == 6 and self.board[row-1][col] == '--':
                move.append(Move((row, col),(row-1, col), self.board))
                if self.board[row-2][col] == '--':
                    move.append(Move((row, col),(row-2, col), self.board))
            # Nếu tốt khác hàng đầu và hàng cuối -> tiến 1 ô
            elif row > 0 and self.board[row-1][col] == '--':
                move.append(Move((row, col), (row-1, col), self.board))
            # Các vị trí tốt có thể ăn
            if col - 1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    move.append(Move((row, col), (row-1, col-1), self.board))     #Chéo trái
                elif (row-1, col-1) == self.enpassant:
                    move.append(Move((row,col), (row-1, col-1), self.board, isEnPassantMove = True))
            if col + 1 <= 7:
                if self.board[row-1][col+1][0] == 'b':
                    move.append(Move((row, col), (row-1, col+1), self.board))    #Chéo phải
                elif (row-1, col+1) == self.enpassant:
                    move.append(Move((row,col), (row-1, col+1), self.board, isEnPassantMove = True))
        else:
            # Nếu tốt ở hàng đầu có thể tiến 1 hoặc 2 ô
            if row == 1 and self.board[row+1][col] == '--':
                move.append(Move((row, col),(row+1, col), self.board))
                if self.board[row+2][col] == '--':
                    move.append(Move((row, col), (row+2, col), self.board))
            # Nếu tốt khác hàng đầu và hàng cuối -> tiến 1 ô
            elif row < 7 and self.board[row+1][col] == '--':
                move.append(Move((row, col),(row+1, col), self.board))
            # Các vị trí tốt có thể ăn
            if col - 1 >= 0:
                if self.board[row+1][col-1][0] == 'w':
                    move.append(Move((row, col),(row+1, col-1), self.board))     #Chéo trái
                elif (row + 1, col - 1) == self.enpassant:
                    move.append(Move((row, col), (row + 1, col - 1), self.board, isEnPassantMove = True))
            if col + 1 <= 7:
                if self.board[row+1][col+1][0] == 'w':
                    move.append(Move((row, col),(row+1, col+1), self.board))    #Chéo phải
                elif (row+1, col+1) == self.enpassant:
                    move.append(Move((row,col), (row+1, col+1), self.board, isEnPassantMove = True))
    def remake_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.piece_move
            self.board[move.endRow][move.endCol] = move.piece_cap
            self.turn = not self.turn
            if move.piece_move == 'wk':
                self.wKLocation = (move.startRow, move.startCol)
            elif move.piece_move == 'bk':
                self.bKLocation = (move.startRow, move.startCol)
            #remake enpassant
            if move.isEnPassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.piece_cap
                self.enpassant = (move.endRow, move.endCol)
            #undo a 2 square pawn advance
            if move.piece_move[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassant = ()
            #undo catsling
            self.castleRightsLog.pop()
            castle = self.castleRightsLog[-1]
            self.curCastlingRights.wks = castle.wks
            self.curCastlingRights.bks = castle.bks
            self.curCastlingRights.wqs = castle.wqs
            self.curCastlingRights.bqs = castle.bqs
            #undo
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'
    def validMove(self):
        tempEnPassant = self.enpassant
        tempCastleRights = CatsleRights(self.curCastlingRights.wks, self.curCastlingRights.bks, self.curCastlingRights.wqs, self.curCastlingRights.bqs)
        #generate possible moves
        moves = self.possibleMove()
        if self.turn:
            self.getCastleMoves(self.wKLocation[0], self.wKLocation[1], moves)
        else:
            self.getCastleMoves(self.bKLocation[0], self.bKLocation[1], moves)
        #make the move
        for i in range(len(moves)-1, -1, -1):
            self.make_move(moves[i])
            self.turn = not self.turn
            if self.Check():
                moves.remove(moves[i])
            self.turn = not self.turn
            self.remake_move()
        if len(moves) == 0:
            if self.Check():
                self.checkMate = True
            else:
                self.staleMate = True
        self.enpassant = tempEnPassant
        self.curCastlingRights= tempCastleRights
        return moves
    #check if current player is in check
    def Check(self):
        if self.turn:
            return self.underAttack(self.wKLocation[0], self.wKLocation[1])
        else:
            return self.underAttack(self.bKLocation[0], self.bKLocation[1])
    #check if the opponent can attack (row, col)
    def underAttack(self, row, col):
        self.turn = not self.turn
        opponentMoves = self.possibleMove()
        self.turn = not self.turn
        for move in opponentMoves:
            if move.endRow == row and move.endCol == col:
                return True
        return False
    def possibleMove(self):
        r = rule.Rule()
        moves = []
        for row in range(8):
            for col in range(8):
                uTurn = self.board[row][col][0]
                if (uTurn == 'w' and self.turn) or (uTurn == 'b' and not self.turn):
                    piece = self.board[row][col][1]
                    if piece == 'p':
                        self.getPMove(row, col, moves)
                    if piece == 'r':
                        r.getRMove(self.board, row, col, moves)
                    if piece == 'n':
                        r.getNMove(self.board, row, col, moves)
                    if piece == 'b':
                        r.getBMove(self.board, row, col, moves)
                    if piece == 'q':
                        r.getQMove(self.board, row, col, moves)
                    if piece == 'k':
                        r.getKMove(self.board, row, col, moves)

        return moves
    def updateCatsleRights(self, move):
        if move.piece_move == 'wk':
            self.curCastlingRights.wks = False
            self.curCastlingRights.wqs = False
        elif move.piece_move == 'bk':
            self.curCastlingRights.bks = False
            self.curCastlingRights.bqs = False
        elif move.piece_move == 'wr':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.curCastlingRights.wqs = False
                elif move.startCol == 7:
                    self.curCastlingRights.wks = False
        elif move.piece_move == 'br':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.curCastlingRights.bqs = False
                elif move.startCol == 7:
                    self.curCastlingRights.bks = False
    def getCastleMoves(self, row, col, moves):
        if self.underAttack(row, col):
            return
        if (self.turn and self.curCastlingRights.wks) or (not self.turn and self.curCastlingRights.bks):
            self.getKingsideCastle(row, col, moves)
        if (self.turn and self.curCastlingRights.wqs) or (not self.turn and self.curCastlingRights.bqs):
            self.getQueensideCastle(row, col, moves)

    def getKingsideCastle(self, row, col, moves):
           if self.board[row][col+1] == '--' and self.board[row][col+2] == '--':
               if not self.underAttack(row, col+1) and not self.underAttack(row, col+2):
                   moves.append(Move((row, col), (row, col+2), self.board, isCastleMove = True))



    def getQueensideCastle(self, row, col, moves):
        if self.board[row][col-1] == '--' and self.board[row][col-2] == '--' and self.board[row][col-3]:
            if not self.underAttack(row, col-1) and not self.underAttack(row, col-2):
                moves.append(Move((row,col), (row, col-2), self.board, isCastleMove = True))


class CatsleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, start, end, board, isEnPassantMove = False, isCastleMove = False):
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]
        self.piece_move = board[self.startRow][self.startCol]
        self.piece_cap = board[self.endRow][self.endCol]
        self.pawnPromotion = False
        if (self.piece_move == 'wp' and self.endRow == 0) or (self.piece_move == 'bp' and self.endRow == 7):
            self.pawnPromotion = True
        self.isEnPassantMove = isEnPassantMove
        if self.isEnPassantMove:
            self.piece_cap = 'wp' if self.piece_move == 'bp' else 'bp'

        self.isCastleMove = isCastleMove


        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNote(self):
        return self.rankFile(self.startRow, self.startCol) + self.rankFile(self.endRow, self.endCol)
    def rankFile(self, row, col):
        return self.colsToFiles[col] + self.rowToRanks[row]

        
        