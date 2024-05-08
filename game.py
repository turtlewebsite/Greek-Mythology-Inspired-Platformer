
import pygame
import sys
import random
# python -m PyInstaller main.py.py
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,102)
FPS = 60

# Player properties
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_COLOR = BLUE
PLAYER_JUMP_POWER = 28
PLAYER_GRAVITY = 1

# Platform properties
PLATFORM_COLOR = GREEN
PLATFORMS = [
    (WIDTH / 6 - 50, HEIGHT * 3 / 4, 100, 20),
    (WIDTH / 3 - 50, HEIGHT / 2, 100, 20),
    (WIDTH / 2 - 50, HEIGHT / 4, 100, 20),
    (WIDTH / 3 * 2 - 50, HEIGHT / 2, 100, 20),
    (WIDTH / 6 * 5 - 50, HEIGHT * 3 / 4, 100, 20)             
]
START_SCREEN = 0
GAME_SCREEN = 1
GAME_OVER_SCREEN = 2
state = START_SCREEN
font = pygame.font.Font(None, 36)
# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")
clock = pygame.time.Clock()
background_image = pygame.image.load(r"C:\Users\skb20\OneDrive\Documents\Greek Mythology\Images\background.png").convert()
# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\skb20\OneDrive\Documents\Greek Mythology\Images\bolt.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 15 * direction # Bullet speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH or self.rect.left < 0:  # Remove bullet if it goes off-screen
            self.kill()
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\skb20\OneDrive\Documents\Greek Mythology\Images\spear.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 15 * direction # Bullet speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH or self.rect.left < 0:  # Remove bullet if it goes off-screen
            self.kill()
# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_left = pygame.image.load(r"C:\Users\skb20\OneDrive\Documents\Greek Mythology\Images\file.png").convert_alpha()
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, PLAYER_GRAVITY)
        self.on_ground = False
        self.last_shoot_time = 0
        self.shoot_delay = 400  # 1 second (in milliseconds)
        self.bullets = pygame.sprite.Group()  # Group to manage bullets
        self.health = 100  # Player's initial health
        self.max_health = 100  # Player's maximum health

    def update(self):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity.x = -5
            self.image = self.image_left
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = 5
            self.image = self.image_right
        else:
            self.velocity.x = 0

        # Jump if on the ground and up arrow key is pressed
        if self.on_ground and keys[pygame.K_UP]:
            self.jump()

        # Shoot if spacebar is pressed and enough time has passed since the last shot
        if keys[pygame.K_SPACE] and current_time - self.last_shoot_time > self.shoot_delay:
            self.shoot()
            self.last_shoot_time = current_time

        self.velocity += self.acceleration
        self.rect.x += self.velocity.x
        self.check_collision_x()

        self.rect.y += self.velocity.y
        self.on_ground = False
        self.check_collision_y()

        # Update bullets
        self.bullets.update()

    def jump(self):
        if self.on_ground:
            self.velocity.y = -PLAYER_JUMP_POWER
            self.on_ground = False

    def shoot(self):
        if self.image == self.image_right:
            bullet = Bullet(self.rect.right, self.rect.centery, 1)  # Direction 1 for right
        else:
            bullet = Bullet(self.rect.left, self.rect.centery, -1)  # Direction -1 for left
        self.bullets.add(bullet)

    def check_collision_x(self):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0:
                    self.rect.left = platform.rect.right

    def check_collision_y(self):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0:
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.velocity.y = 0  # Stop downward velocity when on the ground
                elif self.velocity.y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0
        if self.rect.bottom > HEIGHT- 30:
            self.rect.bottom = HEIGHT - 30
            self.on_ground = True
            self.velocity.y = 0
    # Check if the player is on the ground
        if not self.on_ground:
            self.velocity.y += self.acceleration.y
    def draw_health_bar(self, surface):
       health_bar_width = int((self.health / self.max_health) * 100)
       if health_bar_width < 0:
           health_bar_width = 0
       pygame.draw.rect(surface, (0, 0, 0), (10, HEIGHT - 30, 104, 14), 3)
       pygame.draw.rect(surface, (0, 255, 0), (12, HEIGHT - 28, health_bar_width, 10))
       pygame.draw.rect(surface, (255, 0, 0), (12 + health_bar_width, HEIGHT - 28, 100 - health_bar_width, 10))
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\skb20\OneDrive\Documents\Greek Mythology\Images\cronos4.png").convert_alpha()  # Placeholder surface for enemy image

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 70, HEIGHT / 2 + 50)  # Start position on the right side
        self.speed = 5  # Vertical movement speed
        self.direction = 1  # 1 for moving down, -1 for moving up
        self.shoot_delay = 700  # 2 seconds (in milliseconds)
        self.last_shoot_time = 0
        self.bullets = pygame.sprite.Group()  # Group to manage enemy bullets
        self.health = 100  # Enemy's initial health
        self.max_health = 100  # Enemy's maximum health

    def update(self):
        # Move up and down
        self.rect.y += self.speed * self.direction
        # Randomly change direction if hitting top or bottom or based on a chance
        if self.rect.bottom >= HEIGHT - 50 or self.rect.top <= 0 or random.random() < 0.02:
            self.direction *= random.choice([-1, 1])  # Change direction randomly

        # Ensure the enemy stays within the screen boundaries
        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.direction = -1  # Move upwards if hitting the bottom
        elif self.rect.top <= 0:
            self.rect.top = 0
            self.direction = 1  # Move downwards if hitting the top

        # Shoot bullets
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time > self.shoot_delay:
            self.shoot()
            self.last_shoot_time = current_time

        # Update bullets
        self.bullets.update()

    def shoot(self):
        bullet = EnemyBullet(self.rect.left, self.rect.centery, -1)  # Shoot towards the left
        self.bullets.add(bullet)
    def draw_health_bar(self, surface):
        # Calculate width of health bar based on enemy's health
        health_bar_width = int((self.health / self.max_health) * 100)
        if health_bar_width < 0:
            health_bar_width = 0
        # Draw the health bar at the bottom of the screen with a black outline
        pygame.draw.rect(surface, (0, 0, 0), (WIDTH - 114, HEIGHT - 30, 104, 14), 3)  # Black outline
        pygame.draw.rect(surface, (0, 255, 0), (WIDTH - 112, HEIGHT - 28, health_bar_width, 10))  # Green portion
        pygame.draw.rect(surface, (255, 0, 0), (WIDTH - 112 + health_bar_width, HEIGHT - 28, 100 - health_bar_width, 10))

