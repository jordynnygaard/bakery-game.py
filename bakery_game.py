import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bakery Collector")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
WHITE = (255, 255, 255)
player_size = 40
enemy_size = 40
item_size = 30
powerup_size = 35
chef_img = pygame.image.load("chef.png")
chef_img = pygame.transform.scale(chef_img, (player_size, player_size))
enemy_img = pygame.image.load("rat.png")
enemy_img = pygame.transform.scale(enemy_img, (enemy_size, enemy_size))
bread_img = pygame.image.load("bread.png")
bread_img = pygame.transform.scale(bread_img, (item_size, item_size))
cupcake_img = pygame.image.load("cupcake.png")
cupcake_img = pygame.transform.scale(cupcake_img, (powerup_size, powerup_size))
collect_sound = None
hit_sound = None
try:
    collect_sound = pygame.mixer.Sound("collect.wav")
    hit_sound = pygame.mixer.Sound("hit.wav")
except:
    print("Sound files not found, continuing without sound.")
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
enemy_x, enemy_y = random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size)
enemy_speed = 3
items = [(random.randint(0, WIDTH - item_size), random.randint(0, HEIGHT - item_size)) for _ in range(5)]
powerup = (random.randint(0, WIDTH - powerup_size), random.randint(0, HEIGHT - powerup_size))
score = 0
lives = 3
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player_x -= player_speed
    if keys[pygame.K_RIGHT]: player_x += player_speed
    if keys[pygame.K_UP]: player_y -= player_speed
    if keys[pygame.K_DOWN]: player_y += player_speed
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))
    enemy_x += enemy_speed
    if enemy_x <= 0 or enemy_x >= WIDTH - enemy_size:
        enemy_speed = -enemy_speed
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)
    powerup_rect = pygame.Rect(powerup[0], powerup[1], powerup_size, powerup_size)
    new_items = []
    for (ix, iy) in items:
        item_rect = pygame.Rect(ix, iy, item_size, item_size)
        if player_rect.colliderect(item_rect):
            score += 1
            if collect_sound: collect_sound.play()
            new_items.append((random.randint(0, WIDTH - item_size), random.randint(0, HEIGHT - item_size)))
        else:
            new_items.append((ix, iy))
    items = new_items
    if score % 10 == 0 and score > 0:
        enemy_speed = 3 + (score // 10)
    if player_rect.colliderect(enemy_rect):
        lives -= 1
        if hit_sound: hit_sound.play()
        player_x, player_y = WIDTH // 2, HEIGHT // 2
        if lives <= 0:
            screen.fill(WHITE)
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH//2 - 80, HEIGHT//2))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()
    if player_rect.colliderect(powerup_rect):
        lives += 1
        powerup = (random.randint(0, WIDTH - powerup_size), random.randint(0, HEIGHT - powerup_size))
    screen.fill(WHITE)
    screen.blit(chef_img, player_rect)
    screen.blit(enemy_img, enemy_rect)
    for (ix, iy) in items:
        screen.blit(bread_img, (ix, iy))
    screen.blit(cupcake_img, powerup)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    pygame.display.flip()
    clock.tick(30)