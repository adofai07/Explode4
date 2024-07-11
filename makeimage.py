from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np

N = 500
RED = "#eb3734"
BLUE = "#343deb"
GRAY = "#454545"

def make_image(board: list[list[int]], fname: str="board.png") -> None:
    img = Image.new("RGB", (N * 5, N * 5))
    
    draw = ImageDraw.Draw(img)
    
    for i in range(1, 5):
        draw.line([(0, N * i), (N * 5, N * i)], fill="white", width=N // 20)
        draw.line([(N * i, 0), (N * i, N * 5)], fill="white", width=N // 20)
        
    font = ImageFont.truetype("FiraCode-Regular.ttf", round(N / 1.4))
    
    for i in range(5):
        for j in range(5):
            if board[i][j] == 0:
                c = GRAY
            if board[i][j] < 0:
                c = RED
            if board[i][j] > 0:
                c = BLUE

            _, _, w, h = draw.textbbox((0, 0), str(abs(board[i][j])), font=font)
            draw.text((N // 2 + N * j - w / 2, N // 2 + N * i - h / 2 - N // 10), str(abs(board[i][j])), c, font=font)
    
    
    img.save(fname)
    
def make_images(*boards: list[list[int]], fname: str="board.png") -> None:
    l = len(boards)
    
    for i in range(l):
        make_image(boards[i], F".temp{i}.png")
        
    img = np.zeros((N * 5, N * 5 * l + (N // 20) * (l - 1), 3), dtype=np.uint8)
    
    for i in range(l):
        img[:, N * 5 * i + (N // 20) * i: N * 5 * (i + 1) + (N // 20) * i, :] = cv2.imread(F".temp{i}.png")
        
        if i != l - 1:
            img[:, N * 5 * (i + 1) + (N // 20) * i:N * 5 * (i + 1) + (N // 20) * i + N // 20] = [0, 255, 0]
    
    cv2.imwrite(fname, img)
    
if __name__ == "__main__":
    
    # make_image(
    #     [
    #         [0, 0, 0, 0, 1],
    #         [0, 0, 0, -1, 0],
    #         [0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0]
    #     ]
    # )
    
    make_images(
        [
            [ 0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0],
            [ 0,  0,  3,  0,  0],
            [ 0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0],
        ],
        [
            [ 0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0],
            [ 0,  0,  3,  0,  0],
            [ 0,  0,  0, -3,  0],
            [ 0,  0,  0,  0,  0],
        ],
        [
            [ 0,  0,  0,  0,  0],
            [ 0,  0,  1,  0,  0],
            [ 0,  1,  0,  1,  0],
            [ 0,  0,  1, -3,  0],
            [ 0,  0,  0,  0,  0],
        ],
        [
            [ 0,  0,  0,  0,  0],
            [ 0,  0,  1,  0,  0],
            [ 0,  1,  0, -2,  0],
            [ 0,  0, -2,  0, -1],
            [ 0,  0,  0, -1,  0],
        ],
    )