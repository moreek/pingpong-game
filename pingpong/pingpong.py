import pygame
import sys
import math
import time

class Ball(object):
    def __init__(self, x, y, width, height, vx, vy, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx
        self.vy = vy
        self.color = color

    def render(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

    def update(self):
        self.x += self.vx
        self.y += self.vy

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Board1(object):
    def __init__(self, x, y, width, height, speed, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vy = 0
        self.speed = speed
        self.color = color

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        self.y += self.vy

    def key_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.vy = -self.speed
            elif event.key == pygame.K_DOWN:
                self.vy = self.speed
        elif event.key in (pygame.K_DOWN, pygame.K_UP):
                self.vy = 0

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Board2(object):
    def __init__(self, x, y, width, height, speed, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vy = 0
        self.speed = speed
        self.color = color

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        self.y += self.vy

    def key_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.vy = -self.speed
            elif event.key == pygame.K_s:
                self.vy = self.speed
        elif event.key in (pygame.K_w, pygame.K_s):
                self.vy = 0

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Pong(object):
    COLORS = {"BLACK": (  0,   0,   0), "WHITE": (255, 255, 255), "BLUE": (63, 255, 255)}
    def __init__(self):
        pygame.init()
        (WIDTH, HEIGHT) = (900, 500)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ping' Pong")
        self.ball = Ball(5, 5, 25, 25, 5, 5, Pong.COLORS["BLUE"])
        self.board1 = Board1(WIDTH - 50, HEIGHT / 2, 10, 100, 3, Pong.COLORS["BLUE"])
        self.board2 = Board2(WIDTH - 850, HEIGHT / 2, 10, 100, 3, Pong.COLORS["BLUE"])
        self.score1 = 0
        self.score2 = 0
        self.flag = 0

    def reset_all(self):
        self.ball.x = 433
        self.ball.y = 250
        self.ball.width = 25
        self.ball.height = 25
        self.ball.vx = 5
        self.ball.vy = 5

        self.board1.x = 850
        self.board1.y = 200
        self.board1.vy = 0
        self.board2.x = 50
        self.board2.y = 200
        self.board2.vy = 0

    def endFalg(self, eFlag):
        self.endflag = eFlag

    def setFlag(self, nFlag):
        self.flag = nFlag

    def play(self): #메인실행
        clock = pygame.time.Clock()
        while True:
            clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                    self.board1.key_handler(event)
                    self.board2.key_handler(event)
            if self.flag == 1:
                self.collision_handler()
                self.draw()
            if self.flag == 0:
                if self.endflag == 0:
                    time.sleep(5)
                    pygame.quit()
                    sys.exit()
                self.reset_all()
                self.draw()
                time.sleep(1)
                self.flag = 1

    def winner(self):
        font = pygame.font.Font(None, 100)
        if self.score1 == 10:
            P1win = font.render("P1 Win!", True, Pong.COLORS["BLUE"])
            self.screen.blit(P1win, (350, 200))
        if self.score2 == 10:
            P2win = font.render("P2 Win!", True, Pong.COLORS["BLUE"])
            self.screen.blit(P2win, (350, 200))

    def collision_handler(self):
        if self.ball.rect.colliderect(self.board1.rect): #보드튕김(오른쪽)
            self.ball.vx = -self.ball.vx
        if self.ball.rect.colliderect(self.board2.rect): #보드튕김(왼쪽)
            self.ball.vx = -self.ball.vx

        if self.ball.x + self.ball.width >= self.screen.get_width(): #오른쪽
            self.score1 += 1
            self.flag = 0
        elif self.ball.x <= 0: #왼쪽
            self.score2 += 1
            self.flag = 0
        if self.ball.y + self.ball.height >= self.screen.get_height():  #아래
            self.ball.vy = -self.ball.vy
        elif self.ball.y <= 0: #위
            self.ball.vy = math.fabs(self.ball.vy)

        if self.board1.y + self.board1.height >= self.screen.get_height():
            self.board1.y = self.screen.get_height() - self.board1.height
        elif self.board1.y <= 0: #보드1 위치 제어
            self.board1.y = 0
        if self.board2.y + self.board2.height >= self.screen.get_height():
            self.board2.y = self.screen.get_height() - self.board2.height
        elif self.board2.y <= 0: #보드2 위치 제어
            self.board2.y = 0

    def draw(self):
        self.screen.fill(Pong.COLORS["BLACK"])

        font = pygame.font.Font(None, 60)
        score_text1 = font.render("P1: " + str(self.score1), True, Pong.COLORS["WHITE"])
        score_text2 = font.render("P2: " + str(self.score2), True, Pong.COLORS["WHITE"])
        pygame.draw.line(self.screen, pygame.color.Color(255, 255, 255), (450, 0), (450, 500), 1)
        self.screen.blit(score_text1, (300, 0))
        self.screen.blit(score_text2, (510, 0))

        self.ball.update()
        self.ball.render(self.screen)
        self.board1.update()
        self.board1.render(self.screen)
        self.board2.update()
        self.board2.render(self.screen)

        if self.score1 == 10  or self.score2 == 10:
            self.winner()
            self.endflag = 0

        pygame.display.update()

if __name__ == "__main__":
    #Pong().play()
    objPong = Pong()
    objPong.setFlag(1)
    objPong.endFalg(1)
    objPong.play()
