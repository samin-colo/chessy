import chess
import time
import random
from IPython.display import display, HTML, clear_output

count = 0
b = chess.Board()

def evaluate(board):
    score = 0
    for (piece, weight) in [
            (chess.KING,20),
            (chess.QUEEN,10),
            (chess.ROOK,5),
            (chess.KNIGHT,3),
            (chess.BISHOP,3),
            (chess.PAWN,1)]:
        num_w = len(board.pieces(piece,board.turn))
        num_b = len(board.pieces(piece,not board.turn))
        score += weight*(num_w - num_b)
    return score

def minimax(board, depth, max_level, alpha, beta):
    if board.is_game_over(claim_draw=True) or (depth == 0):
        return evaluate(board)
    if max_level:
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board,depth-1, not max_level, alpha, beta)
            board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha
    else:
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth-1, not max_level, alpha, beta)
            board.pop()
            if score <= alpha:
                return alpha
            if score < beta:
                beta = score
        return beta

def negamax(board, depth, a, b, c):
    if board.is_game_over() or (depth == 0):
        return "None", c*evaluate(board)
    best_score = -float("inf")
    best_move  = None
    for move in board.legal_moves:
        global count
        count += 1
        board.push(move)
        _, score = negamax(board, depth-1, -b, -a, -c)
        score = -score
        board.pop()
        if score > best_score:
            best_score = score
            best_move  = move
        a = max(a, best_score)
        if a >= b:
            break
    return best_move, best_score

def negamax_player(board):
    color    = 1 if board.turn else -1
    move, _  = negamax(board, 4, -float("inf"), float("inf"), color)
    return move.uci()

def ab_player(board):
    depth        = 3
    choice       = None
    highest_seen = -float("inf")
    for move in board.legal_moves:
        board.push(move)
        score = minimax(board,depth, True, -float("inf"),float("inf"))
        board.pop()
        if score > highest_seen:
            highest_seen = score
            choice = move.uci()
    return choice

def human_player(board):
    prompt = "Your move [q to quit]: "
    moves  = [move.uci() for move in board.legal_moves]
    uci    = input(prompt)
    while uci not in moves:
        if(uci[0] == "q"):
            raise KeyboardInterrupt()
        uci = input(prompt)
    return uci

def random_player(board):
    return random.choice(list(board.legal_moves)).uci()

def play(p1, p2):
    result = None
    global b
    b.reset()
    display(HTML(b._repr_svg_()))
    try:
        while not b.is_game_over(claim_draw=True):
            uci = p1(b) if b.turn else p2(b)
            b.push_uci(uci)
            name = "White" if b.turn else "Black"
            html = "<b>{}'s Turn, Move {}:</b><br/>{}".format(
                    name, len(b.move_stack), b._repr_svg_())
            clear_output(wait=True)
            display(HTML(html))
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Game Interrupted!")
    if b.is_checkmate():
        print("Checkmate: {} wins!".format(
            "WHITE" if not b.turn else "BLACK"))
    elif b.is_variant_draw():
        print("DRAW")

