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
    selected_piece = ()     # Lưu vị trí của quân cờ đang được chọn
    player_click = []       # Lưu vị trí trước và sau
    
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:  # Xử lý sự kiện khi chuột được nhấn
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
                            selected_piece = ()
                            player_click = []
                    if not moved:
                        player_click = [selected_piece]
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    state.remake_move()
                    moved = True
        if moved:
           val_move = state.validMove()
           #print(val_move)
           moved = False

        drawGameState(screen, board)
        clock.tick(15)
        pg.display.flip()  # Cập nhật màn hình

# Hàm khởi tạo sàn đấu
def drawGameState(screen, board):
    drawBoard(screen)
    drawChessPieces(screen, board)
    #highlight(screen, board, pos)


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

# Hàm tô những ô quân cờ có thể đi được
def highlight(screen, board, pos):
    moves = []
    if len(pos) == 2:
        if board[pos[0]][pos[1]][1] == 'p':
            rule.getPMove(board, pos[0], pos[1], moves)
        if board[pos[0]][pos[1]][1] == 'n':
            rule.getPMove(board, pos[0], pos[1], moves)
        if board[pos[0]][pos[1]][1] == 'r':
            rule.getPMove(board, pos[0], pos[1], moves)
        if board[pos[0]][pos[1]][1] == 'b':
            rule.getPMove(board, pos[0], pos[1], moves)
        if board[pos[0]][pos[1]][1] == 'q':
            rule.getPMove(board, pos[0], pos[1], moves)
        if board[pos[0]][pos[1]][1] == 'k':
            rule.getPMove(board, pos[0], pos[1], moves)
        anphaBG(screen, hlColorMain, pos)
        for move in moves:
            anphaBG(screen, hlColor, move)

# Hàm tô background mờ
def anphaBG(screen, color, pos):
    hl_rect = pg.Rect(pos[1] * PIECE_WIDTH, pos[0] * PIECE_HEIGHT, PIECE_WIDTH, PIECE_HEIGHT)
    hl_surface = pg.Surface((PIECE_WIDTH, PIECE_HEIGHT))
    hl_surface.set_alpha(100)  # Đặt độ trong suốt
    pg.draw.rect(hl_surface, color, hl_surface.get_rect())  # Vẽ hình chữ nhật trong suốt
    screen.blit(hl_surface, hl_rect)




if __name__ == "__main__":
    main()
