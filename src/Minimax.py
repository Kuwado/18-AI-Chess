import math
import random

piece_score = {"k": 0, "q": 9, "r": 5, "b": 3, "n": 3, "p": 1}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 1

def findBestMove(game_state, valid_moves, return_queue):
    next_move = None  # Khởi tạo next_move trước khi sử dụng
    random.shuffle(valid_moves)
    best_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        score = minimax(game_state, DEPTH - 1, False)
        game_state.remakeMove()
        if score > best_score:
            best_score = score
            next_move = move
    return_queue.put(next_move)


def minimax(game_state, depth, maximizing_player):
    if depth == 0 or game_state.checkMate or game_state.staleMate:
        return -scoreBoard(game_state)
    
    if maximizing_player:
        max_eval = -math.inf
        for move in game_state.validMove():
            game_state.makeMove(move)
            eval_score = minimax(game_state, depth - 1, False)
            game_state.remakeMove()
            max_eval = max(max_eval, eval_score)
        return max_eval
    else:
        min_eval = math.inf
        for move in game_state.validMove():
            game_state.makeMove(move)
            eval_score = minimax(game_state, depth - 1, True)
            game_state.remakeMove()
            min_eval = min(min_eval, eval_score)
        return min_eval


def scoreBoard(game_state):
    if game_state.checkMate:
        if game_state.turn:
            return CHECKMATE  # black wins
        else:
            return -CHECKMATE  # white wins
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


def findRandomMove(valid_moves):
    return random.choice(valid_moves)