import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
BALL_RADIUS = 20
ROD_WIDTH = 10
ROD_HEIGHT = 200
SPACING = 100
ALL_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]  # Red, Green, Blue, Yellow, Orange
NUM_RODS = 5
BALLS_PER_ROD = 5
CONFETTI_COUNT = 100

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Sorting Game")

# Font
font = pygame.font.Font(None, 36)

# Confetti effect
class Confetti:
    def __init__(self):
        self.particles = []

    def generate(self):
        self.particles = [
            [random.randint(0, WIDTH), random.randint(0, HEIGHT), random.choice(ALL_COLORS), random.randint(-3, 3), random.randint(1, 5)]
            for _ in range(CONFETTI_COUNT)
        ]

    def draw(self, screen):
        for p in self.particles:
            pygame.draw.circle(screen, p[2], (p[0], p[1]), 5)
            p[1] -= p[4]  # Move confetti upwards

confetti = Confetti()

# Rod class
class Rod:
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT // 2
        self.balls = []

    def draw(self, screen):
        pygame.draw.rect(screen, (150, 75, 0), (self.x, self.y, ROD_WIDTH, ROD_HEIGHT))
        for i, ball in enumerate(self.balls):
            pygame.draw.circle(screen, ball, (self.x + ROD_WIDTH // 2, self.y + ROD_HEIGHT - (i + 1) * (BALL_RADIUS * 2)), BALL_RADIUS)

    def add_ball(self, color):
        if len(self.balls) < BALLS_PER_ROD:
            self.balls.append(color)
            return True
        return False

    def remove_ball(self):
        return self.balls.pop() if self.balls else None

    def is_uniform(self):
        return len(set(self.balls)) <= 1  # All balls same color or empty

def setup_game():
    global rods, COLORS, win_message

    # Randomly choose 4 colors per session
    COLORS = random.sample(ALL_COLORS, 4)

    # Create rods
    rods = [Rod(SPACING + i * 100) for i in range(NUM_RODS)]

    # Ensure at least one empty rod
    filled_rods = rods[:-1]

    # Distribute exactly 5 of each color
    balls = [color for color in COLORS for _ in range(5)]
    random.shuffle(balls)

    # Assign shuffled balls to rods
    ball_index = 0
    for rod in filled_rods:
        for _ in range(BALLS_PER_ROD):
            rod.add_ball(balls[ball_index])
            ball_index += 1

    win_message = False
    confetti.particles = []  # Reset confetti

setup_game()

selected_ball = None
selected_rod = None
selected_ball_pos = None

# Game loop
running = True
while running:
    screen.fill((200, 200, 200))

    # Check for win condition
    if all(rod.is_uniform() and (len(rod.balls) == BALLS_PER_ROD or len(rod.balls) == 0) for rod in rods):
        win_message = True
        confetti.generate()
        text = font.render("You Win!", True, (0, 255, 0))
        screen.blit(text, (WIDTH // 2 - 50, HEIGHT // 4))

        # New Game button
        button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2, 120, 50)
        pygame.draw.rect(screen, (0, 200, 0), button_rect)
        button_text = font.render("New Game", True, (255, 255, 255))
        screen.blit(button_text, (WIDTH // 2 - 50, HEIGHT // 2 + 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if win_message:
                if button_rect.collidepoint(event.pos):  # Restart game if button is clicked
                    setup_game()
                    continue
            else:
                for rod in rods:
                    if rod.x <= event.pos[0] <= rod.x + ROD_WIDTH and rod.balls:
                        selected_ball = rod.remove_ball()
                        selected_rod = rod
                        selected_ball_pos = event.pos
                        break
        elif event.type == pygame.MOUSEBUTTONUP and selected_ball:
            for rod in rods:
                if rod.x <= event.pos[0] <= rod.x + ROD_WIDTH:
                    if rod.add_ball(selected_ball):
                        selected_ball = None
                        selected_rod = None
                        selected_ball_pos = None
                    else:
                        selected_rod.add_ball(selected_ball)
                        selected_ball = None
                        selected_rod = None
                        selected_ball_pos = None
                    break
            if selected_ball:
                selected_rod.add_ball(selected_ball)
                selected_ball = None
                selected_rod = None
                selected_ball_pos = None

    # Draw rods and balls
    for rod in rods:
        rod.draw(screen)

    # If a ball is being moved, draw it at the current mouse position
    if selected_ball and selected_ball_pos:
        pygame.draw.circle(screen, selected_ball, selected_ball_pos, BALL_RADIUS)

    # Draw confetti if the player wins
    if win_message:
        confetti.draw(screen)

    pygame.display.flip()

pygame.quit()
