from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

w_width = 600
w_height = 800  # increases with the maximizing button on top right
lives = 3 #lives
shooter_x = w_width // 2
shooter_y = 20
shooter_r = 15
bullets = []
balls = []
score = 0
game_over = False
pause = False
color = [random.random(), random.random(), random.random()]

def line(x1, y1, x2, y2, color):
    glColor3f(*color)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    inc = abs(dy) > abs(dx)
    d = 2 * dy - dx
    y = y1

    if inc == True:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        dx, dy = dy, dx

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    d = 2 * dy - dx
    y = y1

    for x in range(int(x1), int(x2) + 1):
        if inc == True:
            glBegin(GL_POINTS)
            glVertex2f(int(y), int(x))
            glEnd()
        else:
            glBegin(GL_POINTS)
            glVertex2f(int(x), int(y))
            glEnd()

        if d > 0:
            y += 1 if y1 < y2 else -1
            d -= 2 * dx
        d += 2 * dy

def circle(a, b, r, color):
    glColor3f(*color)
    d = 1 - r
    x = 0
    y = r
    while x <= y:
        if d < 0:
            d = d + 2 * x + 3
            x += 1
        else:
            d = d + 2 * x - 2 * y + 5
            x += 1
            y -= 1
        glBegin(GL_POINTS)
        glVertex2f(x + a, y + b)
        glVertex2f(x + a, -y + b)
        glVertex2f(-x + a, -y + b)
        glVertex2f(-x + a, y + b)
        glVertex2f(y + a, x + b)
        glVertex2f(y + a, -x + b)
        glVertex2f(-y + a, -x + b)
        glVertex2f(-y + a, x + b)
        glEnd()

def draw_balls():
    global color
    for i in balls:
        color = [random.random(), random.random(), random.random()]
        circle(i[0], i[1], i[2], color)

def generate_balls():
    global balls
    x = random.randint(50, 550)
    y = random.randint(820,1000)
    r = random.randint(15, 40)
    balls.append((x, y, r))

def drop_balls():
    global balls

    if pause == False:
        new_balls = []

        for i in balls[0:7]:
            x, y, r = i
            y -= 1
            if y > 0:
                new_balls.append((x, y, r))

        balls = new_balls

def draw_shooter():
    global shooter_x, shooter_y
    circle(shooter_x, shooter_y, shooter_r, [1, 1, 1])  # right left handle baki

def restart_button():
    line(10, w_height - 30, 60, w_height - 30, [0, 0, 1])
    line(10, w_height - 30, 20, w_height - 20, [0, 0, 1])
    line(10, w_height - 30, 20, w_height - 40, [0, 0, 1])

def pause_button():
    if pause == True:
        line(w_width // 2 - 5, w_height - 20, w_width // 2 - 5, w_height - 40, [1, 1, 0])
        line(w_width // 2 - 5, w_height - 40, w_width // 2 + 20, w_height - 30, [1, 1, 0])
        line(w_width // 2 - 5, w_height - 20, w_width // 2 + 20, w_height - 30, [1, 1, 0])
    else:
        line(w_width // 2 - 5, w_height - 20, w_width // 2 - 5, w_height - 40, [1, 1, 0])
        line(w_width // 2 + 5, w_height - 20, w_width // 2 + 5, w_height - 40, [1, 1, 0])

def exit_button():
    line(w_width - 30, w_height - 20, w_width - 10, w_height - 40, [1, 0, 0])
    line(w_width - 30, w_height - 40, w_width - 10, w_height - 20, [1, 0, 0])

def mouse_click(button, state, x, y):
    global game_over, pause, color, balls, score, lives
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = w_height - y
        if (x >= (w_width - 50) and x <= (w_width - 10) and y >= (w_height - 50) and y <= (
                w_height - 10)):  # exit button click
            print("Thank you for Playing ")
            print(f"Total Score: {score}")
            glutLeaveMainLoop()


        elif (x >= (w_width // 2 - 20) and x <= (w_width // 2 + 20) and y >= (w_height - 50) and y <= (
                w_height - 10)):  # pause button click
            if game_over == False:
                pause = not pause

        elif (x >= 10 and x <= 60 and y >= (w_height - 50) and y <= (w_height - 10)):  # restart button
            print("Restarting Game")

            game_over = False
            score = 0
            pause = False
            lives = 3
            balls = []
            color = [random.random(), random.random(), random.random()]

def draw_bullet():
    for b in bullets:
        bx, by, bz = b
        circle(bx, by, bz, [1, 1, 1])

def position_update():
   global bullets, balls, score, lives
   new_bullets = []
   new_balls = []
   for bullet in bullets:
      bx, by, br = bullet
      hit = False
      for ball in balls:
         ball_x, ball_y, ball_r = ball
         distance = ((bx - ball_x) ** 2 + (by - ball_y) ** 2) ** 0.5
         if distance < br + ball_r:
            hit = True
            score += 1  # Update score
            print(f"Score: {score}")
            print(f"Lives: {lives}")
            balls.remove(ball)  # Remove the hit falling circle
            break

      if hit == False:
         new_bullets.append(bullet)

   bullets = new_bullets

   for ball in balls:
        ball_x, ball_y, ball_r = ball
        if ball_y > 0:
            new_balls.append(ball)  
   balls = new_balls

   for ball in balls:
      ball_x, ball_y, ball_r = ball
      if ball_y-ball_r <=0:
         if(lives>0):   
            lives-=1
            print(f"Lives left: {lives}")
            balls.remove(ball)
            break
         else:
            game_over=True
            print(f"Game Over: Total Score: ", score)
            glutLeaveMainLoop()
        
def shoot_bullet():
    global bullets
    if pause == False:
        new_bullets = []
        for b in bullets:
            x, y, r = b
            y += 20  # Update the y-coordinate to move the bullet upwards
            if y > 0:
                new_bullets.append((x, y, r))
        bullets = new_bullets

def keyboard(key, x, y):
    global bullets
    if key == b' ':
        bullet_x = shooter_x
        bullet_y = shooter_y
        bullet_r = shooter_r // 2
        bullets.append((bullet_x, bullet_y, bullet_r))

def special_keys(key, x, y):
    global shooter_x
    if pause == False:
        if game_over == False:
            if key == GLUT_KEY_RIGHT:
                shooter_x = min(shooter_x + 15, w_width - 15)
            elif key == GLUT_KEY_LEFT:
                shooter_x = max(shooter_x - 15, 15)

def show_screen():
    glClear(GL_COLOR_BUFFER_BIT)
    restart_button()
    pause_button()
    exit_button()
    draw_shooter()
    generate_balls()
    draw_balls()
    drop_balls()
    draw_bullet()
    shoot_bullet()
    position_update()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(600, 800)
glutCreateWindow(b"shoot the balls")
glOrtho(0, 600, 0, 800, -1, 1)
glClearColor(0, 0, 0, 1)

glutDisplayFunc(show_screen)
glutSpecialFunc(special_keys)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse_click)
glutIdleFunc(show_screen)
glutDisplayFunc(show_screen) 
glutSpecialFunc(special_keys)
glutIdleFunc(show_screen)
glutMainLoop()

