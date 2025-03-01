import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from rubik import RubikCube

def draw_background():
    """Vẽ background gradient"""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST)
    glBegin(GL_QUADS)
    
    # Gradient từ xanh dương nhạt đến trắng
    glColor3f(0.8, 0.9, 1.0)  # Màu trên (xanh dương nhạt)
    glVertex2f(-1.0, 1.0)
    glVertex2f(1.0, 1.0)
    glColor3f(1.0, 1.0, 1.0)  # Màu dưới (trắng)
    glVertex2f(1.0, -1.0)
    glVertex2f(-1.0, -1.0)
    
    glEnd()
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Rubik Solver')

    # Cài đặt OpenGL
    glEnable(GL_DEPTH_TEST)  # Chỉ bật depth testing thôi
    
    # Cài đặt góc nhìn
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -10)

    # Khởi tạo Rubik
    rubik_cube = RubikCube()
    
    # Biến theo dõi chuột
    last_mouse_pos = None
    mouse_pressed = False
    
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
            # Xử lý sự kiện chuột
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Chuột trái
                    mouse_pressed = True
                    last_mouse_pos = pygame.mouse.get_pos()
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Chuột trái
                    mouse_pressed = False
                    
            elif event.type == pygame.MOUSEMOTION and mouse_pressed:
                if last_mouse_pos is not None:
                    current_pos = pygame.mouse.get_pos()
                    dx = current_pos[0] - last_mouse_pos[0]
                    dy = current_pos[1] - last_mouse_pos[1]
                    rubik_cube.rotate_cube(dx * 0.5, dy * 0.5)
                    last_mouse_pos = current_pos

        # Xử lý phím bấm
        keys = pygame.key.get_pressed()
        if not rubik_cube.animating:  # Chỉ cho phép xoay khi không có animation đang chạy
            # Xoay theo chiều kim đồng hồ
            if keys[pygame.K_u]:  # Xoay mặt trên
                rubik_cube.rotate_face('U', True)
            if keys[pygame.K_d]:  # Xoay mặt dưới
                rubik_cube.rotate_face('D', True)
            if keys[pygame.K_f]:  # Xoay mặt trước
                rubik_cube.rotate_face('F', True)
            if keys[pygame.K_b]:  # Xoay mặt sau
                rubik_cube.rotate_face('B', True)
            if keys[pygame.K_l]:  # Xoay mặt trái
                rubik_cube.rotate_face('L', True)
            if keys[pygame.K_r]:  # Xoay mặt phải
                rubik_cube.rotate_face('R', True)
                
            # Xoay ngược chiều kim đồng hồ (giữ SHIFT)
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                if keys[pygame.K_u]:
                    rubik_cube.rotate_face('U', False)
                if keys[pygame.K_d]:
                    rubik_cube.rotate_face('D', False)
                if keys[pygame.K_f]:
                    rubik_cube.rotate_face('F', False)
                if keys[pygame.K_b]:
                    rubik_cube.rotate_face('B', False)
                if keys[pygame.K_l]:
                    rubik_cube.rotate_face('L', False)
                if keys[pygame.K_r]:
                    rubik_cube.rotate_face('R', False)

        # Xóa buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Vẽ background
        draw_background()
        
        # Cập nhật animation nếu có
        rubik_cube.update_animation()
        
        # Vẽ Rubik
        rubik_cube.draw_cube()
        
        # Cập nhật màn hình
        pygame.display.flip()
        clock.tick(60)  # Giới hạn 60 FPS

if __name__ == "__main__":
    main() 