
import random
import sys
import time
import pygame
from pygame.locals import *
from collections import deque

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
SIZE = 20

def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("貪吃蛇")

    light = (100, 100, 100)  # 食物顏色
    dark = (20, 20, 250)   # 蛇的顏色
    dark2 = (255, 10, 10)   # 蛇的顏色

    font1 = pygame.font.SysFont("SimHei", 24)  # 得分的字體
    font2 = pygame.font.Font(None, 72)  # GAME OVER 的字體
    red = (200, 30, 30)                 # GAME OVER 的字體顏色
    fwidth, fheight = font2.size("GAME OVER")
    line_width = 1                      # 網格線寬度
    black = (0, 0, 0)                   # 網格線顏色
    bgcolor = (40, 40, 60)              # 背景色

    # 方向，起始向右
    pos_x = 1
    pos_y = 0
    pos_x2 = -1
    pos_y2 = 0
    # 如果蛇正在向右移動，那麽快速點擊向下向左，由於程序刷新沒那麽快，向下事件會被向左覆蓋掉，導致蛇後退，直接GAME OVER
    # b 變量就是用於防止這種情況的發生
    b = True
    b2 = True
    # 範圍
    scope_x = (0, SCREEN_WIDTH // SIZE - 1)
    scope_y = (2, SCREEN_HEIGHT // SIZE - 1)
    # 蛇
    snake = deque()
    snake2 = deque()
    # 食物
    food_x = 0
    food_y = 0
    food_x2 = 0
    food_y2 = 0

    # 初始化蛇
    def _init_snake():
        nonlocal snake
        snake.clear()
        snake.append((2, scope_y[0]))
        snake.append((1, scope_y[0]))
        snake.append((0, scope_y[0]))
    def _init_snake2():
        nonlocal snake2
        snake2.clear()
        snake2.append((scope_x[1]-2, scope_y[0]))
        snake2.append((scope_x[1]-1, scope_y[0]))
        snake2.append((scope_x[1], scope_y[0]))

    # 食物
    def _create_food():
        nonlocal food_x, food_y
        food_x = random.randint(scope_x[0], scope_x[1])
        food_y = random.randint(scope_y[0], scope_y[1])
        while (food_x, food_y) in snake:
            # 為了防止食物出到蛇身上
            food_x = random.randint(scope_x[0], scope_x[1])
            food_y = random.randint(scope_y[0], scope_y[1])
        while (food_x, food_y) in snake2:
            # 為了防止食物出到蛇身上
            food_x = random.randint(scope_x[0], scope_x[1])
            food_y = random.randint(scope_y[0], scope_y[1])
    def _create_food2():
        nonlocal food_x2, food_y2
        food_x2 = random.randint(scope_x[0], scope_x[1])
        food_y2 = random.randint(scope_y[0], scope_y[1])
        while (food_x2, food_y2) in snake:
            # 為了防止食物出到蛇身上
            food_x2 = random.randint(scope_x[0], scope_x[1])
            food_y2 = random.randint(scope_y[0], scope_y[1])
        while (food_x2, food_y2) in snake2:
            # 為了防止食物出到蛇身上
            food_x2 = random.randint(scope_x[0], scope_x[1])
            food_y2 = random.randint(scope_y[0], scope_y[1])

    _init_snake()
    _init_snake2()
    _create_food()
    _create_food2()

    game_over = True
    start = False       # 是否開始，當start = True，game_over = True 時，才顯示 GAME OVER
    score = 0           # 得分
    orispeed = 0.25      # 原始速度
    speed = orispeed
    last_move_time = None
    pause = False       # 暫停
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over:
                        start = True
                        game_over = False
                        b = True
                        _init_snake()
                        _init_snake2()
                        _create_food()
                        _create_food2()
                        pos_x = 1
                        pos_y = 0
                        pos_x2 = -1
                        pos_y2 = 0
                        # 得分
                        score = 0
                        last_move_time = time.time()
                elif event.key == K_SPACE:
                        _create_food()
                        _create_food2()
                elif event.key == K_w:
                    # 這個判斷是為了防止蛇向上移時按了向下鍵，導致直接 GAME OVER
                    if b and not pos_y:
                        pos_x = 0
                        pos_y = -1
                        b = False
                elif event.key == K_s:
                    if b and not pos_y:
                        pos_x = 0
                        pos_y = 1
                        b = False
                elif event.key == K_a:
                    if b and not pos_x:
                        pos_x = -1
                        pos_y = 0
                        b = False
                elif event.key == K_d:
                    if b and not pos_x:
                        pos_x = 1
                        pos_y = 0
                        b = False
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    # 這個判斷是為了防止蛇向上移時按了向下鍵，導致直接 GAME OVER
                    if b2 and not pos_y2:
                        pos_x2 = 0
                        pos_y2 = -1
                        b2 = False
                elif event.key == K_DOWN:
                    if b2 and not pos_y2:
                        pos_x2 = 0
                        pos_y2 = 1
                        b2 = False
                elif event.key == K_LEFT:
                    if b2 and not pos_x2:
                        pos_x2 = -1
                        pos_y2 = 0
                        b2 = False
                elif event.key == K_RIGHT:
                    if b2 and not pos_x2:
                        pos_x2 = 1
                        pos_y2 = 0
                        b2 = False

        # 填充背景色
        screen.fill(bgcolor)
        # 畫網格線 豎線
        for x in range(SIZE, SCREEN_WIDTH, SIZE):
            pygame.draw.line(screen, black, (x, scope_y[0] * SIZE), (x, SCREEN_HEIGHT), line_width)
        # 畫網格線 橫線
        for y in range(scope_y[0] * SIZE, SCREEN_HEIGHT, SIZE):
            pygame.draw.line(screen, black, (0, y), (SCREEN_WIDTH, y), line_width)

        if game_over:
            if start:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth)//2, (SCREEN_HEIGHT - fheight)//2, "GAME OVER", red)
        else:
            curTime = time.time()
            if curTime - last_move_time > speed:
                if not pause:
                    b = True
                    next_s = (snake[0][0] + pos_x, snake[0][1] + pos_y)
                    if next_s[0] == food_x and next_s[1] == food_y:
                        # 吃到了食物
                        _create_food()
                        snake.appendleft(next_s)
                        score += 10
                        speed = orispeed - 0.03 * (score // 100)
                    elif next_s[0] == food_x2 and next_s[1] == food_y2:
                        # 吃到了食物
                        _create_food2()
                        snake.appendleft(next_s)
                        score += 10
                        speed = orispeed - 0.01 * (score // 100)
                    else:
                        if scope_x[0] <= next_s[0] <= scope_x[1] and scope_y[0] <= next_s[1] <= scope_y[1] and next_s not in snake:
                            snake.appendleft(next_s)
                            snake.pop()
                        else:
                            game_over = True
            curTime = time.time()
            if curTime - last_move_time > speed:
                if not pause:
                    b2 = True
                    last_move_time = curTime
                    next_s2 = (snake2[0][0] + pos_x2, snake2[0][1] + pos_y2)
                    if next_s2[0] == food_x and next_s2[1] == food_y:
                        # 吃到了食物
                        _create_food()
                        snake2.appendleft(next_s2)
                        score += 10
                        speed = orispeed - 0.03 * (score // 100)
                    elif next_s2[0] == food_x2 and next_s2[1] == food_y2:
                        # 吃到了食物
                        _create_food2()
                        snake2.appendleft(next_s2)
                        score += 10
                        speed = orispeed - 0.01 * (score // 100)
                    else:
                        if scope_x[0] <= next_s2[0] <= scope_x[1] and scope_y[0] <= next_s2[1] <= scope_y[1] and next_s2 not in snake2:
                            snake2.appendleft(next_s2)
                            snake2.pop()
                        else:
                            game_over = True
        # 畫食物
        if not game_over:
            # 避免 GAME OVER 的時候把 GAME OVER 的字給遮住了
            pygame.draw.rect(screen, light, (food_x * SIZE, food_y * SIZE, SIZE, SIZE), 0)
            pygame.draw.rect(screen, light, (food_x2 * SIZE, food_y2 * SIZE, SIZE, SIZE), 0)

        # 畫蛇
        for s in snake:
            pygame.draw.rect(screen, dark, (s[0] * SIZE + line_width, s[1] * SIZE + line_width,
                                            SIZE - line_width * 2, SIZE - line_width * 2), 0)
        for s2 in snake2:
            pygame.draw.rect(screen, dark2, (s2[0] * SIZE + line_width, s2[1] * SIZE + line_width,
                                            SIZE - line_width * 2, SIZE - line_width * 2), 0)

        print_text(screen, font1, 30, 7, f"speed: {score//100}")
        print_text(screen, font1, 200, 7, f"score: {score}")

        pygame.display.update()


if __name__ == "__main__":
    main()