import sys, pygame
pygame.init()

class grid:
    def __init__(self, y, x, name, piece):
        self.x = x
        self.y = y
        self.xy = (x,y)
        self.name = name
        self.piece = piece
        rect = pygame.Rect(x, y, 90, 90)
        self.rect = rect


pieces = []
class piece:
        def __init__(self, side, x , y , n):
            if side == 0: s = "b"
            else:         s = "w"
            name = f"{s}{n}"
            img = pygame.image.load(f"{name}.png")
            rect = img.get_rect()
            rect.topleft = (x,y)

            self.img = img
            self.side = side
            self.name = name
            self.rect = rect
            pieces.append(self)


size = width,height = 900,720
dgrey = 102, 102, 153
screen = pygame.display.set_mode(size)
board = pygame.image.load("board.png")
boardrect = board.get_rect()
boardheight = board.get_height()
boardwidth = board.get_width()

grids = []
n = 0
for a in range(8):
    for b in range(8):
        x = a * (boardheight/8)
        y = b * (boardwidth/8)
        grids.append(grid(x, y, f"grid{n}", None))
        n += 1

bk = piece(0, grids[4].x, grids[4].y, "king")
bq = piece(0, grids[3].x, grids[3].y, "queen")

br1 = piece(0, grids[0].x, grids[0].y, "rook")
br2 = piece(0, grids[7].x, grids[7].y, "rook")

bb1 = piece(0, grids[2].x, grids[2].y, "bishop")
bb2 = piece(0, grids[5].x, grids[5].y, "bishop")

bp1 = piece(0, grids[1].x, grids[1].y, "pony")
bp2 = piece(0, grids[6].x, grids[6].y, "pony")

bpawn1 = piece(0, grids[8].x, grids[8].y, "pawn")
bpawn2 = piece(0, grids[9].x, grids[9].y, "pawn")
bpawn3 = piece(0, grids[10].x, grids[10].y, "pawn")
bpawn4 = piece(0, grids[11].x, grids[11].y, "pawn")
bpawn5 = piece(0, grids[12].x, grids[12].y, "pawn")
bpawn6 = piece(0, grids[13].x, grids[13].y, "pawn")
bpawn7 = piece(0, grids[14].x, grids[14].y, "pawn")
bpawn8 = piece(0, grids[15].x, grids[15].y, "pawn")

wk = piece(1, grids[60].x, grids[60].y, "king")
wq = piece(1, grids[59].x, grids[59].y, "queen")

wr1 = piece(1, grids[56].x, grids[56].y, "rook")
wr2 = piece(1, grids[63].x, grids[63].y, "rook")

wb1 = piece(1, grids[58].x, grids[58].y, "bishop")
wb2 = piece(1, grids[61].x, grids[61].y, "bishop")

wp1 = piece(1, grids[57].x, grids[57].y, "pony")
wp2 = piece(1, grids[62].x, grids[62].y, "pony")

wpawn1 = piece(1, grids[48].x, grids[48].y, "pawn")
wpawn2 = piece(1, grids[49].x, grids[49].y, "pawn")
wpawn3 = piece(1, grids[50].x, grids[50].y, "pawn")
wpawn4 = piece(1, grids[51].x, grids[51].y, "pawn")
wpawn5 = piece(1, grids[52].x, grids[52].y, "pawn")
wpawn6 = piece(1, grids[53].x, grids[53].y, "pawn")
wpawn7 = piece(1, grids[54].x, grids[54].y, "pawn")
wpawn8 = piece(1, grids[55].x, grids[55].y, "pawn")


drag = False
dragged = None
piecerects = [p.rect for p in pieces]

while True:
    events = pygame.event.get()
    mpos = pygame.mouse.get_pos()


    if not dragged:
        for g in grids:
            for p in piecerects:
                if g.rect.topleft == p.topleft:
                    p_ind = (g.rect).collidelist(piecerects)
                    g.piece = pieces[p_ind]
                    break
                else:
                    g.piece = None

    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            for g in grids:
                if g.rect.collidepoint(mpos):
                    selected_grid = g
                    break

            for p in pieces:
                if p.rect.collidepoint(mpos):
                    drag = not drag
                    if not dragged:
                        dragged = p
                    dragged.rect.topleft = mpos
                    break

            if not drag and dragged:
                if selected_grid.piece:
                    if dragged.side != selected_grid.piece.side:
                        selected_grid.piece.rect.topleft = 800, 600
                        dragged.rect.topleft = selected_grid.xy
                        dragged = None
                if not selected_grid.piece or selected_grid.piece == dragged:
                    dragged.rect.topleft = selected_grid.xy
                    dragged = None

        elif event.type == pygame.MOUSEMOTION:
            if drag and dragged:
                dragged.rect.topleft = mpos

    screen.fill(dgrey)
    screen.blit(board, boardrect)

    for p in pieces:
        screen.blit(p.img, p.rect)

    pygame.display.flip()