import pygame
import sys
import random
import math

# 初始化Pygame
pygame.init()

# 设置屏幕大小为竖向长方形
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("打砖块游戏")

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)
brown = (139, 69, 19)
blue = (0, 0, 255)
pink = (255, 182, 193)  # 火腿片颜色
olive_green = (107, 142, 35)  # 橄榄颜色

# 定义球和板的参数
ball_radius = 10
paddle_width = 100
paddle_height = 10

# 定义砖块类型
brick_types = [
    {"color": yellow, "radius": 30, "pattern": "pineapple"},
    {"color": red, "radius": 25, "pattern": "ham"},
    {"color": green, "radius": 20, "pattern": "pepper"},
    {"color": brown, "radius": 15, "pattern": "olive"}
]

def draw_pixel_art(surface, x, y, pattern, size):
    if pattern == "pineapple":
        # 绘制菠萝切片
        pygame.draw.circle(surface, yellow, (x, y), size)
        pygame.draw.line(surface, brown, (x - size // 2, y), (x + size // 2, y), 2)
        pygame.draw.line(surface, brown, (x, y - size // 2), (x, y + size // 2), 2)
    elif pattern == "ham":
        # 绘制火腿片
        pygame.draw.circle(surface, pink, (x, y), size)
        pygame.draw.line(surface, red, (x - size // 2, y - size // 2), (x + size // 2, y + size // 2), 2)
        pygame.draw.line(surface, red, (x - size // 2, y + size // 2), (x + size // 2, y - size // 2), 2)
    elif pattern == "pepper":
        # 绘制青椒切片
        pygame.draw.circle(surface, green, (x, y), size)
        pygame.draw.arc(surface, black, (x - size, y - size, 2 * size, 2 * size), 0, math.pi / 2, 2)
        pygame.draw.arc(surface, black, (x - size, y - size, 2 * size, 2 * size), math.pi, 3 * math.pi / 2, 2)
    elif pattern == "olive":
        # 绘制橄榄切片
        pygame.draw.circle(surface, olive_green, (x, y), size)
        pygame.draw.circle(surface, black, (x, y), size // 2)

def create_bricks():
    bricks = []
    center_x, center_y = screen_width // 2, screen_height // 3
    max_radius = min(center_x, center_y) - 50  # 最大半径，留出边距

    while len(bricks) < 40:  # 创建40个随机砖块
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, max_radius)
        brick_x = int(center_x + distance * math.cos(angle))
        brick_y = int(center_y + distance * math.sin(angle))
        brick_type = random.choice(brick_types)

        # 检查砖块是否重叠
        overlap = False
        for brick in bricks:
            other_x, other_y = brick["pos"]
            other_radius = brick["type"]["radius"]
            if (brick_x - other_x) ** 2 + (brick_y - other_y) ** 2 < (brick_type["radius"] + other_radius) ** 2:
                overlap = True
                break

        if not overlap:
            bricks.append({"pos": (brick_x, brick_y), "type": brick_type})

    return bricks

def main_menu():
    # 使用像素风格字体
    font = pygame.font.Font(None, 60)
    title_text = font.render("Eliminate Pineapple Pizza!", True, white)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 3))

    button_font = pygame.font.Font(None, 40)
    start_text = button_font.render("Start New Game", True, black)
    start_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2, 300, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return  # Start the game

        screen.fill(black)
        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, white, start_rect)
        screen.blit(start_text, start_text.get_rect(center=start_rect.center))
        pygame.display.flip()

def pause_screen():
    font = pygame.font.Font(None, 74)
    resume_text = font.render("Resume", True, black)
    restart_text = font.render("Restart", True, black)
    resume_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50, 200, 50)
    restart_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(event.pos):
                    return "resume"
                if restart_rect.collidepoint(event.pos):
                    return "restart"

        # 绘制暂停按钮
        pygame.draw.rect(screen, white, resume_rect)
        pygame.draw.rect(screen, white, restart_rect)
        screen.blit(resume_text, resume_text.get_rect(center=resume_rect.center))
        screen.blit(restart_text, restart_text.get_rect(center=restart_rect.center))
        pygame.display.flip()

def game_over_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("You Lose!", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))

    button_font = pygame.font.Font(None, 50)
    button_text = button_font.render("Restart", True, black)
    button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)
    button_text_rect = button_text.get_rect(center=button_rect.center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Restart the game

        screen.fill(black)
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, white, button_rect)
        screen.blit(button_text, button_text_rect)
        pygame.display.flip()

def victory_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("You Win!", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))

    button_font = pygame.font.Font(None, 50)
    start_text = button_font.render("Start New Game", True, black)
    start_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2, 300, 50)

    main_text = button_font.render("Main Menu", True, black)
    main_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 70, 300, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return "start"
                if main_rect.collidepoint(event.pos):
                    return "main"

        screen.fill(black)
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, white, start_rect)
        screen.blit(start_text, start_text.get_rect(center=start_rect.center))
        pygame.draw.rect(screen, white, main_rect)
        screen.blit(main_text, main_text.get_rect(center=main_rect.center))
        pygame.display.flip()

