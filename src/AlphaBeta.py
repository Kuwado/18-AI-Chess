import math
import random

# Điểm số của từng loại quân cờ
piece_score = {"k": 0, "q": 90, "r": 50, "b": 30, "n": 30, "p": 10}

# Giá trị cho tình huống chiếu hết, hòa cờ và độ sâu của thuật toán
CHECKMATE = 1000
STALEMATE = 0

# Hàm tìm nước đi tốt nhất
<<<<<<< HEAD
def findBestMove(game_state, valid_moves, return_queue):
=======
def findBestMove(game_state, valid_moves, return_queue, depth):
>>>>>>> 628c15ebbadb21d471c9ae5d5513758518364773
    next_move = None
    random.shuffle(valid_moves)
    best_score = -CHECKMATE
    alpha = -math.inf
    beta = math.inf
    for move in valid_moves:
        game_state.makeMove(move)
        score = alphabeta(game_state, depth - 1, alpha, beta, False)
        game_state.remakeMove()
        if score > best_score:
            best_score = score
            next_move = move
        alpha = max(alpha, score)
    return_queue.put(next_move)

# Thuật toán alpha-beta
def alphabeta(game_state, depth, alpha, beta, maximizing_player):
    if depth == 0:
        return scoreBoard(game_state)

    valid_moves = game_state.validMove()

    if maximizing_player:
        max_eval = -math.inf
        for move in sorted(valid_moves, key=lambda x: moveOrdering(game_state, x), reverse=True):
            game_state.makeMove(move)
            eval_score = alphabeta(game_state, depth - 1, alpha, beta, False)
            game_state.remakeMove()
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in sorted(valid_moves, key=lambda x: moveOrdering(game_state, x)):
            game_state.makeMove(move)
            eval_score = alphabeta(game_state, depth - 1, alpha, beta, True)
            game_state.remakeMove()
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval

# Hàm đánh giá bàn cờ
def scoreBoard(game_state):
    if game_state.checkMate:
        if game_state.turn:
            return -CHECKMATE  # Black wins
        else:
            return CHECKMATE  # White wins
    elif game_state.staleMate:
        return STALEMATE

    score = 0
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = piecePositionScore(piece, row, col)
                if piece[0] == "w":
                    score += (piece_score[piece[1]] + piece_position_score)
                elif piece[0] == "b":
                    score -= (piece_score[piece[1]] + piece_position_score)
    return float(score)

# Hàm đánh giá vị trí quân cờ
def piecePositionScore(piece, row, col):
    piece_type = piece[1]
    # Bảng vị trí cho từng loại quân cờ
    PAWN_TABLE = [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5,-10,  0,  0,-10, -5,  5,
        5, 10, 10,-20,-20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0
    ]

    KNIGHTS_TABLE = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ]

    BISHOPS_TABLE = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ]

    ROOKS_TABLE = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,  0,  0,  5,  5,  0,  0,  0
    ]

    QUEENS_TABLE = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -5,  0,  5,  5,  5,  5,  0, -5,
        0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ]

    KINGS_TABLE = [
        -50,-40,-30,-20,-20,-30,-40,-50,
        -30,-20,-10,  0,  0,-10,-20,-30,
        -30,-10, 20, 30, 30, 20,-10,-30,
        -30,-10, 30, 40, 40, 30,-10,-30,
        -30,-10, 30, 40, 40, 30,-10,-30,
        -30,-10, 20, 30, 30, 20,-10,-30,
        -30,-30,  0,  0,  0,  0,-30,-30,
        -50,-30,-30,-30,-30,-30,-30,-50
    ]

    # Chọn bảng tương ứng với loại quân cờ
    if piece_type == 'p':
        return PAWN_TABLE[row * 8 + col]
    elif piece_type == 'n':
        return KNIGHTS_TABLE[row * 8 + col]
    elif piece_type == 'b':
        return BISHOPS_TABLE[row * 8 + col]
    elif piece_type == 'r':
        return ROOKS_TABLE[row * 8 + col]
    elif piece_type == 'q':
        return QUEENS_TABLE[row * 8 + col]
    elif piece_type == 'k':
        return KINGS_TABLE[row * 8 + col]
    return 0


# Hàm sắp xếp nước đi
def moveOrdering(game_state, move):
    game_state.makeMove(move)
    score = 0
    if game_state.board[move.endRow][move.endCol] != "--":
        score += piece_score[game_state.board[move.endRow][move.endCol][1]]
    game_state.remakeMove()
    return score

# Hàm tìm nước đi ngẫu nhiên
def findRandomMove(valid_moves):
    return random.choice(valid_moves)
