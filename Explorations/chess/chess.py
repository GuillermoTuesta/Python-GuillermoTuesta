import pygame
import sys
pygame.init()

def nc(piece, a, b):
    return [piece.cords[0] + a, piece.cords[1] + b]

def ncc(piece, a , b):
    new_cord = [piece.cords[0] + a, piece.cords[1] + b]

    if new_cord not in grid:
        return None

    for p in pieces:
        if p.side == piece.side and p.cords == new_cord:
            return 0

        if p.side != piece.side and p.cords == new_cord:
            return 1

    return 2

def in_check(king):
    for p in [q for q in pieces if q.side != king.side]:
        if p != king:
            for m in p.moves():
                if m == king.cords:
                    return True
    return False

def legal_moves(piece):
    legal_moves = []
    current_cords = piece.cords
    attacking_piece = None
    for m in piece.moves():
        piece.cords = m
        if attacking_piece:
            attacking_piece.cords = old_cords
            attacking_piece = None
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

def short_castle_check(c_king):
    for r in short_rooks:
        if r.side == c_king.side:
            own_rook = r

    if not check and not c_king.moved and not own_rook.moved:
        for p in pieces:
            if p.cords == nc(c_king, 1, 0) or p.cords == nc(c_king, 2, 0):
                return False
        for p in [q for q in pieces if q.side != c_king.side and q.img_name != "king"]:
            for m in p.moves():
                if m == nc(c_king, 1, 0) or m == nc(c_king, 2, 0):
                    return False
        return True

def long_castle_check(c_king):
    for r in long_rooks:
        if r.side == c_king.side:
            own_rook = r

    if not check and not c_king.moved and not own_rook.moved:
        for p in pieces:
            if p.cords == nc(c_king, -1, 0) or p.cords == nc(c_king, -2, 0) or p.cords == nc(c_king, -3, 0):
                return False
        for p in [q for q in pieces if q.side != c_king.side and q.img_name != "king"]:
            for m in p.moves():
                if m == nc(c_king, -1, 0) or m == nc(c_king, -2, 0):
                    return False
        return True

def long_castle(c_king):
    if not c_king.side:
        long_black_rook.cords = [c_king.cords[0]-1, c_king.cords[1]]
        long_black_rook.rect.topleft = (long_black_rook.cords[0]*unit_w, long_black_rook.cords[1]*unit_h)
    if c_king.side:
        long_white_rook.cords = [c_king.cords[0]-1, c_king.cords[1]]
        long_white_rook.rect.topleft = (long_white_rook.cords[0]*unit_w, long_white_rook.cords[1]*unit_h)

def short_castle(c_king):
    if not c_king.side:
        short_black_rook.cords = [c_king.cords[0]+1, c_king.cords[1]]
        short_black_rook.rect.topleft = (short_black_rook.cords[0]*unit_w, short_black_rook.cords[1]*unit_h)
    if c_king.side:
        short_white_rook.cords = [c_king.cords[0]+1, c_king.cords[1]]
        short_white_rook.rect.topleft = (short_white_rook.cords[0]*unit_w, short_white_rook.cords[1]*unit_h)

def en_croissant_check(pawn):
    k = -1 if pawn.side else 1

    if selected_piece.img_name == "pawn" and previous_piece.img_name == "pawn" and previous_piece.side != selected_piece.side:
        if previous_cords not in pawn_start:
            return None
        pawn_cords = previous_piece.cords
        previous_piece.cords = nc(previous_piece, 0, k)
        if ncc(selected_piece, -1, k) == 1:
            previous_piece.cords = pawn_cords
            return nc(selected_piece, -1, k)
        if ncc(selected_piece, 1, k) == 1:
            previous_piece.cords = pawn_cords
            return nc(selected_piece, 1, k)
    previous_piece.cords = pawn_cords
    return None

def straight_move(piece, direction):
    legal_grids = []
    x = 0
    y = 0

    if direction == "down":
        increment = [0,1]
    elif direction == "up":
        increment = [0,-1]
    elif direction == "right":
        increment = [1,0]
    elif direction == "left":
        increment = [-1,0]
    elif direction == "upleft":
        increment = [-1,-1]
    elif direction == "upright":
        increment = [1, -1]
    elif direction == "downleft":
        increment = [-1, 1]
    elif direction == "downright":
        increment = [1,1]

    x += increment[0]
    y += increment[1]

    while ncc(piece, x, y):
        if ncc(piece, x, y) == 1:
            legal_grids.append(nc(piece, x, y))
            break
        legal_grids.append(nc(piece, x, y))
        x += increment[0]
        y += increment[1]

    return legal_grids

