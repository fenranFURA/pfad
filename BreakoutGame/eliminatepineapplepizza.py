import pygame
import sys
import random
import math
import cv2
from tkinter import *
from moviepy.editor import VideoFileClip

# Initialize Pygame
pygame.init()

# Set screen size
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pineapple Apocalypse")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)
brown = (139, 69, 19)
blue = (0, 0, 255)

# Define ball and paddle parameters
ball_radius = 10
paddle_width = 100
paddle_height = 100

# 在初始化部分加载砖块图片
yellow_brick_img = pygame.image.load("yellow_brick.png")
red_brick_img = pygame.image.load("red_brick.png")
green_brick_img = pygame.image.load("green_brick.png")
brown_brick_img = pygame.image.load("brown_brick.png")

# 定义砖块类型，添加图片
brick_types = [
    {"color": yellow, "radius": 30, "image": yellow_brick_img},
    {"color": red, "radius": 25, "image": red_brick_img},
    {"color": green, "radius": 20, "image": green_brick_img},
    {"color": brown, "radius": 15, "image": brown_brick_img}
]

# Load the paddle image
paddle_image = pygame.image.load("path_to_your_paddle_image.png").convert_alpha()
paddle_image = pygame.transform.scale(paddle_image, (paddle_width, paddle_height))

# 按钮参数
button_color = (255, 0, 0) 
button_rect = pygame.Rect(screen_width // 2 - 120, 540 + 70, 240, 50)  # 按钮位置和大小

def draw_button(screen, color, text, font_size):
    font = pygame.font.Font(None, font_size)
    text_surf = font.render(text, True, black)
    text_rect = text_surf.get_rect(center=button_rect.center)
    pygame.draw.rect(screen, color, button_rect)
    screen.blit(text_surf, text_rect)

def create_bricks():
    bricks = []
    center_x, center_y = screen_width // 2, screen_height // 3
    max_radius = min(center_x, center_y) - 50  # Maximum radius with margin

    while len(bricks) < 40:  # Create 40 random bricks
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, max_radius)
        brick_x = int(center_x + distance * math.cos(angle))
        brick_y = int(center_y + distance * math.sin(angle))
        brick_type = random.choice(brick_types)

        # Check for overlap
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
    video_clip = VideoFileClip("Main_video.mp4")
    video_clip = video_clip.resize((screen_width, screen_height))  # 调整视频大小以适应窗口
    video_clip = video_clip.set_fps(24) 
    video_frames = [frame for frame in video_clip.iter_frames()]
    current_frame = 0

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    main()  # Start the game

        # 获取当前帧并转换为pygame图像
        frame_image = pygame.surfarray.make_surface(video_frames[current_frame].swapaxes(0, 1))
        screen.blit(frame_image, (0, 0))

        # 加载图片
        start_image = pygame.image.load("path_to_your_paddle_image.png").convert_alpha()
        start_image = pygame.transform.scale(start_image, (300, 50))

        # 绘制按钮（覆盖在视频上）
        screen.blit(start_image, start_image.get_rect(center=button_rect.center))

        # 更新帧索引
        current_frame = (current_frame + 1) % len(video_frames)

        pygame.display.flip()

        # 控制帧率
        clock.tick(24)

    pygame.quit()
    sys.exit()

def pause_screen():
    resume_image = pygame.image.load("path_to_your_paddle_image.png").convert_alpha()
    resume_image = pygame.transform.scale(resume_image, (200, 50))
    resume_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50, 200, 50)

    restart_image = pygame.image.load("path_to_your_paddle_image.png").convert_alpha()
    restart_image = pygame.transform.scale(restart_image, (200, 50))
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
        screen.blit(resume_image, resume_image.get_rect(center=resume_rect.center))
        screen.blit(restart_image, restart_image.get_rect(center=restart_rect.center))
        pygame.display.flip()

def game_over_screen():
    play_video("gameOver.mp4")
    return

