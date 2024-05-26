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
        self.wKLocation = (7, 4)
        self.bKLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassant = ()
        self.curCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.curCastlingRights.wks, self.curCastlingRights.bks, self.curCastlingRights.wqs, self.curCastlingRights.bqs)]

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.piece_move
        self.moveLog.append(move)
        self.turn = not self.turn

        if move.piece_move == 'wk':
            self.wKLocation = (move.endRow, move.endCol)
        elif move.piece_move == 'bk':
            self.bKLocation = (move.endRow, move.endCol)

        if move.pawnPromotion:
            self.board[move.endRow][move.endCol] = move.piece_move[0] + 'q'

        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = '--'

        if move.piece_move[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassant = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassant = ()

        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.curCastlingRights.wks, self.curCastlingRights.bks, self.curCastlingRights.wqs, self.curCastlingRights.bqs))

    def remakeMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.piece_move
            self.board[move.endRow][move.endCol] = move.piece_cap
            self.turn = not self.turn

            if move.piece_move == 'wk':
                self.wKLocation = (move.startRow, move.startCol)
            elif move.piece_move == 'bk':
                self.bKLocation = (move.startRow, move.startCol)

            if move.isEnPassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.piece_cap

            if move.piece_move[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassant = ()

            self.castleRightsLog.pop()
            castle = self.castleRightsLog[-1]
            self.curCastlingRights.wks = castle.wks
            self.curCastlingRights.bks = castle.bks
            self.curCastlingRights.wqs = castle.wqs
            self.curCastlingRights.bqs = castle.bqs

            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'

    def validMove(self):
        tempEnPassant = self.enpassant
        tempCastleRights = CastleRights(self.curCastlingRights.wks, self.curCastlingRights.bks, self.curCastlingRights.wqs, self.curCastlingRights.bqs)
        moves = self.possibleMove()
        if self.turn:
            self.getCastleMoves(self.wKLocation[0], self.wKLocation[1], moves)
        else:
            self.getCastleMoves(self.bKLocation[0], self.bKLocation[1], moves)

        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.turn = not self.turn
            if self.Check():
                moves.remove(moves[i])
            self.turn = not self.turn
            self.remakeMove()

        if len(moves) == 0:
            if self.Check():
                self.checkMate = True
            else:
                self.staleMate = True

        self.enpassant = tempEnPassant
        self.curCastlingRights = tempCastleRights
        return moves

    def Check(self):
        if self.turn:
            return self.underAttack(self.wKLocation[0], self.wKLocation[1])
        else:
            return self.underAttack(self.bKLocation[0], self.bKLocation[1])

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
                        r.getPMove(self.board, row, col, moves)
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

    def updateCastleRights(self, move):
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
        if self.board[row][col + 1] == '--' and self.board[row][col + 2] == '--':
            if not self.underAttack(row, col + 1) and not self.underAttack(row, col + 2):
                moves.append(Move((row, col), (row, col + 2), self.board, isCastleMove=True))

    def getQueensideCastle(self, row, col, moves):
        if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--' and self.board[row][col - 3] == '--':
            if not self.underAttack(row, col - 1) and not self.underAttack(row, col - 2):
                moves.append(Move((row, col), (row, col - 2), self.board, isCastleMove=True))


class CastleRights():
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

    def __init__(self, start, end, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]
        self.piece_move = board[self.startRow][self.startCol]
        self.piece_cap = board[self.endRow][self.endCol]
        self.pawnPromotion = False
        if (self.piece_move == 'wp' and self.endRow == 0) or (self.piece_move == 'bp' and self.endRow == 7):
            self.pawnPromotion = True
        self.isEnPassantMove = isEnpassantMove
        if self.isEnPassantMove:
            self.piece_cap = 'wp' if self.piece_move == 'bp' else 'bp'

        self.isCastleMove = isCastleMove

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNote(self):
        return self.rankFile(self.startRow, self.startCol) + self.rankFile(self.endRow, self.endCol)

    def rankFile(self, row, col):
        return self.colsToFiles[col] + self.rowToRanks[row]
