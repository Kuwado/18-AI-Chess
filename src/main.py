import pygame as pg
import rule as rule

MAX_WIDTH = 800
MAX_HEIGHT = 800
WIDTH = HEIGHT = 800
PIECE_WIDTH = PIECE_HEIGHT = HEIGHT // 8
UP_PIECE_WIDTH = UP_PIECE_HEIGHT = PIECE_HEIGHT * 4 // 5
images = {}
upimages = {}
whiteChess = (255, 250, 205)
blackChess = (0, 100, 0)
# Kích thước ảnh mới (bao gồm padding)
NEW_SIZE = (PIECE_WIDTH, PIECE_HEIGHT)


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
        upimages[piece] = pg.transform.smoothscale(pg.image.load("images/pieces/" + piece + ".png"),(UP_PIECE_WIDTH, UP_PIECE_HEIGHT))
        images[piece] = add_padding(upimages[piece])


# Hàm main
def main():
    pg.init()
    screen = pg.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
    state = rule.GameState()
    board = state.board
    loadImages()  # do this only once before while loop
    running = True
    selected_piece = ()  # Lưu vị trí của quân cờ đang được chọn
    player_click = []
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:  # Xử lý sự kiện khi chuột được nhấn
                location = pg.mouse.get_pos()
                clicked_row = location[1] // PIECE_HEIGHT
                clicked_col = location[0] // PIECE_WIDTH
                if selected_piece == (clicked_row, clicked_col):  # Nếu chưa có quân cờ nào được chọn
                    selected_piece = ()
                    player_click = []
                else:  # Nếu đã có quân cờ được chọn
                    selected_piece = (clicked_row, clicked_col)
                    player_click.append(selected_piece)
                    if len(player_click) == 2:
                        move_piece(player_click[0], player_click[1], board)
                        selected_piece = ()  # reset user clicks
                        player_click = []
        drawGameState(screen, state, board)
        pg.display.flip()  # Cập nhật màn hình


def move_piece(start, end, board):
    # Lấy thông tin về quân cờ tại vị trí xuất phát
    piece_to_move = board[start[0]][start[1]]
    # Di chuyển quân cờ đến vị trí đích
    board[end[0]][end[1]] = piece_to_move
    # Đặt ô cờ xuất phát thành trống
    board[start[0]][start[1]] = "--"


# Hàm khởi tạo sàn đấu
def drawGameState(screen, state, board):
    drawBoard(screen)  # draw squares on the board
    drawChessPieces(screen, board)  # draw pieces on top of those squares


# Hàm vẽ bàn cờ
def drawBoard(screen):
    # Vẽ bàn cờ
    screen.fill(whiteChess)  # Màu nền trắng
    # Vẽ các ô cờ
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:  # Xác định màu ô cờ
                pg.draw.rect(screen, blackChess,
                             (col * PIECE_WIDTH, row * PIECE_HEIGHT, PIECE_WIDTH, PIECE_HEIGHT))


# Hàm vẽ vị trí ban đầu của quân cờ
def drawChessPieces(screen, board):
    # Vẽ quân cờ
    for row in range(8):
        for column in range(8):
            piece = board[row][column]
            if piece != "--":
                screen.blit(images[piece],
                            pg.Rect(column * PIECE_WIDTH, row * PIECE_HEIGHT, PIECE_WIDTH, PIECE_HEIGHT))


if __name__ == "__main__":
    main()
