import pygame as pg
import rule as rule
state = rule.GameState()
MAX_WIDTH = 1138
MAX_HEIGHT = 736
WIDTH = HEIGHT = 640
PIECE_WIDTH = PIECE_HEIGHT = HEIGHT / 8
UP_PIECE_WIDTH = UP_PIECE_HEIGHT = PIECE_HEIGHT * 4 / 5
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
        upimages[piece] = pg.transform.smoothscale(pg.image.load("images/pieces/" + piece + ".png"), (UP_PIECE_WIDTH, UP_PIECE_HEIGHT))
        images[piece] = add_padding(upimages[piece])

# Hàm main
def main():
    pg.init()
    screen = pg.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
    loadImages()  # do this only once before while loop
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        drawGameState(screen, state)
        

        
        pg.display.flip()  # Cập nhật màn hình
    pg.quit()

# Hàm khởi tạo sàn đấu
def drawGameState(screen, state):
    drawBoard(screen)  # draw squares on the board
    drawChessPieces(screen, state)  # draw pieces on top of those squares

# Hàm vẽ bàn cờ
def drawBoard(screen):
    # Vẽ bàn cờ
    screen.fill(whiteChess)  # Màu nền trắng
    # Vẽ các ô cờ
    for row in range(8):
        for col in range(8):
            if ((row + col) % 2 == 0): # Xác định màu ô cờ
                pg.draw.rect(screen, blackChess, (col * PIECE_WIDTH, row * PIECE_HEIGHT, PIECE_WIDTH, PIECE_HEIGHT))
            
# Hàm vẽ vị trí ban đầu của quân cờ
def drawChessPieces(screen, state):
    # Vẽ quân cờ
   for row in range(8):
        for column in range(8):
            piece = state.board[row][column]
            if piece != "--":
                screen.blit(images[piece], pg.Rect(column * PIECE_WIDTH, row * PIECE_WIDTH, PIECE_WIDTH, PIECE_WIDTH))









main()
