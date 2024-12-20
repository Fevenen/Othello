import sys
import pygame
import random

board = [[0] * 8 for _ in range(8)]
board[4][4] = -1
board[3][3] = -1
board[4][3] = 1
board[3][4] = 1

directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, 1), (0, -1), (1, 0)]

pygame.mixer.init()
down_music = pygame.mixer.Sound("music/down.mp3")  # 在棋盘上落子的声音 许可:CC0 作者:代号091 来源:耳聆网 https://www.ear0.com/sound/39400


def random_AI(player):
    lst = []
    for x in range(8):
        for y in range(8):
            if is_valid(x, y, player):
                lst.append((x, y))
    index = random.randint(0, len(lst) - 1)
    i, j = lst.pop(index)
    board[i][j] = player
    turn(i, j, player)
    down_music.play()


def max_AI(player):
    lst1 = []
    lst2 = []
    indexes = []
    for x in range(8):
        for y in range(8):
            if is_valid(x, y, player):
                for dx, dy in directions:
                    sx, sy = x + dx, y + dy
                    c = 0
                    while 0 <= sx < 8 and 0 <= sy < 8 and board[sx][sy] == -player:
                        sx += dx
                        sy += dy
                        c += 1
                        if 0 <= sx < 8 and 0 <= sy < 8 and board[sx][sy] == player:
                            lst1.append((x, y, c))
                            lst2.append(c)
    for i in range(lst2.count(max(lst2))):
        indexes.append(lst2.index(max(lst2)) + i)
        lst2.remove(max(lst2))
    r = random.randint(0, len(indexes) - 1)
    index = indexes[r]
    i, j = lst1[index][0], lst1[index][1]
    board[i][j] = player
    turn(i, j, player)
    down_music.play()


def plus_AI(player):
    flag = True
    angles = [(0, 0), (0, 7), (7, 0), (7, 7)]
    vice_angles = [(2, 2), (2, 5), (5, 2), (5, 5)]
    centers = [(2, 3), (2, 4), (3, 2), (4, 2), (3, 5), (4, 5), (5, 3), (5, 4)]
    vice_centers = [(1, 2), (1, 5), (2, 1), (2, 6), (6, 2), (6, 5), (5, 1), (5, 6)]
    length = [(0, 2), (0, 5), (2, 0), (5, 0), (2, 7), (7, 2), (7, 5), (5, 7)]
    random.shuffle(angles)
    random.shuffle(vice_angles)
    random.shuffle(centers)
    random.shuffle(vice_centers)
    for x, y in angles:
        if is_valid(x, y, player) and flag is True:
            board[x][y] = player
            turn(x, y, player)
            down_music.play()
            flag = False

    for x, y in vice_angles:
        if is_valid(x, y, player) and flag is True:
            board[x][y] = player
            turn(x, y, player)
            down_music.play()
            flag = False

    for x, y in centers:
        if is_valid(x, y, player) and flag is True:
            board[x][y] = player
            turn(x, y, player)
            down_music.play()
            flag = False

    for x, y in length:
        if is_valid(x, y, player) and flag is True:
            board[x][y] = player
            turn(x, y, player)
            down_music.play()
            flag = False

    for x, y in vice_centers:
        if is_valid(x, y, player) and flag is True:
            board[x][y] = player
            turn(x, y, player)
            down_music.play()
            flag = False

    if flag is True:
        max_AI(player)


def is_valid(x, y, player):
    if not (0 <= x < 8 and 0 <= y < 8) or board[x][y] != 0:
        return False

    for dx, dy in directions:
        sx, sy = x + dx, y + dy
        while 0 <= sx < 8 and 0 <= sy < 8 and board[sx][sy] == -player:
            sx += dx
            sy += dy
            if 0 <= sx < 8 and 0 <= sy < 8 and board[sx][sy] == player:
                return True
    return False


def turn(x, y, player):
    for dx, dy in directions:
        sx, sy = x + dx, y + dy
        c = 0
        while 0 <= sx < 8 and 0 <= sy < 8 and board[sx][sy] == -player:
            sx += dx
            sy += dy
            c += 1
            if 0 <= sx < 8 and 0 <= sy < 8 and board[sx][sy] == player:
                for i in range(c + 1):
                    board[x + dx * i][y + dy * i] = player


