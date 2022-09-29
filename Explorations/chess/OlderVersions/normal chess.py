import pygame, sys
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

            self.n = n
            self.img = img
            self.side = side
            self.name = name
            self.rect = rect
            pieces.append(self)

leftside = list(range(0,64,8))
rightside = list(range(7,64,8))

def move(s_grid):
    global selected
    index = grids.index(s_grid)
    selected = s_grid.piece
    name = selected.n
    move_grids = []

    if name == "king":

        if 0 <= (index - 9) <= 63 and (index - 9) not in rightside and (not grids[index - 9].piece or grids[index - 9].piece.side != selected.side):
            move_grids.append(grids[index - 9])

        if 0 <= (index - 8) <= 63 and (not grids[index - 8].piece or grids[index - 8].piece.side != selected.side):
            move_grids.append(grids[index - 8])

        if 0 <= (index - 7) <= 63 and (index - 7) not in leftside and (not grids[index - 7].piece or grids[index - 7].piece.side != selected.side):
            move_grids.append(grids[index - 7])

        if 0 <= (index - 1) <= 63 and (index - 1) not in rightside and (not grids[index - 1].piece or grids[index - 1].piece.side != selected.side):
            move_grids.append(grids[index - 1])

        if 0 <= (index + 1) <= 63 and (index + 1) not in leftside and (not grids[index + 1].piece or grids[index + 1].piece.side != selected.side):
            move_grids.append(grids[index + 1])

        if 0 <= (index + 7) <= 63 and (index + 7) not in rightside and (not grids[index + 7].piece or grids[index + 7].piece.side != selected.side):
            move_grids.append(grids[index+7])

        if 0 <= (index + 8) <= 63 and (not grids[index + 8].piece or grids[index + 8].piece.side != selected.side):
            move_grids.append(grids[index + 8])

        if 0 <= (index + 9) <= 63 and (index + 9) not in leftside and (not grids[index + 9].piece or grids[index + 9].piece.side != selected.side):
            move_grids.append(grids[index + 9])


    elif name == "queen":
        for i in range(8):
            counter = index

            if i == 0:
                counter -= 9
                while 0 <= counter <= 63:
                    if counter in rightside:
                        break
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter -= 9

            elif i == 1:
                counter -= 8
                while 0 <= counter <= 63:
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter -= 8

            elif i == 2:
                counter -= 7
                while 0 <= counter <= 63:
                    if counter in leftside:
                        break
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter -= 7

            elif i == 3:
                counter -= 1
                while 0 <= counter <= 63:
                    if counter in rightside:
                        break
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter -= 1

            elif i == 4:
                counter += 1
                while 0 <= counter <= 63:
                    if counter in leftside:
                        break
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter += 1

            elif i == 5:
                counter += 7
                while 0 <= counter <= 63:
                    if counter in rightside:
                        break
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter += 7

            elif i == 6:
                counter += 8
                while 0 <= counter <= 63:
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter += 8

            elif i == 7:
                counter += 9
                while 0 <= counter <= 63:
                    if counter in leftside:
                        break
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter += 9

    if name == "rook":
        for i in range(4):

            counter = index

            if i == 0:
                counter -= 8
                while 0 <= counter <= 63:
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter -= 8

            elif i == 1:
                counter -= 1
                while 0 <= counter <= 63:
                    if counter in rightside:
                        break
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter -= 1

            elif i == 2:
                counter += 1
                while 0 <= counter <= 63:
                    if counter in leftside:
                        break
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter += 1

            elif i == 3:
                counter += 8
                while 0 <= counter <= 63:
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter += 8

    if name == "bishop":
        for i in range(4):

            counter = index

            if i == 0:
                counter -= 9
                while 0 <= counter <= 63:
                    if counter in rightside:
                        break
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter -= 9

            elif i == 1:
                counter -= 7
                while 0 <= counter <= 63:
                    if counter in leftside:
                        break
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter -= 7

            elif i == 2:
                counter += 7
                while 0 <= counter <= 63:
                    if counter in rightside:
                        break
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter += 7

            elif i == 3:
                counter += 9
                while 0 <= counter <= 63:
                    if counter in leftside:
                        break
                    if grids[counter].piece:
                        if grids[counter].piece.side != selected.side:
                            move_grids.append(grids[counter])
                            break
                        if grids[counter].piece.side == selected.side:
                            break
                    move_grids.append(grids[counter])
                    counter += 9


    if name == "pony":
        if not (index-1) in rightside:

            if 0 <= index - 17 <= 63 and (not grids[index - 17].piece or grids[index - 17].piece.side != selected.side):
                move_grids.append(grids[index - 17])

            if 0 <= index + 15 <= 63 and (not grids[index + 15].piece or grids[index + 15].piece.side != selected.side):
                move_grids.append(grids[index  + 15])

        if not (index+1) in leftside:

            if 0 <= index - 15 <= 63 and (not grids[index - 15].piece or grids[index - 15].piece.side != selected.side):
                move_grids.append(grids[index - 15])

            if 0 <= index + 17 <= 63 and (not grids[index + 17].piece or grids[index + 17].piece.side != selected.side):
                move_grids.append(grids[index  + 17])

        if not (index-2) in rightside and not (index-2) in range(6,64,8):

            if 0 <= index - 10 <= 63 and (not grids[index - 10].piece or grids[index - 10].piece.side != selected.side):
                move_grids.append(grids[index - 10])

            if 0 <= index + 6 <= 63 and (not grids[index + 6].piece or grids[index + 6].piece.side != selected.side):
                move_grids.append(grids[index + 6])

        if not (index+2) in leftside and not (index+2) in range(1,64,8):

            if 0 <= index - 6 <= 63 and (not grids[index - 6].piece or grids[index - 6].piece.side != selected.side):
                move_grids.append(grids[index - 6])

            if 0 <= index + 10 <= 63 and (not grids[index + 10].piece or grids[index + 10].piece.side != selected.side):
                move_grids.append(grids[index + 10])

    return move_grids

size = width,height = 900,720
dgrey = 102, 102, 153
screen = pygame.display.set_mode(size)
board = pygame.image.load("board.png")
highlight = pygame.image.load("highlight.png")
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

selected_grid = None
piecerects = [p.rect for p in pieces]
turn = True

while True:
    events = pygame.event.get()

    for g in grids:
        if g.rect.collidelist(piecerects) != -1:
            p_index = g.rect.collidelist(piecerects)
            g.piece = pieces[p_index]
            continue
        else:
            g.piece = None

    for event in events:

        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            mpos = pygame.mouse.get_pos()

            for g in grids:
                if g.piece and g.rect.collidepoint(mpos):
                    selected_grid = g

            if selected_grid and selected_grid.piece:
                for m in move(selected_grid):
                    if m.rect.collidepoint(mpos):
                        if m.piece and m.piece.side != selected.side and selected.side == turn:
                            m.piece.rect.topleft = 800,720
                            selected.rect.topleft = m.rect.topleft
                            break
                        selected.rect.topleft = m.rect.topleft
                        if not turn:
                            turn = 1
                        elif turn:
                            turn = 0

    screen.fill(dgrey)
    screen.blit(board, boardrect)

    if selected_grid and selected_grid.piece and move(selected_grid):
        for m in move(selected_grid):
            screen.blit(highlight, m.rect)

    for p in pieces:
        screen.blit(p.img, p.rect)

    pygame.display.flip()