def display():
    screen.fill(dgrey)
    screen.blit(board, boardrect)

    if check:
        screen.blit(checkimg, current_king.rect)

    if legal_grids:
        for l in legal_grids:
            screen.blit(highlight, pygame.Rect(l[0]*unit_w, l[1]*unit_h, unit_w, unit_h))

    for p in pieces:
        screen.blit(p.img, p.rect)

    pygame.display.flip()

def remove_piece(p):
    p.cords = the_void
    p.rect.topleft = (800, 720)
    pieces.remove(p)

pieces = []
class piece:
    def __init__(self, side, cords, img_name):

        if not side:
            s = "b"
        elif side:
            s = "w"

        self.img_name = img_name
        self.cords = cords
        self.side = side
        self.img = pygame.image.load(s + img_name + ".png")
        self.rect = pygame.Rect(cords[0]*unit_w, cords[1]*unit_h, unit_w, unit_h)
        pieces.append(self)

class king(piece):
    def __init__(self, side, cords, moved):
        super().__init__(side, cords, "king")

        self.moved = moved

    def moves(self):
        legal_grids = []

        for y in [-1, 1]:
            if ncc(self, -1, y):
                    legal_grids.append(nc(self, -1, y))

            if ncc(self, 0, y):
                legal_grids.append(nc(self, 0, y))

            if ncc(self, 1, y):
                    legal_grids.append(nc(self, 1, y))

        if ncc(self, -1, 0):
                legal_grids.append(nc(self, -1, 0))

        if ncc(self, 1, 0):
                legal_grids.append(nc(self, 1, 0))

        if selected_piece == self and short_castle_check(self):
            legal_grids.append(nc(current_king, 2, 0))

        if selected_piece == self and long_castle_check(self):
            legal_grids.append(nc(current_king, -2, 0))

        return legal_grids

class queen(piece):
    def __init__(self, side, cords):
        super().__init__(side, cords, "queen")

    def moves(self):
        legal_grids = []
        for i in range(8):
            if straight_move(self,directions[i]):
                for g in straight_move(self,directions[i]):
                    legal_grids.append(g)

        return legal_grids

class rook(piece):
    def __init__(self, side, cords, moved):
        super().__init__(side, cords, "rook")
        self.moved = moved

    def moves(self):
        legal_grids = []

        for i in range(4):
            if straight_move(self, directions[i]):
                for g in straight_move(self, directions[i]):
                    legal_grids.append(g)

        return legal_grids

class bishop(piece):
    def __init__(self, side, cords):
        super().__init__(side, cords, "bishop")

    def moves(self):
        legal_grids = []

        for i in range(4, 8):
            if straight_move(self, directions[i]):
                for g in straight_move(self, directions[i]):
                    legal_grids.append(g)

        return legal_grids

class pony(piece):
    def __init__(self, side, cords):
        super().__init__(side, cords, "pony")

    def moves(self):
        legal_grids = []

        for x in [-2, 2]:
            for y in [-1, 1]:
                if ncc(self, x, y):
                    legal_grids.append(nc(self, x, y))

        for x in [-1, 1]:
            for y in [-2,2]:
                if ncc(self, x, y):
                    legal_grids.append(nc(self, x, y))

        return legal_grids

class pawn(piece):
    def __init__(self, side, cords):
        super().__init__(side, cords, "pawn")

    def moves(self):
        legal_grids = []

        k = -1 if self.side else 1

        if previous_piece and selected_piece:
            if selected_piece.img_name == "pawn" and previous_piece.img_name == "pawn" and en_croissant_check(self):
                legal_grids.append(en_croissant_check(self))

        if ncc(self, 0, k) == 2:
            legal_grids.append(nc(self, 0, k))
            if self.cords in pawn_start and ncc(self, 0, k*2) == 2:
                legal_grids.append(nc(self, 0, k*2))

        if self.side:
            if ncc(self, -1, -1) == 1:
                legal_grids.append(nc(self, -1, -1))
            if ncc(self, 1, -1) == 1:
                legal_grids.append(nc(self, 1, -1))
        if not self.side:
            if ncc(self, -1, 1) == 1:

                legal_grids.append(nc(self, -1, 1))
            if ncc(self, 1, 1) == 1:
                legal_grids.append(nc(self, 1, 1))

        return legal_grids

size = width, height = 900, 720
dgrey = 102, 102, 153
screen = pygame.display.set_mode(size)
board = pygame.image.load("board.png")
highlight = pygame.image.load("highlight.png")
checkimg = pygame.image.load("check.png")
boardrect = board.get_rect()
unit_h = board.get_height()/8
unit_w = board.get_width()/8

grid = []
for a in range(8):
    for b in range(8):
        grid.append([b,a])

