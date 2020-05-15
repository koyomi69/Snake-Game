import pygame
import random
import Client as myModule

pygame.init()
# Sets the window title
pygame.display.set_caption('Snake Game')

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 155, 0)
cyan = (0, 255, 255)

width = 600
height = 400
size = (width, height)
gameDisplay = pygame.display.set_mode(size)
clock = pygame.time.Clock()
clock_speed = 15


class Snake:
    snake_size = 0
    snake_speed = 0
    direction = ('L', 'R', 'U', 'D')
    x_pos = 0
    y_pos = 0
    x_move = 0
    y_move = 0

    def __init__(self, snake_size, snake_speed, x, y, color):
        self.snake_size = snake_size
        self.snake_speed = snake_speed
        self.x_pos = x
        self.y_pos = y
        self.color = color

    def snake_draw(self, snake_list):
        value = 0
        for snak in snake_list:
            value = pygame.draw.rect(gameDisplay, self.color, [snak[0], snak[1], self.snake_size, self.snake_size])
        return value

    def move(self, direc):

        if direc == self.direction[0]:
            self.x_move = -self.snake_speed
            self.y_move = 0
        if direc == self.direction[1]:
            self.x_move = self.snake_speed
            self.y_move = 0
        if direc == self.direction[2]:
            self.y_move = -self.snake_speed
            self.x_move = 0
        if direc == self.direction[3]:
            self.y_move = self.snake_speed
            self.x_move = 0

    def pos_update(self):
        self.x_pos += self.x_move
        self.y_pos += self.y_move

    # For checking if snake collides with itself and wall
    @staticmethod
    def check_dead(snake_head, snake_list, snake_charac):
        walls = draw_walls()
        # Won't work for len = 0 and len = 1
        if snake_head in snake_list[:-1]:
            return True
        if not walls.colliderect(snake_charac):
            return True


def draw_walls():
    world = pygame.Rect(10, 10, width, height)
    return world


def quiting():
    pygame.quit()
    quit()


def pick_font(name, font_size):
    # SysFont(name, size, bold=False, italic=False)
    font = pygame.font.SysFont(name, font_size)
    return font


def screen_message(msg, color, displ, mes_font):
    text_on_screen = mes_font.render(msg, True, color)
    text_rect = text_on_screen.get_rect(center=(width / 2.0, height / 2.0 + displ))
    gameDisplay.blit(text_on_screen, text_rect)


# The Loop where the operation of the snake goes
def main():
    running = True
    over = True
    len_snake = 0
    len_snake2 = 0
    snake_list = []
    snake_list2 = []

    n = myModule.Network()
    start_pos = n.getPos()

    snake = Snake(10, 10, start_pos[0], start_pos[1], green)
    snake2 = Snake(10, 10, width / 2.0, height / 2.0, cyan)

    sender = [start_pos[0], start_pos[1]]
    p_pos = n.send(sender)
    snake2.x_pos = p_pos[0]
    snake2.y_pos = p_pos[1]

    while running:
        # Displays the messages when our game ends
        if not over:
            mes_font = pick_font(None, 25)
            screen_message('Game Over!', red, -20, mes_font)
            pygame.display.update()
        # Loop for when game ends so both reset and quit options gets available
        while not over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    over = True
        for event in pygame.event.get():
            # pygame.QUIT : This is the event type that is fired when you click on the close button.
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snake.move('L')
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snake.move('R')
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    snake.move('U')
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snake.move('D')

        snake.pos_update()
        sender = [snake.x_pos, snake.y_pos]
        p_pos = n.send(sender)
        snake2.x_pos = p_pos[0]
        snake2.y_pos = p_pos[1]

        # Clear the screen and set the screen background
        gameDisplay.fill(white)

        snake_head = [snake.x_pos, snake.y_pos]
        snake_head2 = [snake2.x_pos, snake2.y_pos]
        snake_list.append(snake_head)
        snake_list2.append(snake_head2)
        snake_character = snake.snake_draw(snake_list)
        snake_character2 = snake2.snake_draw(snake_list2)

        if snake.check_dead(snake_head, snake_list, snake_character):
            mes_font = pick_font(None, 20)
            screen_message("Player 1 Dies", black, 30, mes_font)
            over = False

        if snake2.check_dead(snake_head2, snake_list2, snake_character2):
            mes_font = pick_font(None, 20)
            screen_message("Player 2 Dies", black, 30, mes_font)
            over = False

        # Checking to see if both players collide with each other
        if snake_head in snake_list2:
            mes_font = pick_font(None, 20)
            screen_message("Player 1 Dies", black, 30, mes_font)
            over = False

        elif snake_head2 in snake_list:
            mes_font = pick_font(None, 20)
            screen_message("Player 2 Dies", black, 30, mes_font)
            over = False

        elif snake_head in snake_head2:
            mes_font = pick_font(None, 20)
            screen_message("Both Players are Killed", black, 30, mes_font)
            over = False

        if len(snake_list) > len_snake:
            del snake_list[0]

        if len(snake_list2) > len_snake2:
            del snake_list2[0]

        pygame.display.update()
        clock.tick(clock_speed)

    quiting()


if __name__ == "__main__":
    main()