class BouncingWeapon(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y):
        super().__init__()
        self.original_image = pygame.image.load(r"C:\Users\skb20\OneDrive\Documents\Greek Mythology\Images\sit2.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = speed_x + 2  # Speed of the weapon in the x direction
        self.speed_y = speed_y + 2 # Speed of the weapon in the y direction
        self.angle = 0
        self.angular_speed = -3 
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.angle += self.angular_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # Reverse direction if the weapon hits the screen edges
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT-50:
            self.speed_y *= -1

    def collide_player(self, player):
        # Check collision with the player
        if self.rect.colliderect(player.rect):
            player.health -= 2  # Decrease player's health upon collision
            self.kill()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\skb20\OneDrive\Documents\Greek Mythology\Images\cloud.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (width, height))  # Scale the image to the desired width and height
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Ensure crop_rect is within the dimensions of the loaded image
        #crop_rect = pygame.Rect(0, 0, width, height)
        #self.image = self.image.subsurface(crop_rect)
        #self.image = pygame.Surface((width, height))
        #self.image.fill(PLATFORM_COLOR)
# Create player and enemy object
player = Player()
enemy = Enemy()
weapon = BouncingWeapon(WIDTH  - 100 , HEIGHT  - 100, 3, 3)
weapon1 = BouncingWeapon(WIDTH // 4, HEIGHT // 4, 3, 3)
# Create platform objects
platforms = pygame.sprite.Group()
for plat in PLATFORMS:
    platform = Platform(*plat)
    platforms.add(platform)

# Main game loop
running = True
end = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #elif event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_UP:
        #        player.jump()

    # Update
    if state == START_SCREEN:
        screen.fill(BLACK)
        start_text = font.render("Press SPACE to start. Arrow keys for movement, SPACE to shoot.", True, WHITE)
        start_rect = start_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(start_text, start_rect)
        pygame.display.flip()

        # Switch to game screen if SPACE is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            state = GAME_SCREEN
    elif state == GAME_SCREEN:        
        if end:
            player.update()
            enemy.update()
            weapon.update()
            weapon1.update()

            if pygame.sprite.spritecollide(player, enemy.bullets, True):
                player.health -= 10
            if pygame.sprite.spritecollide(enemy, player.bullets, True):
                enemy.health -= 10
            if player.health <= 0 or enemy.health <= 0:
                state = GAME_OVER_SCREEN
                end  = False

            weapon.collide_player(player)
            weapon1.collide_player(player)
            # Draw
            screen.fill(WHITE)
            screen.blit(background_image, (0, 0))
            platforms.draw(screen)
            screen.blit(weapon.image, weapon.rect)
            screen.blit(weapon1.image, weapon1.rect)
            screen.blit(player.image, player.rect)
            player.bullets.draw(screen)  # Draw player bullets
            screen.blit(enemy.image, enemy.rect)
            enemy.bullets.draw(screen)  # Draw enemy bullets
            player.draw_health_bar(screen)
            enemy.draw_health_bar(screen)

            # Update display
            pygame.display.flip()

        # Cap the frame rate
    elif state == GAME_OVER_SCREEN:
        screen.fill(BLACK)
        if (player.health < enemy.health):
            game_over_text = font.render("The Titans got you!", True, WHITE)
        else:
            game_over_text = font.render("Congrats on taking Olympus!", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
