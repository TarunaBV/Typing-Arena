import pygame
import sys
from enemy import Enemy
from utils import draw_text
from config import WIDTH, HEIGHT, FPS

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Load Sounds
pygame.mixer.music.set_volume(0.4)

type_sound = pygame.mixer.Sound("assets/sounds/type.wav")
success_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
gameover_sound = pygame.mixer.Sound("assets/sounds/gameover.wav")

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Code Invaders")
clock = pygame.time.Clock()

# Load background
bg_image = pygame.image.load("assets/images/modern_background.png").convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# Fonts (built-in)
font_large = pygame.font.SysFont("arial", 48, bold=True)
font_small = pygame.font.SysFont("arial", 28)

# High Score
high_score = 0
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

# Game States
MENU, PLAYING, GAME_OVER = "menu", "playing", "game_over"
game_state = MENU

# Game variables
enemies = []
score = 0
input_text = ""
spawn_timer = 0
spawn_delay = 2000  # in ms

# Buttons
def draw_button(text, x, y, w, h, active_color, inactive_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    color = active_color if rect.collidepoint(mouse) else inactive_color
    pygame.draw.rect(screen, color, rect, border_radius=12)
    draw_text(screen, text, font_small, (255, 255, 255), rect.centerx, rect.centery)

    if rect.collidepoint(mouse) and click[0] == 1:
        pygame.time.delay(200)
        if action:
            action()

def start_game():
    global game_state, score, enemies, input_text, spawn_timer
    game_state = PLAYING
    score = 0
    input_text = ""
    enemies = []
    spawn_timer = 0

def quit_game():
    pygame.quit()
    sys.exit()

def game_over_screen():
    screen.blit(bg_image, (0, 0))
    draw_text(screen, "Game Over", font_large, (0, 0, 0), WIDTH // 2, HEIGHT // 2 - 100)
    draw_text(screen, f"Final Score: {score}", font_small, (0, 0, 0), WIDTH // 2, HEIGHT // 2 - 40)
    draw_text(screen, f"High Score: {high_score}", font_small, (0, 0, 0), WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Press R to Restart", font_small, (80, 80, 80), WIDTH // 2, HEIGHT // 2 + 60)
    pygame.display.flip()

def menu_screen():
    screen.blit(bg_image, (0, 0))
    draw_text(screen, "Code Invaders", font_large, (0, 0, 0), WIDTH // 2, HEIGHT // 2 - 120)
    draw_button("Start Game", WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 50, (50, 150, 255), (100, 100, 255), start_game)
    draw_button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 50, (255, 80, 80), (200, 80, 80), quit_game)
    pygame.display.flip()

def spawn_enemy():
    new_enemy = Enemy()
    enemies.append(new_enemy)

# Game loop
running = True
while running:
    dt = clock.tick(FPS)
    screen.blit(bg_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
                    type_sound.play()

                for enemy in enemies[:]:
                    if input_text.strip() == enemy.word:
                        enemies.remove(enemy)
                        score += 1
                        success_sound.play()
                        input_text = ""
                        break

        elif game_state == GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_state = MENU

    if game_state == MENU:
        menu_screen()

    elif game_state == PLAYING:
        spawn_timer += dt
        if spawn_timer >= spawn_delay:
            spawn_enemy()
            spawn_timer = 0

        for enemy in enemies[:]:
            enemy.update()
            enemy.draw(screen)
            if enemy.rect.top > HEIGHT:
                game_state = GAME_OVER
                if score > high_score:
                    high_score = score
                    with open("highscore.txt", "w") as f:
                        f.write(str(high_score))
                gameover_sound.play()

        draw_text(screen, f"Type: {input_text}", font_small, (0, 0, 0), WIDTH // 2, HEIGHT - 40)
        draw_text(screen, f"Score: {score}", font_small, (0, 0, 0), WIDTH - 100, 20)
        pygame.display.flip()

    elif game_state == GAME_OVER:
        game_over_screen()
