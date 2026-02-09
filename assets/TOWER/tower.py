import pygame
import math
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

# Game variables
clock = pygame.time.Clock()
FPS = 60
money = 100
lives = 10
wave = 0
game_over = False
font = pygame.font.SysFont('Arial', 24)

# Path for enemies (list of points)
path = [
    (0, 300), (100, 300), (100, 100), (400, 100), 
    (400, 500), (700, 500), (700, 300), (800, 300)
]

# Projectile class
class Projectile:
    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 10
        self.damage = damage
        self.radius = 5
        self.color = YELLOW
        
    def update(self):
        # Move toward target
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist < self.speed:  # Reached target
            self.target.health -= self.damage
            return True  # Projectile should be removed
        
        self.x += self.speed * dx / dist
        self.y += self.speed * dy / dist
        return False
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

# Tower class
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.range = 150
        self.damage = 10
        self.cooldown = 30  # frames between attacks
        self.cooldown_counter = 0
        self.color = BLUE
        self.cost = 50
        self.projectiles = []
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        # Draw range circle (transparent)
        range_surface = pygame.Surface((self.range*2, self.range*2), pygame.SRCALPHA)
        pygame.draw.circle(range_surface, (0, 0, 255, 50), (self.range, self.range), self.range)
        surface.blit(range_surface, (self.x - self.range, self.y - self.range))
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(surface)
        
    def attack(self, enemies):
        if self.cooldown_counter <= 0:
            # Find closest enemy in range
            closest_enemy = None
            closest_dist = float('inf')
            
            for enemy in enemies:
                dist = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
                if dist <= self.range and dist < closest_dist:
                    closest_enemy = enemy
                    closest_dist = dist
            
            if closest_enemy:
                self.projectiles.append(Projectile(self.x, self.y, closest_enemy, self.damage))
                self.cooldown_counter = self.cooldown
        else:
            self.cooldown_counter -= 1
            
        # Update projectiles
        for projectile in self.projectiles[:]:
            if projectile.update():  # Returns True if projectile hit target
                self.projectiles.remove(projectile)

# Enemy class
class Enemy:
    def __init__(self, path):
        self.path = path
        self.path_index = 0
        self.x, self.y = path[0]
        self.speed = 2
        self.health = 100
        self.max_health = 100
        self.radius = 15
        self.color = RED
        
    def move(self):
        target_x, target_y = self.path[self.path_index]
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < self.speed:
            self.x = target_x
            self.y = target_y
            self.path_index += 1
        else:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance
            
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # Health bar
        health_ratio = self.health / self.max_health
        pygame.draw.rect(surface, RED, (self.x - self.radius, self.y - self.radius - 10, 
                                        self.radius * 2, 5))
        pygame.draw.rect(surface, GREEN, (self.x - self.radius, self.y - self.radius - 10, 
                                         self.radius * 2 * health_ratio, 5))
        
    def is_at_end(self):
        return self.path_index >= len(self.path)

# Game objects
towers = []
enemies = []
selected_tower_pos = None
wave_cooldown = 0

def draw_path():
    for i in range(len(path) - 1):
        pygame.draw.line(screen, GRAY, path[i], path[i+1], 5)

def spawn_wave():
    global wave, wave_cooldown
    wave += 1
    for _ in range(5 + wave * 2):
        enemies.append(Enemy(path))
    wave_cooldown = 300  # 5 seconds at 60 FPS

def draw_ui():
    money_text = font.render(f"Money: ${money}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    wave_text = font.render(f"Wave: {wave}", True, BLACK)
    
    screen.blit(money_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    screen.blit(wave_text, (10, 70))
    
    # Draw tower cost
    tower_cost_text = font.render(f"Tower Cost: $50 (Click to place)", True, BLACK)
    screen.blit(tower_cost_text, (SCREEN_WIDTH - 250, 10))

# Main game loop
running = True
while running:
    clock.tick(FPS)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if we can place a tower here
            if money >= 50:
                # Simple check to prevent towers on path (this could be improved)
                on_path = False
                for i in range(len(path) - 1):
                    x1, y1 = path[i]
                    x2, y2 = path[i+1]
                    # Simple line-point distance check (could be more accurate)
                    if (min(x1, x2) <= mouse_x <= max(x1, x2) and min(y1, y2) <= mouse_y <= max(y1, y2)):
                        on_path = True
                        break
                
                if not on_path:
                    towers.append(Tower(mouse_x, mouse_y))
                    money -= 50
    
    if game_over:
        # Game over screen
        screen.fill(WHITE)
        game_over_text = font.render("GAME OVER", True, RED)
        restart_text = font.render("Press R to restart", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 70, SCREEN_HEIGHT//2 - 20))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 20))
        
        keys = pygame.key.get_pressed()
        if keys[K_r]:
            # Reset game
            towers = []
            enemies = []
            money = 100
            lives = 10
            wave = 0
            game_over = False
    else:
        # Game logic
        if wave_cooldown > 0:
            wave_cooldown -= 1
        elif not enemies:  # No enemies left
            spawn_wave()
        
        # Update enemies
        for enemy in enemies[:]:
            enemy.move()
            if enemy.is_at_end():
                enemies.remove(enemy)
                lives -= 1
                if lives <= 0:
                    game_over = True
            elif enemy.health <= 0:
                enemies.remove(enemy)
                money += 10
        
        # Update towers
        for tower in towers:
            tower.attack(enemies)
        
        # Drawing
        screen.fill(WHITE)
        draw_path()
        
        for tower in towers:
            tower.draw(screen)
        
        for enemy in enemies:
            enemy.draw(screen)
        
        draw_ui()
    
    pygame.display.flip()

pygame.quit()
