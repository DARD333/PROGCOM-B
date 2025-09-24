import random
import pygame
import sys

# Inicializar pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aprende Colores y Números en Inglés")

# Colores básicos
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (0, 255, 255),  # Cyan
    (255, 192, 203),# Pink
    (0, 0, 0),      # Black
    (255, 255, 255) # White
]
COLOR_NAMES = [
    "Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Cyan", "Pink", "Black", "White"
]

# Fuente
font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont('Arial', 28)

# Estados del juego
MODE_COLOR = 0
MODE_NUMBER = 1


def draw_text(text, y, color=(0,0,0)):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH//2, y))
    screen.blit(surf, rect)

def color_game():
    color_idx = random.randint(0, len(COLORS)-1)
    color = COLORS[color_idx]
    color_name = COLOR_NAMES[color_idx]
    options = random.sample(COLOR_NAMES, 3)
    if color_name not in options:
        options[random.randint(0,2)] = color_name
    else:
        options = list(set(options + [color_name]))[:3]
    random.shuffle(options)
    return color, color_name, options

def number_game():
    number = random.randint(1, 100)
    options = [number]
    while len(options) < 3:
        n = random.randint(1, 100)
        if n not in options:
            options.append(n)
    random.shuffle(options)
    return number, options

def main():
    mode = MODE_COLOR
    score = 0
    running = True
    color, color_name, color_options = color_game()
    number, number_options = number_game()
    feedback = ""
    while running:
        screen.fill((240, 240, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mode = MODE_NUMBER if mode == MODE_COLOR else MODE_COLOR
                    feedback = ""
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    idx = event.key - pygame.K_1
                    if mode == MODE_COLOR:
                        if color_options[idx] == color_name:
                            score += 1
                            feedback = "Correct!"
                        else:
                            feedback = f"Wrong! It was {color_name}"
                        color, color_name, color_options = color_game()
                    else:
                        if number_options[idx] == number:
                            score += 1
                            feedback = "Correct!"
                        else:
                            feedback = f"Wrong! It was {number}"
                        number, number_options = number_game()
        # Mostrar instrucciones
        draw_text("Press SPACE to switch mode", 40, (80,80,80))
        draw_text(f"Score: {score}", 90, (80,80,80))
        if mode == MODE_COLOR:
            draw_text("What color is this?", 160)
            pygame.draw.rect(screen, color, (WIDTH//2-75, 200, 150, 150))
            for i, opt in enumerate(color_options):
                draw_text(f"{i+1}. {opt}", 400 + i*50)
        else:
            draw_text("What number is this in English?", 160)
            draw_text(str(number), 250, (0,0,180))
            for i, opt in enumerate(number_options):
                draw_text(f"{i+1}. {opt}", 400 + i*50)
        if feedback:
            draw_text(feedback, 550, (0,120,0) if feedback.startswith("Correct") else (180,0,0))
        pygame.display.flip()
        pygame.time.wait(50)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