def play_video(video_path):
    try:
        # 加载视频并设置帧率为24fps
        video_clip = VideoFileClip(video_path)
        video_clip = video_clip.resize((screen_width, screen_height))  # 调整视频大小以适应窗口
        video_clip = video_clip.set_fps(30)  # 设置帧率为24fps
        video_frames = [frame for frame in video_clip.iter_frames()]
        current_frame = 0

        # 创建时钟对象以控制帧率
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        main()

            # 获取当前帧并转换为pygame图像
            frame_image = pygame.surfarray.make_surface(video_frames[current_frame].swapaxes(0, 1))
            screen.blit(frame_image, (0, 0))

            # 加载图片
            start_image = pygame.image.load("path_to_your_paddle_image.png").convert_alpha()
            start_image = pygame.transform.scale(start_image, (300, 50))

            # 绘制按钮（覆盖在视频上）
            screen.blit(start_image, start_image.get_rect(center=button_rect.center))

            # 更新帧索引
            current_frame = (current_frame + 1) % len(video_frames)

            pygame.display.flip()

            # 控制帧率
            clock.tick(30)  # 设置帧率为24fps
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()
        sys.exit()

def victory_screen():
    play_video("victory_video.mp4")
    return "main"

def main():
    # 初始化球和板的位置
    paddle_x = (screen_width - paddle_width) // 2
    paddle_y = screen_height - paddle_height
    ball_x = paddle_x + paddle_width // 2
    ball_y = paddle_y - ball_radius

    # 随机初始速度，确保向上
    angle = random.uniform(-math.pi / 7.2, math.pi / 7.2)  # 随机角度在-25到25度之间
    speed = 8
    ball_dx = speed * math.cos(angle)
    ball_dy = -speed * math.sin(angle)

    bricks = create_bricks()

    # 定义暂停按钮和主菜单按钮
    pause_image = pygame.image.load("path_to_your_paddle_image.png").convert_alpha()
    pause_image = pygame.transform.scale(pause_image, (80, 30))
    pause_rect = pygame.Rect(10, 10, 80, 30)

    main_image = pygame.image.load("path_to_your_paddle_image.png").convert_alpha()
    main_image = pygame.transform.scale(main_image, (80, 30))
    main_rect = pygame.Rect(screen_width - 90, 10, 80, 30)

    # 游戏循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(event.pos):
                    action = pause_screen()
                    if action == "restart":
                        # 重新开始游戏
                        paddle_x = (screen_width - paddle_width) // 2
                        paddle_y = screen_height - paddle_height
                        ball_x = paddle_x + paddle_width // 2
                        ball_y = paddle_y - ball_radius
                        angle = random.uniform(-math.pi / 7.2, math.pi / 7.2)  # 随机角度在-25到25度之间
                        speed = 6
                        ball_dx = speed * math.cos(angle)
                        ball_dy = -speed * math.sin(angle)
                        bricks = create_bricks()
                if main_rect.collidepoint(event.pos):
                    main_menu()
                    return  # Go to main menu

        # 获取按键状态
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= 6
        if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
            paddle_x += 6

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

        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
        if paddle_rect.collidepoint(ball_x, ball_y + ball_radius):
            ball_dy = -ball_dy
        for brick in bricks[:]:
            brick_x, brick_y = brick["pos"]
            brick_radius = brick["type"]["radius"]
            if (brick_x - ball_x) ** 2 + (brick_y - ball_y) ** 2 <= (brick_radius + ball_radius) ** 2:
                ball_dy = -ball_dy
                bricks.remove(brick)
                break
        if not bricks:
            result = victory_screen()
            if result == "start":
                return
            elif result == "main":
                main_menu()
                return

         # 绘制背景图片
        background = pygame.image.load("background.jpg")
        background = pygame.transform.scale(background, (screen_width, screen_height))
        screen.blit(background, (0, 0))

         # 绘制球、板和砖块
        pygame.draw.circle(screen, white, (ball_x, ball_y), ball_radius)
        screen.blit(paddle_image, (paddle_x, paddle_y))  # 使用加载的图像绘制paddle
        for brick in bricks:
            brick_x, brick_y = brick["pos"]
            brick_radius = brick["type"]["radius"]
            brick_img = brick["type"]["image"]
            # 调整图片大小，保持宽高比
            scale_factor = brick_radius * 2 / brick_img.get_height()
            brick_img_scaled = pygame.transform.scale(brick_img, (int(brick_img.get_width() * scale_factor), int(brick_img.get_height() * scale_factor)))
            # 绘制图片
            screen.blit(brick_img_scaled, (brick_x - brick_img_scaled.get_width() // 2, brick_y - brick_img_scaled.get_height() // 2))

        # 绘制暂停按钮和主菜单按钮
        screen.blit(pause_image, pause_image.get_rect(center=pause_rect.center))
        screen.blit(main_image, main_image.get_rect(center=main_rect.center))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

main_menu()

while True:
    main()

pygame.quit()
sys.exit()