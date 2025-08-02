import pygame
import sys
import random
from enemy import Enemy
from utils import draw_text
from config import WIDTH, HEIGHT, FPS
from levels import levels

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Load Sounds
pygame.mixer.music.set_volume(0.4)
type_sound = pygame.mixer.Sound("assets/sounds/type.wav")
success_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
level_complete_sound = pygame.mixer.Sound("assets/sounds/level_complete.wav")
gameover_sound = pygame.mixer.Sound("assets/sounds/gameover.wav")

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Arena")
clock = pygame.time.Clock()

# Load background
bg_image = pygame.image.load("assets/images/modern_background.png").convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# Fonts (built-in)
font_large = pygame.font.SysFont("arial", 48, bold=True)
font_small = pygame.font.SysFont("arial", 28)

# Game States
MENU, PLAYING, LEVEL_COMPLETE, GAME_OVER = "menu", "playing", "level_complete", "game_over"
game_state = MENU

# Game variables
current_level = 0
unlocked_levels = 1
score = 0
input_text = ""
spawn_timer = 0
enemies = []
typed_words = set()
level_words = []

# High Score
high_score = 0
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

def start_level(level_index):
    global game_state, enemies, input_text, spawn_timer, typed_words, level_words, current_level
    current_level = level_index
    input_text = ""
    spawn_timer = 0
    typed_words = set()
    enemies = []
    level_words = levels[current_level]["words"][:]
    game_state = PLAYING

def spawn_enemy():
    global level_words
    if level_words:
        word = random.choice(level_words)
        level_words.remove(word)
        new_enemy = Enemy(word, *levels[current_level]["enemy_speed_range"])
        enemies.append(new_enemy)

def draw_button(text, x, y, w, h, active_color, inactive_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    color = active_color if rect.collidepoint(mouse) else inactive_color
    pygame.draw.rect(screen, color, rect, border_radius=12)
    draw_text(screen, text, font_small, (255, 255, 255), rect.centerx, rect.centery)
    if rect.collidepoint(mouse) and click[0] == 1 and action:
        pygame.time.delay(200)
        action()

def menu_screen():
    screen.blit(bg_image, (0, 0))
    draw_text(screen, "Typing Arena", font_large, (0, 0, 0), WIDTH // 2, 80)

    lock_img = pygame.image.load("assets/images/lock.png").convert_alpha()
    lock_img = pygame.transform.scale(lock_img, (24, 24))

    button_w, button_h = 150, 60
    padding = 40
    cols = 2
    rows = (len(levels) + 1) // 2

    start_x = WIDTH // 2 - (cols * (button_w + padding) - padding) // 2
    start_y = 160

    for i, level in enumerate(levels):
        row = i // cols
        col = i % cols
        x = start_x + col * (button_w + padding)
        y = start_y + row * (button_h + padding)

        rect = pygame.Rect(x, y, button_w, button_h)
        color = (50, 150, 255) if i < unlocked_levels else (160, 160, 160)
        pygame.draw.rect(screen, color, rect, border_radius=12)

        draw_text(screen, level["name"], font_small, (255, 255, 255), rect.centerx, rect.centery)

        if i >= unlocked_levels:
            screen.blit(lock_img, (rect.right - 30, rect.top + 6))
        else:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if rect.collidepoint(mouse) and click[0]:
                pygame.time.delay(200)
                start_level(i)

    pygame.display.flip()

def level_complete_screen():
    screen.blit(bg_image, (0, 0))
    draw_text(screen, "Level Complete!", font_large, (0, 0, 0), WIDTH // 2, HEIGHT // 2 - 80)
    draw_text(screen, "Press N for Next Level or M for Menu", font_small, (0, 0, 0), WIDTH // 2, HEIGHT // 2 + 20)
    pygame.display.flip()

def game_over_screen():
    screen.blit(bg_image, (0, 0))
    draw_text(screen, "Game Over", font_large, (0, 0, 0), WIDTH // 2, HEIGHT // 2 - 40)
    draw_text(screen, "Press R to Restart", font_small, (80, 80, 80), WIDTH // 2, HEIGHT // 2 + 20)
    pygame.display.flip()

def quit_game():
    pygame.quit()
    sys.exit()

# Game loop
running = True
while running:
    dt = clock.tick(FPS)
    screen.blit(bg_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == PLAYING and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
                type_sound.play()
                for enemy in enemies[:]:
                    if input_text.strip() == enemy.word:
                        enemies.remove(enemy)
                        typed_words.add(enemy.word)
                        input_text = ""
                        success_sound.play()
                        break

        elif game_state == LEVEL_COMPLETE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    if current_level + 1 < len(levels):
                        unlocked_levels = max(unlocked_levels, current_level + 2)
                        start_level(current_level + 1)
                    else:
                        game_state = MENU
                elif event.key == pygame.K_m:
                    game_state = MENU

        elif game_state == GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_state = MENU

    if game_state == MENU:
        menu_screen()

    elif game_state == PLAYING:
        spawn_timer += dt
        if spawn_timer >= levels[current_level]["spawn_delay"] and level_words:
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
        draw_text(screen, f"Level: {levels[current_level]['name']}", font_small, (0, 0, 0), 100, 20)
        draw_text(screen, f"Words: {len(typed_words)}/{levels[current_level]['word_count']}", font_small, (0, 0, 0), WIDTH - 130, 20)

        if len(typed_words) >= levels[current_level]["word_count"]:
            level_complete_sound.play()
            game_state = LEVEL_COMPLETE

        pygame.display.flip()

    elif game_state == LEVEL_COMPLETE:
        level_complete_screen()

    elif game_state == GAME_OVER:
        game_over_screen()
