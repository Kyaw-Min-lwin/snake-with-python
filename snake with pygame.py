import pygame
import random


class SnakeGame:
    def __init__(self):
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 690, 690
        self.PURPLE = (150, 0, 255)
        self.FPS = 15
        self.snake_width, self.snake_height = 30, 30
        self.apple_width, self.apple_height = 30, 30
        self.constant = 0.1
        self.velocity = 0.1

        # Variables
        self.continuous_move_x, self.continuous_move_y = 0, 0
        self.snake_body = []

        # Pygame window setup
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake game")
        self.apple = pygame.image.load("apple.png")
        self.apple = pygame.transform.scale(
            self.apple, (self.apple_width, self.apple_height)
        )

    def draw(self):
        self.WIN.fill(self.PURPLE)
        for rect in self.snake_body:
            pygame.draw.rect(self.WIN, "green", rect)
        self.WIN.blit(self.apple, self.apple_rect)
        pygame.display.update()

    def append_snake_part(self, x, y):
        self.snake_body.append(pygame.Rect(x, y, self.snake_width, self.snake_height))

    def snake_movement(self, keys_pressed):
        if len(self.snake_body) != 1:
            self.snake_body.pop(0)
        if keys_pressed[pygame.K_LEFT]:
            x, y = self.snake_body[-1].x - self.snake_width, self.snake_body[-1].y
            self.append_snake_part(x, y)
            self.continuous_move_x = -self.constant
            self.continuous_move_y = 0
        if keys_pressed[pygame.K_RIGHT]:
            x, y = self.snake_body[-1].x + self.snake_width, self.snake_body[-1].y
            self.append_snake_part(x, y)
            self.continuous_move_x = self.constant
            self.continuous_move_y = 0
        if keys_pressed[pygame.K_UP]:
            x, y = self.snake_body[-1].x, self.snake_body[-1].y - self.snake_height
            self.append_snake_part(x, y)
            self.continuous_move_x = 0
            self.continuous_move_y = -self.constant
        if keys_pressed[pygame.K_DOWN]:
            x, y = self.snake_body[-1].x, self.snake_body[-1].y + self.snake_height
            self.append_snake_part(x, y)
            self.continuous_move_x = 0
            self.continuous_move_y = self.constant


    def place_apple(self):
        random_x = random.randint(0, self.WIDTH - self.apple_width)
        random_y = random.randint(0, self.HEIGHT - self.apple_height)
        self.apple_rect.x, self.apple_rect.y = random_x, random_y

    def check_collision(self):
        x, y = self.snake_body[-1].x, self.snake_body[-1].y
        if self.snake_body[-1].colliderect(self.apple_rect):
            self.place_apple()
            self.append_snake_part(x - self.snake_width, y)

    def game_over(self):
        if (
            self.snake_body[-1].x < 0
            or self.snake_body[-1].x > self.WIDTH
            or self.snake_body[-1].y < 0
            or self.snake_body[-1].y > self.HEIGHT
        ):
            self.continuous_move_x, self.continuous_move_y = 0, 0
            self.velocity, self.constant = 0, 0
            font = pygame.font.Font("freesansbold.ttf", 32)
            text = font.render("You lost", True, (0, 20, 0))
            text_rect = text.get_rect()
            text_rect.center = (self.WIDTH / 2, self.HEIGHT / 2)
            self.WIN.blit(text, text_rect)
            pygame.display.update()

    def main(self):
        clock = pygame.time.Clock()
        self.snake_rect = pygame.Rect(100, 100, self.snake_width, self.snake_height)
        self.append_snake_part(100, 100)
        self.apple_rect = pygame.Rect(400, 400, self.apple_width, self.apple_height)
        run = True

        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.draw()
            keys_pressed = pygame.key.get_pressed()
            self.snake_movement(keys_pressed)
            self.check_collision()
            self.game_over()

        pygame.quit()


if __name__ == "__main__":
    snake_game = SnakeGame()
    snake_game.main()
