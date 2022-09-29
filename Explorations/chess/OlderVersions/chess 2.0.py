import pygame, sys
pygame.init()

def new_cord(piece, a, b):
    if [piece.cords[0] + a, piece.cords[1] + b] in grid:
        return [piece.cords[0] + a, piece.cords[1] + b]

def capture(piece, a , b):

    new_cord = [piece.cords[0] + a, piece.cords[1] + b]

    for p in pieces:

        if p.side == piece.side and p.cords == new_cord:
            return 0

        if p.side != piece.side and p.cords == new_cord:
            return 1

    return 2

def in_check(king):
    for p in pieces:
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

def short_castle_check():
    if not current_king.side and not check and not current_king.moved and not br2.moved:
        for p in pieces:
            if p.cords == [5,0] or p.cords == [6,0]:
                return False
        for p in [q for q in pieces if q.side != current_king.side and q.img_name != "king"]:
            for m in p.moves():
                if m == [5,0] or m == [6,0]:
                    return False
        return True

    if current_king.side and not check and not current_king.moved and not wr2.moved:
        for p in pieces:
            if p.cords == [5,7] or p.cords == [6,7]:
                return False
        for p in [q for q in pieces if q.side != current_king.side and q.img_name != "king"]:
            for m in p.moves():
                if m == [5,7] or m == [6,7]:
                    return False
        return True

def long_castle_check():
    if not current_king.side and not current_king.moved and not br2.moved:
        for p in pieces:
            if p.cords == [3,0] or p.cords == [2,0]:
                return False
        for p in [q for q in pieces if q.side != current_king.side and q.img_name != "king"]:
            for m in p.moves():
                if m == [3,0] or m == [2,0]:
                    return False
        return True

    if current_king.side and not current_king.moved and not wr2.moved:
        for p in pieces:
            if p.cords == [3,7] or p.cords == [2,7]:
                return False
        for p in [q for q in pieces if q.side != current_king.side and q.img_name != "king"]:
            for m in p.moves():
                if m == [3,7] or m == [2,7]:
                    return False
        return True

def long_castle():
    if not current_king.side:
        bk.cords = [2,0]
        bk.cords = [3,0]
    if current_king.side:
        wk.cords = [2,7]
        wr1.cords = [3,7]

def short_castle():
    if not current_king.side:
        bk.cords = [6,0]
        bk.cords = [5,0]
    if current_king.side:
        wk.cords = [6,7]
        wr1.cords = [5,7]

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
            if new_cord(self, -1, y):
                if capture(self, -1, y):
                    legal_grids.append(new_cord(self, -1, y))

            if new_cord(self, 0, y):
                if capture(self, 0, y):
                    legal_grids.append(new_cord(self, 0, y))

            if new_cord(self, 1, y):
                if capture(self, 1, y):
                    legal_grids.append(new_cord(self, 1, y))

        if new_cord(self, -1, 0):
            if capture(self, -1, 0):
                legal_grids.append(new_cord(self, -1, 0))

        if new_cord(self, 1, 0):
            if capture(self, 1, 0):
                legal_grids.append(new_cord(self, 1, 0))

        if selected_piece == self and long_castle_check():
            print("here!")
            legal_grids.append(new_cord(current_king, -2, 0))

        if selected_piece == self and short_castle_check():
            print("here!")
            legal_grids.append(new_cord(current_king, 2, 0))

        return legal_grids