def main():
    # 初始化球和板的位置
    paddle_x = (screen_width - paddle_width) // 2
    paddle_y = screen_height - 30
    ball_x = paddle_x + paddle_width // 2
    ball_y = paddle_y - ball_radius

    # 随机初始速度，确保向上
    angle = random.uniform(-math.pi / 4, math.pi / 4)  # 随机角度在-45到45度之间
    speed = 4  # 固定速度
    ball_dx = speed * math.cos(angle)
    ball_dy = -speed * math.sin(angle)

    bricks = create_bricks()

    # 定义暂停按钮和主菜单按钮
    pause_button = pygame.Rect(10, 10, 80, 30)
    pause_font = pygame.font.Font(None, 36)
    pause_text = pause_font.render("Pause", True, black)

    main_button = pygame.Rect(screen_width - 90, 10, 80, 30)
    main_text = pause_font.render("Main", True, black)

    # 游戏循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.collidepoint(event.pos):
                    action = pause_screen()
                    if action == "restart":
                        return  # Restart the game
                if main_button.collidepoint(event.pos):
                    main_menu()
                    return  # Go to main menu

        # 获取按键状态
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= 5
        if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
            paddle_x += 5

        # 更新球的位置
        ball_x += ball_dx
        ball_y += ball_dy

        # 碰撞检测
        if ball_x <= 0 or ball_x >= screen_width - ball_radius:
            ball_dx = -ball_dx  # 保持速度不变
        if ball_y <= 0:
            ball_dy = -ball_dy  # 保持速度不变
        if ball_y >= screen_height:
            game_over_screen()
            return  # Exit the main loop to restart the game

        # 球和板的碰撞
        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
        if paddle_rect.collidepoint(ball_x, ball_y + ball_radius):
            ball_dy = -ball_dy  # 保持速度不变

        # 球和砖块的碰撞
        for brick in bricks[:]:
            brick_x, brick_y = brick["pos"]
            brick_radius = brick["type"]["radius"]
            if (brick_x - ball_x) ** 2 + (brick_y - ball_y) ** 2 <= (brick_radius + ball_radius) ** 2:
                ball_dy = -ball_dy  # 保持速度不变
                bricks.remove(brick)
                break

        # 检查是否所有砖块都被消灭
        if not bricks:
            result = victory_screen()
            if result == "start":
                return  # Start a new game
            elif result == "main":
                main_menu()
                return  # Go to main menu

        # 绘制
        screen.fill(black)
        pygame.draw.circle(screen, white, (ball_x, ball_y), ball_radius)
        pygame.draw.rect(screen, blue, paddle_rect)
        for brick in bricks:
            draw_pixel_art(screen, brick["pos"][0], brick["pos"][1], brick["type"]["pattern"], brick["type"]["radius"])

        # 绘制暂停按钮和主菜单按钮
        pygame.draw.rect(screen, white, pause_button)
        screen.blit(pause_text, pause_text.get_rect(center=pause_button.center))
        pygame.draw.rect(screen, white, main_button)
        screen.blit(main_text, main_text.get_rect(center=main_button.center))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# 启动程序时进入主菜单
main_menu()

while True:
    main()

pygame.quit()
sys.exit()