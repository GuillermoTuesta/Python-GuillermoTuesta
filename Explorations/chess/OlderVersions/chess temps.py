def legal_moves(piece):
    legal_moves = []
    current_cords = piece.cords
    attacking_piece = None
    for m in piece.moves():
        piece.cords = m
        if attacking_piece:
            attacking_piece.cords = old_cords
        for p in pieces:
            if p != piece and p.cords == m:
                attacking_piece = p
                old_cords = attacking_piece.cords
                attacking_piece.cords = [-10,-10]
        if in_check(current_king):
            continue
        legal_moves.append(m)
    if attacking_piece:
        attacking_piece.cords = old_cords
    piece.cords = current_cords
    return legal_moves

def legal_moves(piece):
    legal_moves = []
    current_cords = piece.cords
    for m in piece.moves():
        piece.cords = m
        if in_check(current_king):
            continue
        legal_moves.append(m)
    piece.cords = current_cords
    return legal_moves