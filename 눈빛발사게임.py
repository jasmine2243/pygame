import pygame
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("눈빛 발사 게임")

# 색깔 설정
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        laser = Laser(self.rect.centerx, self.rect.top)
        all_sprites.add(laser)
        lasers.add(laser)

# 적 클래스
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 8)

# 레이저 클래스
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -20  # 이동 속도를 더 빠르게 설정합니다.

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()



# 그룹 설정
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
lasers = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# 적 생성
for _ in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# 게임 루프
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    # 레이저와 적 충돌 체크
    hits = pygame.sprite.groupcollide(enemies, lasers, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # 플레이어와 적 충돌 체크
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False

    SCREEN.fill((0, 0, 0))
    all_sprites.draw(SCREEN)
    pygame.display.flip()

pygame.quit()