class queen(piece):

    def __init__(self, side, cords):
        super().__init__(side, cords, "queen")

    def moves(self):
        legal_grids = []

        a = 1
        b = 1
        while new_cord(self, 0, -b):
            if not capture(self, 0, -b):
                break
            if capture(self, 0, -b) == 1:
                legal_grids.append(new_cord(self, 0, -b))
                break
            legal_grids.append(new_cord(self, 0, -b))
            a += 1
            b += 1

        a = 1
        b = 1
        while new_cord(self, -a, -b):
            if not capture(self, -a, -b):
                break
            if capture(self, -a, -b) == 1:
                legal_grids.append(new_cord(self, -a, -b))
                break
            legal_grids.append(new_cord(self, -a, -b))
            a += 1
            b += 1

        a = 1
        b = 1
        while new_cord(self, 0, -b):
            if not capture(self, 0, -b):
                break
            if capture(self, 0, -b) == 1:
                legal_grids.append(new_cord(self, 0, -b))
                break
            legal_grids.append(new_cord(self, 0, -b))
            a += 1
            b += 1

        a = 1
        b = 1
        while new_cord(self, a, -b):
            if not capture(self, a, -b):
                break
            if capture(self, a, -b) == 1:
                legal_grids.append(new_cord(self, a, -b))
                break
            legal_grids.append(new_cord(self, a, -b))
            a += 1
            b += 1

        a = 1
        b = 1
        while new_cord(self, -a, 0):
            if not capture(self, -a, 0):
                break
            if capture(self, -a, 0) == 1:
                legal_grids.append(new_cord(self, -a, 0))
                break
            legal_grids.append(new_cord(self, -a, 0))
            a += 1
            b += 1

        a = 1
        b = 1
        while new_cord(self, a, 0):
            if not capture(self, a, 0):
                break
            if capture(self, a, 0) == 1:
                legal_grids.append(new_cord(self, a, 0))
                break
            legal_grids.append(new_cord(self, a, 0))
            a += 1
            b += 1

        a = 1
        b = 1
        while new_cord(self, -a, b):
            if not capture(self, -a, b):
                break
            if capture(self, -a, b) == 1:
                legal_grids.append(new_cord(self, -a, b))
                break
            legal_grids.append(new_cord(self, -a, b))
            a += 1
            b += 1

        a = 1
        b = 1
        while new_cord(self, 0, b):
            if not capture(self, 0, b):
                break
            if capture(self, 0, b) == 1:
                legal_grids.append(new_cord(self, 0, b))
                break
            legal_grids.append(new_cord(self, 0, b))
            a += 1
            b += 1

        a = 1
        b = 1
        while new_cord(self, a, b):
            if not capture(self, a, b):
                break
            if capture(self, a, b) == 1:
                legal_grids.append(new_cord(self, a, b))
                break
            legal_grids.append(new_cord(self, a, b))
            a += 1
            b += 1

        return legal_grids

class rook(piece):

    def __init__(self, side, cords, moved):
        super().__init__(side, cords, "rook")

        self.moved = moved

    def moves(self):

        legal_grids = []

        a = 1
        b = 1
        while new_cord(self, -a, 0):
            if not capture(self, -a, 0):
                break
            if capture(self, -a, 0) == 1:
                legal_grids.append(new_cord(self, -a, 0))
                break
            legal_grids.append(new_cord(self, -a, 0))
            a += 1
            b += 1

        a = 1
        b = 1
        while new_cord(self, a, 0):
            if not capture(self, a, 0):
                break
            if capture(self, a, 0) == 1:
                legal_grids.append(new_cord(self, a, 0))
                break
            legal_grids.append(new_cord(self, a, 0))
            a += 1
            b += 1

        a = 1
        b = 1
        while new_cord(self, 0, b):
            if not capture(self, 0, b):
                break
            if capture(self, 0, b) == 1:
                legal_grids.append(new_cord(self, 0, b))
                break
            legal_grids.append(new_cord(self, 0, b))
            a += 1
            b += 1

        a = 1
        b = 1
        while new_cord(self, 0, -b):
            if not capture(self, 0, -b):
                break
            if capture(self, 0, -b) == 1:
                legal_grids.append(new_cord(self, 0, -b))
                break
            legal_grids.append(new_cord(self, 0, -b))
            a += 1
            b += 1

        return legal_grids

