import pygame
import sys
from moviepy.editor import VideoFileClip

# 初始化pygame
pygame.init()

# 设置窗口大小
screen = pygame.display.set_mode((600, 400))

# 设置窗口标题
pygame.display.set_caption("Button and Video Example")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (255, 255, 255)

# 定义按钮的矩形区域
button_rect = pygame.Rect(250, 175, 200, 50)


def draw_button(screen, color, text, font_size):
    font = pygame.font.Font(None, font_size)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=button_rect.center)
    pygame.draw.rect(screen, color, button_rect)
    screen.blit(text_surf, text_rect)


try:
    # 加载视频并设置帧率为24fps
    video_clip = VideoFileClip('gameOver.mp4')
    video_clip = video_clip.resize((600, 400))  # 调整视频大小以适应窗口
    video_clip = video_clip.set_fps(24)  # 设置帧率为24fps
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
                    print("Button clicked!")

        # 获取当前帧并转换为pygame图像
        frame_image = pygame.surfarray.make_surface(video_frames[current_frame].swapaxes(0, 1))
        screen.blit(frame_image, (0, 0))

        # 绘制按钮（覆盖在视频上）
        draw_button(screen, GREEN, "start new game", 30)

        # 更新帧索引
        current_frame = (current_frame + 1) % len(video_frames)

        pygame.display.flip()

        # 控制帧率
        clock.tick(24)  # 设置帧率为24fps
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    pygame.quit()
    sys.exit()
