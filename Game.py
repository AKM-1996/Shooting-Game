import pygame
import random
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")

clock = pygame.time.Clock()

# Colors
WHITE = (255,255,255)
RED = (255,0,0)
CYAN = (0,255,255)
YELLOW = (255,255,0)
GREEN = (0,255,0)
ORANGE = (255,165,0)

# Player
player = pygame.Rect(WIDTH//2, HEIGHT-60, 40, 40)
gun_type = "normal"
gun_timer = 0

# Lists
bullets = []
enemies = []
powerups = []

score = 0
font = pygame.font.SysFont(None, 30)

# Functions
def shoot():
    if gun_type == "normal":
        bullets.append(pygame.Rect(player.centerx, player.y, 5, 10))
    elif gun_type == "spread":
        bullets.append(pygame.Rect(player.centerx-10, player.y, 5, 10))
        bullets.append(pygame.Rect(player.centerx, player.y, 5, 10))
        bullets.append(pygame.Rect(player.centerx+10, player.y, 5, 10))
    elif gun_type == "rapid":
        for i in range(5):
            bullets.append(pygame.Rect(player.centerx, player.y - i*5, 5, 10))

def spawn_enemy():
    enemies.append(pygame.Rect(random.randint(0, WIDTH-40), 0, 40, 40))

def spawn_powerup():
    types = ["spread", "rapid"]
    powerups.append({
        "rect": pygame.Rect(random.randint(0, WIDTH-20), 0, 20, 20),
        "type": random.choice(types)
    })

enemy_timer = 0
power_timer = 0

# Game Loop
while True:
    screen.fill((10,10,30))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot()
    
    # Movement
    mouse_x = pygame.mouse.get_pos()[0]
    player.x = mouse_x - player.width//2
    
    # Spawn enemies
    enemy_timer += 1
    if enemy_timer > 60:
        spawn_enemy()
        enemy_timer = 0
    
    # Spawn powerups
    power_timer += 1
    if power_timer > 300:
        spawn_powerup()
        power_timer = 0
    
    # Update bullets
    for b in bullets[:]:
        b.y -= 7
        if b.y < 0:
            bullets.remove(b)
    
    # Update enemies
    for e in enemies[:]:
        e.y += 3
        
        if e.y > HEIGHT:
            print("Game Over! Score:", score)
            pygame.quit()
            sys.exit()
        
        for b in bullets[:]:
            if e.colliderect(b):
                enemies.remove(e)
                bullets.remove(b)
                score += 1
                break
    
    # Update powerups
    for p in powerups[:]:
        p["rect"].y += 2
        
        if p["rect"].colliderect(player):
            gun_type = p["type"]
            gun_timer = pygame.time.get_ticks()
            powerups.remove(p)
    
    # Reset gun after 5 sec
    if gun_type != "normal":
        if pygame.time.get_ticks() - gun_timer > 5000:
            gun_type = "normal"
    
    # Draw player
    pygame.draw.rect(screen, CYAN, player)
    
    # Draw bullets
    for b in bullets:
        pygame.draw.rect(screen, YELLOW, b)
    
    # Draw enemies
    for e in enemies:
        pygame.draw.rect(screen, RED, e)
    
    # Draw powerups
    for p in powerups:
        color = GREEN if p["type"] == "spread" else ORANGE
        pygame.draw.rect(screen, color, p["rect"])
    
    # UI
    text = font.render(f"Score: {score} | Gun: {gun_type}", True, WHITE)
    screen.blit(text, (10,10))
    
    pygame.display.flip()
    clock.tick(60)