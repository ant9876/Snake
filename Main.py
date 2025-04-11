import pygame
import random

pygame.init()

width, height = 600, 400
block_size = 20
snake_speed = 15


light_pink = (250, 210, 240)
light_pink_grid = (250, 225, 244)
dark_purple = (131, 84, 138)
word_purple = (150, 68, 141)
apple_color = (179, 100, 150)
black = (0, 0, 0)
red = (184, 44, 139)
brown = (139, 69, 19)
silver = (199, 200, 209)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

font_path = 'atop.ttf'
font_two ='boorush.ttf'
font_tim_cheese = 'sourgummy.ttf'
font_milk = 'shadowsintolighttwo.ttf'
font_style = pygame.font.SysFont("bahnschrift", 50)
bubblegum_font = pygame.font.Font(font_path, 50)
button_font = pygame.font.Font(font_two, 30)
score_font = pygame.font.SysFont("bahnschrift", 25)
message_font = pygame.font.Font(font_tim_cheese, 30)
words_font = pygame.font.Font(font_milk, 30)

high_score = 0
new_high_score_flag = False
game_start = False

def display_score(score):
    value = words_font.render("Apples Eaten: " + str(score), True, black)
    window.blit(value, [width - value.get_width() - 10, 10])  # Top-right corner

def display_game_over(is_new_high_score, apples_eaten, high_score):
    window.fill(light_pink)

    if is_new_high_score:
        message = "HIGH SCORE"
        color = word_purple
    else:
        message = "GAME OVER"
        color = red

    temp_bubblegum_font = pygame.font.Font(font_path, 90)

    lines = message.split('\n')
    y_offset = height / 10
    for line in lines:
        game_over_msg = temp_bubblegum_font.render(line, True, color)
        window.blit(game_over_msg, [(width - game_over_msg.get_width()) / 2, y_offset+30])
        y_offset += game_over_msg.get_height() + 5

    larger_score_font = words_font
    score_y_offset = y_offset + 5  # Reduced spacing to bring closer
    score_msg = larger_score_font.render(f"  Apples Eaten: {apples_eaten} ", True, black)
    high_score_msg = larger_score_font.render(f"High Score: {high_score}", True, black)

    window.blit(score_msg, [(width / 2) - score_msg.get_width() - 5, score_y_offset+35])
    window.blit(high_score_msg, [(width / 2) + 15, score_y_offset+35])

    instruction_font = message_font
    instruction_msg1 = instruction_font.render("Press E to Exit or R to Play Again", True, black)
    window.blit(instruction_msg1, [(width - instruction_msg1.get_width()) / 2, 270])

    pygame.display.update()

def display_title_screen():
    window.fill(light_pink)

    title_font = pygame.font.Font(font_path, 120)
    title_text = title_font.render("SNAKE", True, word_purple)
    title_x = (width - title_text.get_width()) / 2
    title_y = height / 7 + 20
    window.blit(title_text, (title_x, title_y))

    button_color = word_purple
    button_hover_color = (173, 120, 157)
    text_color = light_pink
    padding_x, padding_y = 20, 10

    buttons = [
        ("Rosy Boa", 5),
        ("King Cobra", 15),
        ("Sidewinder", 25),
    ]

    button_y = height // 2 + 50
    button_spacing = 20

    button_rects = []
    max_height = 0

    for label, _ in buttons:
        text_surface = button_font.render(label, True, text_color)
        text_width, text_height = text_surface.get_size()
        max_height = max(max_height, text_height + 2 * padding_y)
        button_rects.append((text_width + 2 * padding_x, text_height + 2 * padding_y, text_surface))

    total_button_width = sum(rect[0] for rect in button_rects) + (len(buttons) - 1) * button_spacing
    start_x = (width - total_button_width) // 2

    waiting = True
    while waiting:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        button_x = start_x
        for i, (label, speed) in enumerate(buttons):
            button_width, button_height, text_surface = button_rects[i]
            current_color = button_hover_color if (button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + max_height) else button_color

            pygame.draw.rect(window, current_color, (button_x, button_y, button_width, max_height), border_radius=10)

            text_x = button_x + (button_width - text_surface.get_width()) // 2
            text_y = button_y + (max_height - text_surface.get_height()) // 2
            window.blit(text_surface, (text_x, text_y))

            button_x += button_width + button_spacing

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_x = start_x
                for i, (label, speed) in enumerate(buttons):
                    button_width, button_height, _ = button_rects[i]
                    if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + max_height:
                        global snake_speed
                        snake_speed = speed
                        waiting = False
                    button_x += button_width + button_spacing

