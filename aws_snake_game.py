import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)

# AWS Service colors (approximated)
EC2_COLOR = (255, 153, 0)  # Orange
S3_COLOR = (76, 175, 80)   # Green
LAMBDA_COLOR = (255, 193, 7)  # Amber

class AWSService:
    def __init__(self, name, color, symbol):
        self.name = name
        self.color = color
        self.symbol = symbol
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)
        self.points = 10

    def draw(self, screen, font):
        # Draw the service icon background
        rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        
        # Draw the service symbol
        text = font.render(self.symbol, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    def respawn(self, snake_body):
        while True:
            self.x = random.randint(0, GRID_WIDTH - 1)
            self.y = random.randint(0, GRID_HEIGHT - 1)
            if (self.x, self.y) not in snake_body:
                break

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Moving right initially
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, direction):
        # Prevent moving in opposite direction
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def check_collision(self):
        head_x, head_y = self.body[0]
        
        # Check wall collision
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            return True
        
        # Check self collision
        if (head_x, head_y) in self.body[1:]:
            return True
        
        return False

    def eat_service(self, service):
        head_x, head_y = self.body[0]
        if head_x == service.x and head_y == service.y:
            self.grow = True
            return True
        return False

    def draw(self, screen):
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if i == 0:  # Head
                pygame.draw.rect(screen, GREEN, rect)
            else:  # Body
                pygame.draw.rect(screen, (0, 200, 0), rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("AWS Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 16)
        self.big_font = pygame.font.Font(None, 48)
        self.score = 0
        self.snake = Snake()
        
        # AWS Services
        self.aws_services = [
            AWSService("EC2", EC2_COLOR, "EC2"),
            AWSService("S3", S3_COLOR, "S3"),
            AWSService("Lambda", LAMBDA_COLOR, "λ")
        ]
        self.current_service = random.choice(self.aws_services)
        self.current_service.respawn(self.snake.body)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))
        return True

    def update(self):
        self.snake.move()
        
        # Check if snake ate AWS service
        if self.snake.eat_service(self.current_service):
            self.score += self.current_service.points
            self.current_service = random.choice(self.aws_services)
            self.current_service.respawn(self.snake.body)
        
        # Check collision
        if self.snake.check_collision():
            return False
        
        return True

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw snake
        self.snake.draw(self.screen)
        
        # Draw current AWS service
        self.current_service.draw(self.screen, self.font)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw current service info
        service_text = self.font.render(f"Collect: {self.current_service.name}", True, WHITE)
        self.screen.blit(service_text, (10, 30))
        
        pygame.display.flip()

    def game_over_screen(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.big_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.big_font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # Instructions
        restart_text = self.font.render("Press SPACE to play again or ESC to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        
        # Wait for input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True  # Restart game
                    elif event.key == pygame.K_ESCAPE:
                        return False  # Quit game
        return False

    def reset(self):
        self.score = 0
        self.snake = Snake()
        self.current_service = random.choice(self.aws_services)
        self.current_service.respawn(self.snake.body)

    def run(self):
        running = True
        game_active = True
        
        while running:
            if game_active:
                running = self.handle_events()
                if running:
                    game_active = self.update()
                    self.draw()
            else:
                # Game over state
                restart = self.game_over_screen()
                if restart:
                    self.reset()
                    game_active = True
                else:
                    running = False
            
            self.clock.tick(10)  # Game speed
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