class bishop(piece):
    def __init__(self, side, cords):
        super().__init__(side, cords, "bishop")

    def moves(self):
        legal_grids = []

        a = 1
        b = 1
        while new_cord(self, -a, -b):
            if not capture(self, -a, -b):
                break
            if capture(self, -a, -b) == 1:
                legal_grids.append(new_cord(self, -a, -b))
                break
            legal_grids.append(new_cord(self, -a, -b))
            a += 1
            b += 1

        a = 1
        b = 1
        while new_cord(self, a, -b):
            if not capture(self, a, -b):
                break
            if capture(self, a, -b) == 1:
                legal_grids.append(new_cord(self, a, -b))
                break
            legal_grids.append(new_cord(self, a, -b))
            a += 1
            b += 1

        a = 1
        b = 1
        while new_cord(self, -a, b):
            if not capture(self, -a, b):
                break
            if capture(self, -a, b) == 1:
                legal_grids.append(new_cord(self, -a, b))
                break
            legal_grids.append(new_cord(self, -a, b))
            a += 1
            b += 1

        a = 1
        b = 1
        while new_cord(self, a, b):
            if not capture(self, a, b):
                break
            if capture(self, a, b) == 1:
                legal_grids.append(new_cord(self, a, b))
                break
            legal_grids.append(new_cord(self, a, b))
            a += 1
            b += 1

        return legal_grids

class pony(piece):

    def __init__(self, side, cords):
        super().__init__(side, cords, "pony")

    def moves(self):
        legal_grids = []

        for x in [-2, 2]:
            for y in [-1, 1]:
                if new_cord(self,x,y):
                    if capture(self, x, y):
                        legal_grids.append(new_cord(self,x,y))

        for x in [-1, 1]:
            for y in [-2,2]:
                if new_cord(self,x,y):
                    if capture(self, x, y):
                        legal_grids.append(new_cord(self,x,y))

        return legal_grids

class pawn(piece):
    def __init__(self, side, cords):
        super().__init__(side, cords, "pawn")

    def moves(self):
        legal_grids = []

        if self.side:
            if new_cord(self, 0, -1) and capture(self, 0, -1) == 2:
                legal_grids.append(new_cord(self, 0, -1))
                if self.cords in pawn_start and new_cord(self, 0, -2) and capture(self, 0, -2) == 2:
                    legal_grids.append(new_cord(self, 0, -2))

            if new_cord(self, -1, -1) and capture(self, -1, -1) == 1:
                legal_grids.append(new_cord(self, -1, -1))
            if new_cord(self, 1, -1) and capture(self, 1, -1) == 1:
                legal_grids.append(new_cord(self, 1, -1))


        if not self.side:
            if new_cord(self, 0, 1) and capture(self, 0, 1) == 2:
                legal_grids.append(new_cord(self, 0, 1))
                if self.cords in pawn_start and new_cord(self, 0, 2) and capture(self, 0, 2) == 2:
                    legal_grids.append(new_cord(self, 0, 2))
            if new_cord(self, -1, 1) and capture(self, -1, 1) == 1:
                legal_grids.append(new_cord(self, -1, 1))
            if new_cord(self, 1, 1) and capture(self, 1, 1) == 1:
                legal_grids.append(new_cord(self, 1, 1))
        return legal_grids

size = width, height = 900, 720
dgrey = 102, 102, 153
screen = pygame.display.set_mode(size)
board = pygame.image.load("board.png")
highlight = pygame.image.load("highlight.png")
checkimg = pygame.image.load("check.png")
boardrect = board.get_rect()
boardheight = board.get_height()
boardwidth = board.get_width()
unit_h = boardheight/8
unit_w = boardwidth/8

grid = []
for a in range(8):
    for b in range(8):
        grid.append([b,a])

bk = king(False, grid[4], False)
bq = queen(False, grid[3])

br1 = rook(False, grid[0], False)
br2 = rook(False, grid[7], False)

bb1 = bishop(False, grid[2])
bb2 = bishop(False, grid[5])

bp1 = pony(False, grid[1])
bp2 = pony(False, grid[6])

bpawn1 = pawn(False, grid[8])
bpawn2 = pawn(False, grid[9])
bpawn3 = pawn(False, grid[10])
bpawn4 = pawn(False, grid[11])
bpawn5 = pawn(False, grid[12])
bpawn6 = pawn(False, grid[13])
bpawn7 = pawn(False, grid[14])
bpawn8 = pawn(False, grid[15])

