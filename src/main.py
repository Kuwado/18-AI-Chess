import pygame as pg
#import State as State
import rule as Rule
from src import State

MAX_WIDTH = 720
MAX_HEIGHT = 720
WIDTH = HEIGHT = 720
PIECE_WIDTH = PIECE_HEIGHT = HEIGHT // 8
UP_PIECE_WIDTH = UP_PIECE_HEIGHT = PIECE_HEIGHT * 4 // 5
images = {}
upimages = {}
whiteChess = (255, 250, 205)
blackChess = (0, 100, 0)
hlColor = (0, 191, 255)
hlColorMain = (255, 255, 0)
# Kích thước ảnh mới (bao gồm padding)
NEW_SIZE = (PIECE_WIDTH, PIECE_HEIGHT)

rule = Rule.Rule()

def add_padding(image, padding_color=(0, 0, 0, 0)):
    # Tạo ảnh mới có kích thước lớn hơn và fill với màu trong suốt
    padded_image = pg.Surface(NEW_SIZE, pg.SRCALPHA)
    padded_image.fill(padding_color)

    # Tính toán vị trí để đặt ảnh ban đầu vào trung tâm của ảnh mới
    x_offset = (NEW_SIZE[0] - image.get_width()) // 2
    y_offset = (NEW_SIZE[1] - image.get_height()) // 2

    # Đặt ảnh ban đầu vào trung tâm của ảnh mới
    padded_image.blit(image, (x_offset, y_offset))

    return padded_image


# Hàm load ảnh các quân cờ
def loadImages():
    pieces = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk', 'bp', 'br', 'bn', 'bb', 'bq', 'bk']
    for piece in pieces:
        upimages[piece] = pg.transform.smoothscale(pg.image.load("/Users/nampham/HUST/18-AI-Chess/images/pieces/" + piece + ".png"),(UP_PIECE_WIDTH, UP_PIECE_HEIGHT))
        images[piece] = add_padding(upimages[piece])


# Hàm main
def main():
    pg.init()
    screen = pg.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
    clock = pg.time.Clock()
    state = State.State()
    board = state.board
    val_move = state.validMove()
    moved = False
    loadImages()  
    running = True
    animate = False
    game_over = False
    move_log_font = pg.font.SysFont("Arial", 14, False, False)
    selected_piece = ()     # Lưu vị trí của quân cờ đang được chọn
    player_click = []    # Lưu vị trí trước và sau
    
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:  # Xử lý sự kiện khi chuột được nhấn
                if not game_over:
                    location = pg.mouse.get_pos()
                    clicked_row = location[1] // PIECE_HEIGHT
                    clicked_col = location[0] // PIECE_WIDTH
                    if selected_piece == (clicked_row, clicked_col):  # Nếu click 1 quân cờ 2 lần
                        selected_piece = ()
                        player_click = []
                    else:  # Nếu chưa có quân cờ được chọn
                        selected_piece = (clicked_row, clicked_col)
                        player_click.append(selected_piece)
                    if len(player_click) == 2:
                        move = State.Move(player_click[0], player_click[1], board)
                        print(move.getChessNote())
                        for i in range(len(val_move)):
                            if move == val_move[i]:
                                state.make_move(val_move[i])
                                moved = True
                                animate = True
                                selected_piece = ()
                                player_click = []
                        if not moved:
                            player_click = [selected_piece]
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    state.remake_move()
                    moved = True
                    animate = False
                    game_over = False
        if moved:
            if animate:
                animateMove(state.moveLog[-1], screen, state.board, clock)
            val_move = state.validMove()
             #print(val_move)
            moved = False
            animate = False

        drawGameState(screen, board, state, val_move, selected_piece)
        if state.checkMate:
            game_over = True
            if state.turn:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif state.staleMate:
            game_over = True
            drawEndGameText(screen, "Stalemate")
        clock.tick(15)
        pg.display.flip()  # Cập nhật màn hình

#Highlight
def highlightsq(screen, state, val_move, selected_piece):
    if selected_piece != ():
        row, col = selected_piece
        if state.board[row][col][0] == ('w' if state.turn else 'b'):
            s = pg.Surface((PIECE_WIDTH, PIECE_HEIGHT))
            s.set_alpha(100)
            s.fill(pg.Color('blue'))
            screen.blit(s, (col*PIECE_WIDTH, row*PIECE_HEIGHT))
            s.fill(pg.Color('yellow'))
            for move in val_move:
                if move.startRow == row and move.startCol == col:
                    screen.blit(s, (PIECE_WIDTH*move.endCol, PIECE_HEIGHT*move.endRow))
# Hàm khởi tạo sàn đấu
def drawGameState(screen, board, state, val_move, selected_piece):
    drawBoard(screen)
    highlightsq(screen, state, val_move, selected_piece)
    drawChessPieces(screen, board)

# Hàm vẽ bàn cờ
def drawBoard(screen):
    # Vẽ bàn cờ
    screen.fill(whiteChess)  # Màu nền trắng
    # Vẽ các ô cờ
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 1:  # Xác định màu ô cờ
                pg.draw.rect(screen, blackChess, (col * PIECE_WIDTH, row * PIECE_HEIGHT, PIECE_WIDTH, PIECE_HEIGHT))


# Hàm vẽ vị trí ban đầu của quân cờ
def drawChessPieces(screen, board):
    # Vẽ quân cờ
    for row in range(8):
        for column in range(8):
            piece = board[row][column]
            if piece != "--":
                screen.blit(images[piece], pg.Rect(column * PIECE_WIDTH, row * PIECE_HEIGHT, PIECE_WIDTH, PIECE_HEIGHT))

def drawEndGameText(screen, text):
    font = pg.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, pg.Color("gray"))
    text_location = pg.Rect(0, 0, MAX_WIDTH, MAX_HEIGHT).move(MAX_WIDTH / 2 - text_object.get_width() / 2,
                                                                 MAX_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, pg.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))



def animateMove(move, screen, board, clock):
    global colors
    colors = [pg.Color(whiteChess), pg.Color(blackChess)]
    coords = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSq = 10
    frameCount = (abs(dR) + abs(dC))*framesPerSq
    for frame in range(frameCount+1):
        row, col = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawChessPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSq = pg.Rect(move.endCol*PIECE_WIDTH, move.endRow*PIECE_HEIGHT, PIECE_WIDTH, PIECE_HEIGHT)
        pg.draw.rect(screen, color, endSq)
        if move.piece_cap != '--':
            screen.blit(images[move.piece_cap], endSq)
        screen.blit(images[move.piece_move], pg.Rect(col*PIECE_WIDTH, row*PIECE_HEIGHT, PIECE_WIDTH, PIECE_HEIGHT))
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
