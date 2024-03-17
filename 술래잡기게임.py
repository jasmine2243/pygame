import pygame
import random
import sys

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("술래잡기 게임")

# 색깔 설정
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y, speed):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def update(self):
        pass

# 플레이어 그룹 생성
all_players = pygame.sprite.Group()

# 술래와 도망자 생성 (도망자 속도: 0.1, 술래 속도: 8)
runner = Player(RED, 0, 0, 0.001)
chaser = Player(BLUE, 400, 300, 8)

all_players.add(runner)
all_players.add(chaser)

# 게임 루프
running = True
clock = pygame.time.Clock()
while running:
    SCREEN.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        chaser.move_left()
    if keys[pygame.K_RIGHT]:
        chaser.move_right()
    if keys[pygame.K_UP]:
        chaser.move_up()
    if keys[pygame.K_DOWN]:
        chaser.move_down()

    # 도망자가 화면 경계에 닿으면 멈춤
    if runner.rect.left <= 0:
        runner.rect.left = 0
    elif runner.rect.right >= WIDTH:
        runner.rect.right = WIDTH
    if runner.rect.top <= 0:
        runner.rect.top = 0
    elif runner.rect.bottom >= HEIGHT:
        runner.rect.bottom = HEIGHT

    # 도망자가 술래에게 잡히면 재시작
    if pygame.sprite.spritecollide(chaser, all_players, False):
        runner.rect.x = random.randint(0, WIDTH)
        runner.rect.y = random.randint(0, HEIGHT)

    all_players.draw(SCREEN)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
