import chess
import time
import random
from piece_square_tables import pos_value
from IPython.display import display, HTML, clear_output

t = 0
b = chess.Board()

def evaluate(board):
    score = 0
    if board.is_checkmate():
        score  = 2*int(board.turn)-1
        score *= -float("inf")
        return score
    for (piece, weight) in [
            (chess.KING,20000),
            (chess.QUEEN,1000),
            (chess.ROOK,500),
            (chess.KNIGHT,300),
            (chess.BISHOP,400),
            (chess.PAWN,100)]:
        p_w    = board.pieces(piece, chess.WHITE)
        p_b    = board.pieces(piece, chess.BLACK)
        score += weight*(len(p_w) - len(p_b))
        score += pos_value[piece][list(p_w)].sum()
        score += pos_value[-1*piece][list(p_b)].sum()
    return score

def negamax(board, depth, alpha, beta, s):
    global t
    color = 2*int(board.turn)-1
    t     = time.time()-s
    if board.is_game_over() or (depth == 0) or t>120:
        return None, color*evaluate(board)
    best_score = -float("inf")
    best_move  = None
    for move in board.legal_moves:
        board.push(move)
        _, score = negamax(board, depth-1, -beta, -alpha, s)
        score = -score
        board.pop()
        if score > best_score:
            best_score = score
            best_move  = move
        alpha = max(alpha, best_score)
        if alpha >= beta:
            break
    return best_move, best_score

def negamax_player(board):
    s        = time.time()
    move, _  = negamax(board, 4, -float("inf"), float("inf"), s)
    return move.uci()

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
    else:
        print("DRAW")