bk = king(False, grid[4], False)
bq = queen(False, grid[3])
long_black_rook = rook(False, grid[0], False)
short_black_rook = rook(False, grid[7], False)
bb1 = bishop(False, grid[2])
bb2 = bishop(False, grid[5])
bp1 = pony(False, grid[1])
bp2 = pony(False, grid[6])

for k in range(8):
    pieces.append(pawn(False, grid[8+k]))

wk = king(True, grid[60], False)
wq = queen(True, grid[59])
long_white_rook = rook(True, grid[56], False)
short_white_rook = rook(True, grid[63], False)
wb1 = bishop(True, grid[58])
wb2 = bishop(True, grid[61])
wp1 = pony(True, grid[57])
wp2 = pony(True, grid[62])

for k in range(8):
    pieces.append(pawn(True, grid[48+k]))

directions = ["down","up","right","left","upleft","upright","downleft","downright"]
turn = True
selected_piece = None
current_king = wk
legal_grids = []
check = False
check_test = False
GameWinTest = False
previous_piece = None
p_check = False
short_rooks = [short_black_rook, short_white_rook]
long_rooks = [long_black_rook, long_white_rook]
the_void = [-10,-10]

pawn_start = []
for y in [1,6]:
    for x in range(8):
        pawn_start.append([x,y])

pawn_end = []
for y in [0,7]:
    for x in range(8):
        pawn_end.append([x,y])

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            mpos = pygame.mouse.get_pos()

            if legal_grids:
                for m in legal_grids:
                    if pygame.Rect(m[0]*unit_w, m[1]*unit_h, unit_w, unit_h).collidepoint(mpos):

                        for p in pieces:
                            if p.cords == m:
                                remove_piece(p)

                        if previous_piece and selected_piece:
                            if selected_piece.img_name == "pawn" and previous_piece.img_name == "pawn" and en_croissant_check(selected_piece):
                                if m == en_croissant_check(selected_piece):
                                    remove_piece(previous_piece)

                        if selected_piece and selected_piece.img_name == "king":
                            if m == nc(current_king, 2, 0):
                                short_castle(current_king)
                            if m == nc(current_king, -2, 0):
                                long_castle(current_king)
                            current_king.moved = True

                        if selected_piece and selected_piece.img_name == "rook":
                            selected_piece.moved = True

                        if selected_piece and selected_piece.img_name == "pawn" and m in pawn_end:
                            c_side = selected_piece.side
                            promotion_pieces = []
                            promotion_pieces.append(queen(selected_piece.side, m))
                            promotion_pieces.append(rook(selected_piece.side, m, True))
                            promotion_pieces.append(bishop(selected_piece.side, m))
                            promotion_pieces.append(pony(selected_piece.side, m))

                            for p in promotion_pieces:
                                p.rect.topleft = (unit_w * 8, unit_h * (promotion_pieces.index(p)+3))

                            promotion = True
                            p_check = True
                            while promotion:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        sys.exit()
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mpos = pygame.mouse.get_pos()
                                        for p in promotion_pieces:
                                            if p.rect.collidepoint(mpos):

                                                remove_piece(selected_piece)

                                                if p.img_name == "queen":
                                                    new_piece = queen(c_side, m)
                                                elif p.img_name == "rook":
                                                    new_piece = rook(c_side, m, True)
                                                elif p.img_name == "bishop":
                                                    new_piece = bishop(c_side, m)
                                                elif p.img_name == "pony":
                                                   new_piece = pony(c_side, m)

                                                new_piece.rect.topleft = (m[0] * unit_w, m[1] * unit_h)
                                                pieces = [x for x in pieces if x not in promotion_pieces]
                                                promotion = False
                                display()

                        previous_piece = selected_piece
                        previous_cords = selected_piece.cords
                        if not p_check:
                            selected_piece.cords = m
                            selected_piece.rect.topleft = (m[0]*unit_w, m[1]*unit_h)
                        selected_piece = None
                        legal_grids = []
                        turn = not turn
                        current_king = wk if turn else bk
                        check_test = True
                        GameWinTest = True
                        p_check = False
                        break

            for p in pieces:
                if p.side == turn and p.rect.collidepoint(mpos):
                    if selected_piece and selected_piece == p:
                        selected_piece = None
                        legal_grids = []
                        break
                    selected_piece = p
                    break

            if selected_piece:
                legal_grids = legal_moves(selected_piece)

    if check_test:
        check = in_check(current_king)
        check_test = False

    if GameWinTest:
        for p in [q for q in pieces if q.side == current_king.side]:
            if legal_moves(p):
                break
            if p == [q for q in pieces if q.side == current_king.side][-1]:
                if not check:
                    print("Stalemate!")
                if check:
                    print("Checkmate!")
        GameWinTest = False

    display()
    # 1. Threefold repetition and 50-move draw (who cares)
    # 2. Sounds
    # 3. undo moves