wk = king(True, grid[60], False)
wq = queen(True, grid[59])

wr1 = rook(True, grid[56], False)
wr2 = rook(True, grid[63], False)

wb1 = bishop(True, grid[58])
wb2 = bishop(True, grid[61])

wp1 = pony(True, grid[57])
wp2 = pony(True, grid[62])

wpawn1 = pawn(True, grid[48])
wpawn2 = pawn(True, grid[49])
wpawn3 = pawn(True, grid[50])
wpawn4 = pawn(True, grid[51])
wpawn5 = pawn(True, grid[52])
wpawn6 = pawn(True, grid[53])
wpawn7 = pawn(True, grid[54])
wpawn8 = pawn(True, grid[55])

turn = True
check = False
selected_piece = None
current_king = wk
legal_grids = []
check_test = True
checkmate_test = False
stalemate_test = False

pawn_start = []
for y in [1,6]:
    for x in range(8):
            pawn_start.append([x,y])

pawn_end = []
for y in [0,7]:
    for x in range(8):
            pawn_end.append([x,y])        # for promotion later on

while True:

    events = pygame.event.get()
    if check_test:
        check = in_check(current_king)
        check_test = False

    for event in events:

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            mpos = pygame.mouse.get_pos()

            if legal_grids:
                for m in legal_grids:
                    if pygame.Rect(m[0]*unit_w, m[1]*unit_h, unit_w, unit_h).collidepoint(mpos):
                        for p in pieces:
                            if p.cords == m:
                                p.cords = [-10,-10]
                                p.rect.topleft = 800,720

                        if selected_piece.img_name == "king":
                            if current_king.side and m == [6,7]: # short white
                                wr2.cords = [5,7]
                                wr2.rect.topleft = ((m[0]-1)*unit_w, m[1]*unit_h)

                            if not current_king.side and m == [6,0]: # short black
                                br2.cords = [5,0]
                                br2.rect.topleft = ((m[0]-1)*unit_w, m[1]*unit_h)

                            if current_king.side and m == [2,7]: # long white
                                wr1.cords = [3,7]
                                wr1.rect.topleft = ((m[0]+1)*unit_w, m[1]*unit_h)

                            if not current_king.side and m == [2,0]: # long black
                                br1.cords = [1,0]
                                br1.rect.topleft = ((m[0]+1)*unit_w, m[1]*unit_h)
                            current_king.moved = True

                        if selected_piece.img_name == "rook":
                            selected_piece.moved = True

                        selected_piece.cords = m
                        selected_piece.rect.topleft = (m[0]*unit_w, m[1]*unit_h)
                        selected_piece = None
                        legal_grids = []
                        turn = not turn
                        current_king = wk if turn else bk



                        check_test = True
                        checkmate_test = True
                        stalemate_test = True

                        break

            for p in pieces:
                if p.side == turn and p.rect.collidepoint(mpos):
                    if selected_piece and selected_piece == p:
                        selected_piece = None
                        break
                    selected_piece = p
                    break

            if selected_piece:
                legal_grids = legal_moves(selected_piece)

    screen.fill(dgrey)
    screen.blit(board, boardrect)

    if check:
        screen.blit(checkimg, current_king.rect)
        if checkmate_test:
            for p in [q for q in pieces if q.side == current_king.side]:
                if legal_moves(p):
                    break
                if p == [q for q in pieces if q.side == current_king.side][-1]:
                    print("Checkmate!")
        checkmate_test = False

    if stalemate_test:
        for p in [q for q in pieces if q.side == current_king.side]:
            if legal_moves(p):
                break
            if p == [q for q in pieces if q.side == current_king.side][-1]:
                print("Stalemate!")
        stalemate_test = False

    if legal_grids:
        for l in legal_grids:
            screen.blit(highlight, pygame.Rect(l[0]*unit_w, l[1]*unit_h, unit_w, unit_h))

    for p in pieces:
        screen.blit(p.img, p.rect)

    pygame.display.flip()

    # 4. En passant
    # 5. Promotions (still include rooks and bishops in-case of stalemate situations)
    # 6. only check for checkmate/stalemate once