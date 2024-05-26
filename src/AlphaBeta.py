import math
import random

# Điểm số của từng loại quân cờ
piece_score = {"k": 0, "q": 9, "r": 5, "b": 3, "n": 3, "p": 1}

# Giá trị cho tình huống chiếu hết, hòa cờ và độ sâu của thuật toán
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4

# Hàm tìm nước đi tốt nhất
def findBestMove(game_state, valid_moves, return_queue):
    next_move = None
    random.shuffle(valid_moves)
    best_score = -CHECKMATE
    alpha = -math.inf
    beta = math.inf
    for move in valid_moves:
        game_state.makeMove(move)
        score = alphabeta(game_state, DEPTH - 1, alpha, beta, False)
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
    if game_state.checkMate or game_state.staleMate:
        return scoreBoard(game_state)

    if maximizing_player:
        max_eval = -math.inf
        for move in valid_moves:
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
        for move in valid_moves:
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
                if piece[0] == "w":
                    score += piece_score[piece[1]]
                elif piece[0] == "b":
                    score -= piece_score[piece[1]]
    return float(score)
