import pygame as pg
#import State as State
import rule as Rule
import State
import Minimax
import queue



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
    selected_piece = ()                 # Lưu vị trí của quân cờ được chọn bởi người chơi
    last_selected_piece = ()           # Lưu vị trí trước đó của quân cờ được chọn bởi người chơi
    last_selected_piece_computer = ()  # Lưu vị trí trước đó của quân cờ được chọn bởi máy cơ
    player_click = []
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if not game_over:
            # Lấy danh sách các nước đi hợp lệ từ trạng thái hiện tại
            valid_moves = state.validMove()
            if not state.turn:  # Lượt của AI
                # Tìm nước đi tốt nhất cho AI bằng thuật toán minimax
                return_queue = queue.Queue()
                Minimax.findBestMove(state, valid_moves, return_queue)
                next_move = return_queue.get()  # Đợi cho AI chọn nước đi
                for i in range(len(valid_moves)):
                    if next_move == valid_moves[i]:
                        last_selected_piece_computer = selected_piece  # Cập nhật vị trí trước đó của máy cơ
                        state.makeMove(valid_moves[i])
                        animate = True
                        moved = True
                        state.turn = True  # Chuyển lượt sang cho người chơi
                        break
            else:  # Lượt của người chơi
                # Xử lý khi người chơi nhấn chuột
                if event.type == pg.MOUSEBUTTONDOWN:
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
                            for i in range(len(val_move)):
                                if move == val_move[i]:
                                    state.makeMove(val_move[i])
                                    moved = True
                                    animate = True
                                    selected_piece = ()
                                    player_click = []
                            if not moved:
                                player_click = [selected_piece]
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_z:
                        state.remakeMove()
                        moved = True
                        animate = False
                        game_over = False

        # Nếu cờ di chuyển    
        if moved:
            if animate:
                animateMove(state.moveLog[-1], screen, state.board, clock)
            val_move = state.validMove()
            moved = False
            animate = False

        drawGameState(screen, board, state, val_move, selected_piece, last_selected_piece, last_selected_piece_computer)
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



def drawGameState(screen, board, state, val_move, selected_piece, last_selected_piece, last_selected_piece_computer):
    drawBoard(screen)
    highlightsq(screen, state, val_move, selected_piece, last_selected_piece, last_selected_piece_computer)
    drawChessPieces(screen, board)

def highlightsq(screen, state, val_move, selected_piece, last_selected_piece, last_selected_piece_computer):
    if selected_piece != () and state.turn:
        row, col = selected_piece
        if state.board[row][col][0] == 'w':
            # Tạo một bề mặt màu đỏ cho quân cờ được chọn bởi người chơi
            selected_surface = pg.Surface((PIECE_WIDTH, PIECE_HEIGHT))
            selected_surface.set_alpha(100)
            selected_surface.fill(pg.Color('red'))
            screen.blit(selected_surface, (col * PIECE_WIDTH, row * PIECE_HEIGHT))
            
            # Iterate over valid moves and highlight them in yellow
            yellow_surface = pg.Surface((PIECE_WIDTH, PIECE_HEIGHT))
            yellow_surface.set_alpha(100)
            yellow_surface.fill(pg.Color('yellow'))
            for move in val_move:
                if move.startRow == row and move.startCol == col:
                    screen.blit(yellow_surface, (move.endCol * PIECE_WIDTH, move.endRow * PIECE_HEIGHT))
    
    # Highlight vị trí trước đó và vị trí hiện tại của máy cơ
    if last_selected_piece_computer:
        row, col = last_selected_piece_computer
        # Tạo một bề mặt màu đỏ cho vị trí trước đó của máy cơ
        last_selected_surface = pg.Surface((PIECE_WIDTH, PIECE_HEIGHT))
        last_selected_surface.set_alpha(100)
        last_selected_surface.fill(pg.Color('blue'))  # Thay đổi màu sắc
        screen.blit(last_selected_surface, (col * PIECE_WIDTH, row * PIECE_HEIGHT))
    if state.moveLog:
        last_move = state.moveLog[-1]
        start_row, start_col = last_move.startRow, last_move.startCol  # Vị trí ban đầu của nước đi
        end_row, end_col = last_move.endRow, last_move.endCol  # Vị trí kết thúc của nước đi

        # Tạo một bề mặt màu đỏ cho vị trí hiện tại của máy cơ
        last_selected_surface = pg.Surface((PIECE_WIDTH, PIECE_HEIGHT))
        last_selected_surface.set_alpha(100)
        last_selected_surface.fill(pg.Color('blue'))  # Thay đổi màu sắc

        # Vẽ bề mặt này lên màn hình tại vị trí ban đầu và vị trí kết thúc của nước đi cuối cùng
        screen.blit(last_selected_surface, (start_col * PIECE_WIDTH, start_row * PIECE_HEIGHT))
        screen.blit(last_selected_surface, (end_col * PIECE_WIDTH, end_row * PIECE_HEIGHT))



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
    font = pg.font.SysFont("Helvetica", 72, True, False)
    
    # Vị trí trung tâm màn hình
    x, y = screen.get_width() // 2, screen.get_height() // 2
    
    # Màu chữ và màu glow
    text_color = (255, 0, 0)  # Chữ màu đỏ
    glow_color = (255, 255, 0)  # Glow màu vàng
    glow_radius = 20  # Bán kính glow

    # Vẽ nhiều lớp chữ với các bán kính khác nhau để tạo hiệu ứng glow
    for i in range(glow_radius, 0, -1):
        glow_surface = font.render(text, True, glow_color)
        alpha = int(255 * (i / glow_radius))  # Điều chỉnh độ trong suốt
        glow_surface.set_alpha(alpha)
        screen.blit(glow_surface, (x - glow_surface.get_width() // 2, y - glow_surface.get_height() // 2))

    # Vẽ lớp chữ chính
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)



def animateMove(move, screen, board, clock):
    global colors
    colors = [pg.Color(whiteChess), pg.Color(blackChess)]
    coords = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSq = 5
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