class Center:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load("image/bmp/center.bmp")
        self.rect = self.image.get_rect()
        self.rect.centerx = 400
        self.rect.centery = self.screen_rect.centery

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Black:
    def __init__(self, screen, x, y):
        super(Black, self).__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load("image/bmp/black.bmp")
        self.rect = self.image.get_rect()
        self.rect.centerx = 120 + 80 * x
        self.rect.centery = 170 + 80 * y

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class White:
    def __init__(self, screen, x, y):
        super(White, self).__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load("image/bmp/white.bmp")
        self.rect = self.image.get_rect()
        self.rect.centerx = 120 + 80 * x
        self.rect.centery = 170 + 80 * y

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Black_score:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load("image/bmp/black.bmp")
        self.rect = self.image.get_rect()
        self.rect.centerx = 900
        self.rect.centery = 350

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class White_score:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load("image/bmp/white.bmp")
        self.rect = self.image.get_rect()
        self.rect.centerx = 900
        self.rect.centery = 550

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Score1:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont("arial", 60)
        self.score_str = ""
        self.score_image = self.font.render(self.score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = 980
        self.score_rect.centery = 350

    def blitme(self):
        self.font = pygame.font.SysFont("arial", 60)
        self.score_image = self.font.render(self.score_str, True, self.text_color)
        self.score_rect.right = 980
        self.score_rect.centery = 350
        self.screen.blit(self.score_image, self.score_rect)


class Score2:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont("arial", 60)
        self.score_str = ""
        self.score_image = self.font.render(self.score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = 980
        self.score_rect.centery = 550

    def blitme(self):
        self.font = pygame.font.SysFont("arial", 60)
        self.score_image = self.font.render(self.score_str, True, self.text_color)
        self.score_rect.right = 980
        self.score_rect.centery = 550
        self.screen.blit(self.score_image, self.score_rect)


class Win:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont("arial", 100)
        self.black_str = "Black Win!!!"
        self.white_str = "White Win!!!"
        self.black_image = self.font.render(self.black_str, True, self.text_color)
        self.white_image = self.font.render(self.white_str, True, self.text_color)
        self.black_rect = self.black_image.get_rect()
        self.white_rect = self.white_image.get_rect()
        self.black_rect.centerx = self.white_rect.centerx = self.screen_rect.centerx
        self.black_rect.centery = self.white_rect.centery = self.screen_rect.centery

    def black_blitme(self):
        self.font = pygame.font.SysFont("arial", 100)
        self.black_image = self.font.render(self.black_str, True, self.text_color)
        self.black_rect.centerx = self.screen_rect.centerx
        self.black_rect.centery = self.screen_rect.centery
        self.screen.blit(self.black_image, self.black_rect)

    def white_blitme(self):
        self.font = pygame.font.SysFont("arial", 100)
        self.white_image = self.font.render(self.white_str, True, self.text_color)
        self.white_rect.centerx = self.screen_rect.centerx
        self.white_rect.centery = self.screen_rect.centery
        self.screen.blit(self.white_image, self.white_rect)


class Draw:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont("arial", 100)
        self.str = "Draw!!!"
        self.image = self.font.render(self.str, True, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.rect.centery = self.screen_rect.centery

    def blitme(self):
        self.font = pygame.font.SysFont("arial", 100)
        self.image = self.font.render(self.str, True, self.text_color)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.screen.blit(self.image, self.rect)


class Red_point_black:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont("arial", 200)
        self.str = "`"
        self.image = self.font.render(self.str, True, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.centerx = 940
        self.rect.centery = 380

    def blitme(self):
        self.font = pygame.font.SysFont("arial", 200)
        self.image = self.font.render(self.str, True, self.text_color)
        self.rect.centerx = 940
        self.rect.centery = 380
        self.screen.blit(self.image, self.rect)


class Red_point_white:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont("arial", 200)
        self.str = "`"
        self.image = self.font.render(self.str, True, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.centerx = 940
        self.rect.centery = 580

    def blitme(self):
        self.font = pygame.font.SysFont("arial", 200)
        self.image = self.font.render(self.str, True, self.text_color)
        self.rect.centerx = 940
        self.rect.centery = 580
        self.screen.blit(self.image, self.rect)


class Yellow_point:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load("image/bmp/yellow_point.bmp")
        self.rect = self.image.get_rect()
        self.rect.centerx = 120 + 80 * x
        self.rect.centery = 170 + 80 * y

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Edge:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load("image/bmp/edge.bmp")
        self.rect = self.image.get_rect()
        self.rect.centerx = 120 + 80 * x
        self.rect.centery = 170 + 80 * y

    def blitme(self):
        self.screen.blit(self.image, self.rect)


def run_game():
    time = 0
    pygame.init()
    screen = pygame.display.set_mode((1200, 900))
    color = (230, 230, 230)
    center = Center(screen)
    black_score = Black_score(screen)
    white_score = White_score(screen)
    score1 = Score1(screen)
    score2 = Score2(screen)
    win = Win(screen)
    draw = Draw(screen)
    red_point_black = Red_point_black(screen)
    red_point_white = Red_point_white(screen)
    pygame.display.set_caption("othello_PVE_max_AI")
    game = 0
    player = 1
    match = 2
    while True:
        if game == 0:
            for x in range(8):
                for y in range(8):
                    board[x][y] = 0
                    board[4][4] = -1
                    board[3][3] = -1
                    board[4][3] = 1
                    board[3][4] = 1
            player = 1
            game = 1
            pygame.display.flip()
            screen.fill(color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

        if game == 1:
            b = 0
            w = 0
            check = check1 = check2 = 0
            pygame.mouse.set_cursor(pygame.cursors.ball)
            pygame.display.flip()
            screen.fill(color)
            black_score.blitme()
            white_score.blitme()
            score1.blitme()
            score2.blitme()
            center.blitme()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for x in range(8):
                for y in range(8):
                    black = Black(screen, x, y)
                    white = White(screen, x, y)
                    if board[x][y] == 1:
                        black.blitme()
                    if board[x][y] == -1:
                        white.blitme()
            for x in range(8):
                for y in range(8):
                    if board[x][y] == 1:
                        b += 1
                    if board[x][y] == -1:
                        w += 1
            if b > w:
                match = 1
            if b < w:
                match = -1
            if b == w:
                match = 0
            score1.score_str = str(b)
            score2.score_str = str(w)
            for x in range(8):
                for y in range(8):
                    if not is_valid(x, y, 1):
                        check1 += 1
                    if not is_valid(x, y, -1):
                        check2 += 1
            if check1 == 64 and check2 == 64:
                player = 0
            for x in range(8):
                for y in range(8):
                    if (80 + 80 * x < mouse_x < 160 + 80 * x and
                            130 + 80 * y < mouse_y < 210 + 80 * y and board[x][y] == 0):
                        edge = Edge(screen, x, y)
                        edge.blitme()
            for x in range(8):
                for y in range(8):
                    if not is_valid(x, y, player):
                        check += 1
                        if check == 64:
                            player = -player
                            time = pygame.time.get_ticks()
            for x in range(8):
                for y in range(8):
                    if is_valid(x, y, player):
                        yellow_point = Yellow_point(screen, x, y)
                        yellow_point.blitme()
            if player == 0:
                if match == 0:
                    draw.blitme()
                if match == 1:
                    win.black_blitme()
                if match == -1:
                    win.white_blitme()
            if player == 1:
                red_point_black.blitme()
            if player == -1:
                red_point_white.blitme()
                if pygame.time.get_ticks() - time > 1000:
                    # random_AI(player)
                    max_AI(player)
                    # plus_AI(player)
                    player = -player
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for x in range(8):
                        for y in range(8):
                            if 80 + 80 * x < mouse_x < 160 + 80 * x and 130 + 80 * y < mouse_y < 210 + 80 * y:
                                if player == 1:
                                    if is_valid(x, y, player):
                                        down_music.play()
                                        board[x][y] = 1
                                        turn(x, y, player)
                                        player = -1
                                        time = pygame.time.get_ticks()
                                        break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    # if event.key == pygame.K_SPACE:
                    #     for i in range(8):
                    #         for j in range(8):
                    #             print(board[j][i], end="\t")
                    #         print()
                    if event.key == pygame.K_SPACE:
                        game = 0
                if event.type == pygame.QUIT:
                    sys.exit()


run_game()