def display_timer(time_remaining):
    if time_remaining > 0:
        seconds = time_remaining // 1000
        timer_text = words_font.render(f"{seconds}", True, black)
        window.blit(timer_text, [10, 10])


def game_loop():
    global high_score, new_high_score_flag, game_start, snake_speed

    if not game_start:
        display_title_screen()
        game_start = True

    game_over = False
    game_close = False

    x, y = width // 2, height // 2
    x_change, y_change = 0, 0

    snake_list = [[x, y]]
    length_of_snake = 1

    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    pink_apple = None
    pink_apple_spawn_chance = 0.1

    rotten_apple = None
    rotten_apple_spawn_chance = 0.1  # or whatever you want

    silver_apple = None
    silver_apple_spawn_chance = 0.1

    ghost_apple = None
    ghost_apple_spawn_chance = 0.1

    ghost_mode_active = False
    ghost_mode_end_time = 0

    slow_effect_active = False
    slow_effect_end_time = 0
    original_speed = snake_speed  # store default speed

    apples_eaten = 0
    double_points_active = False
    double_points_end_time = 0

    reverse_controls_active = False
    reverse_controls_end_time = 0

    while not game_over:
        while game_close:
            if apples_eaten > high_score and not new_high_score_flag:
                high_score = apples_eaten
                new_high_score_flag = True

            display_game_over(new_high_score_flag, apples_eaten, high_score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        new_high_score_flag = False
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                left = pygame.K_LEFT if not reverse_controls_active else pygame.K_RIGHT
                right = pygame.K_RIGHT if not reverse_controls_active else pygame.K_LEFT
                up = pygame.K_UP if not reverse_controls_active else pygame.K_DOWN
                down = pygame.K_DOWN if not reverse_controls_active else pygame.K_UP

                a = pygame.K_a if not reverse_controls_active else pygame.K_d
                d = pygame.K_d if not reverse_controls_active else pygame.K_a
                w = pygame.K_w if not reverse_controls_active else pygame.K_s
                s = pygame.K_s if not reverse_controls_active else pygame.K_w

                if (event.key == left or event.key == a) and x_change == 0:
                    x_change = -block_size
                    y_change = 0
                elif (event.key == right or event.key == d) and x_change == 0:
                    x_change = block_size
                    y_change = 0
                elif (event.key == up or event.key == w) and y_change == 0:
                    y_change = -block_size
                    x_change = 0
                elif (event.key == down or event.key == s) and y_change == 0:
                    y_change = block_size
                    x_change = 0

        x += x_change
        y += y_change

        if ghost_mode_active:
            # Wrap around the screen edges
            if x >= width:
                x = 0
            elif x < 0:
                x = width - block_size
            if y >= height:
                y = 0
            elif y < 0:
                y = height - block_size
        else:
            # Normal border collision
            if x >= width or x < 0 or y >= height or y < 0:
                game_close = True

        window.fill(light_pink)

        for x_pos in range(0, width, block_size):
            for y_pos in range(0, height, block_size):
                pygame.draw.rect(window, light_pink_grid, [x_pos, y_pos, block_size, block_size], 1)

        # Draw normal apple
        pygame.draw.rect(window, apple_color, [food_x, food_y, block_size, block_size], border_radius=5)

        # Draw hot pink apple if it exists
        if pink_apple:
            pygame.draw.rect(window, red, [pink_apple[0], pink_apple[1], block_size, block_size], border_radius=5)

        if rotten_apple:
            pygame.draw.rect(window, brown, [rotten_apple[0], rotten_apple[1], block_size, block_size], border_radius=5)

        if silver_apple:
            pygame.draw.rect(window, silver, [silver_apple[0], silver_apple[1], block_size, block_size], border_radius=5)

        if ghost_apple:
            # Transparent fill (draw nothing), just draw black border
            pygame.draw.rect(window, black, [ghost_apple[0], ghost_apple[1], block_size, block_size], width=2, border_radius=5)

        snake_head = [x, y]
        snake_list.insert(0, snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[-1]

        for segment in snake_list[1:]:
            if segment == snake_head and not ghost_mode_active:
                game_close = True

        for i, segment in enumerate(snake_list):
            rect = pygame.Rect(segment[0], segment[1], block_size, block_size)
            if ghost_mode_active:
                pygame.draw.rect(window, black, rect, width=2, border_radius=5)
            else:
                if i == 0:
                    pygame.draw.rect(window, dark_purple, rect, border_radius=5)
                else:
                    pygame.draw.rect(window, dark_purple, rect)

        # Display score
        display_score(apples_eaten)

        if double_points_active:
            time_remaining = double_points_end_time - pygame.time.get_ticks()
            display_timer(time_remaining)

        if slow_effect_active:
            time_remaining = slow_effect_end_time - pygame.time.get_ticks()
            display_timer(time_remaining)

        if reverse_controls_active:
            time_remaining = reverse_controls_end_time - pygame.time.get_ticks()
            display_timer(time_remaining)

        if ghost_mode_active:
            time_remaining = ghost_mode_end_time - pygame.time.get_ticks()
            display_timer(time_remaining)

        if reverse_controls_active and pygame.time.get_ticks() > reverse_controls_end_time:
            reverse_controls_active = False

        # Check collision with normal apple
        if x == food_x and y == food_y:
            if double_points_active:
                apples_eaten += 2
            else:
                apples_eaten += 1
            length_of_snake += 1

            # Spawn new normal apple
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

            if not pink_apple and not rotten_apple and not silver_apple and not ghost_apple:
                roll = random.random()
                if roll < pink_apple_spawn_chance:
                    pink_apple_x = round(random.randrange(0, width - block_size) / block_size) * block_size
                    pink_apple_y = round(random.randrange(0, height - block_size) / block_size) * block_size
                    pink_apple = (pink_apple_x, pink_apple_y)
                elif roll < pink_apple_spawn_chance + rotten_apple_spawn_chance:
                    rotten_apple_x = round(random.randrange(0, width - block_size) / block_size) * block_size
                    rotten_apple_y = round(random.randrange(0, height - block_size) / block_size) * block_size
                    rotten_apple = (rotten_apple_x, rotten_apple_y)
                elif roll < pink_apple_spawn_chance + rotten_apple_spawn_chance + silver_apple_spawn_chance:
                    silver_apple_x = round(random.randrange(0, width - block_size) / block_size) * block_size
                    silver_apple_y = round(random.randrange(0, height - block_size) / block_size) * block_size
                    silver_apple = (silver_apple_x, silver_apple_y)
                elif roll < pink_apple_spawn_chance + rotten_apple_spawn_chance + silver_apple_spawn_chance + ghost_apple_spawn_chance:
                    ghost_apple_x = round(random.randrange(0, width - block_size) / block_size) * block_size
                    ghost_apple_y = round(random.randrange(0, height - block_size) / block_size) * block_size
                    ghost_apple = (ghost_apple_x, ghost_apple_y)

        if pink_apple and x == pink_apple[0] and y == pink_apple[1]:
            double_points_active = True
            double_points_end_time = pygame.time.get_ticks() + 20000
            pink_apple = None

        if silver_apple and x == silver_apple[0] and y == silver_apple[1]:
            reverse_controls_active = True
            reverse_controls_end_time = pygame.time.get_ticks() + 20000  # 20 seconds
            silver_apple = None

        if rotten_apple and x == rotten_apple[0] and y == rotten_apple[1]:
            slow_effect_active = True
            slow_effect_end_time = pygame.time.get_ticks() + 20000  # 20 seconds
            snake_speed = max(5, snake_speed // 2)  # Slow down but not below 5
            rotten_apple = None

        if ghost_apple and x == ghost_apple[0] and y == ghost_apple[1]:
            ghost_mode_active = True
            ghost_mode_end_time = pygame.time.get_ticks() + 20000  # 20 seconds
            ghost_apple = None

        if double_points_active and pygame.time.get_ticks() > double_points_end_time:
            double_points_active = False

        if slow_effect_active and pygame.time.get_ticks() > slow_effect_end_time:
            slow_effect_active = False
            snake_speed = original_speed

        if ghost_mode_active and pygame.time.get_ticks() > ghost_mode_end_time:
            ghost_mode_active = False

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()


game_loop()

