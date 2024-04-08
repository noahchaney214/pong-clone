import pygame as pg
from pathlib import Path

""" Simple Pong Copy

    First player to 11 wins.
"""

WIDTH = 1000
HEIGHT = 800

pg.init()

WIN = 11

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('PONG')
pg.display.set_icon(pg.image.load('Ping-Pong-icon.png'))
clock = pg.time.Clock()
running = True

# ball variables
ball_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)
speed = 1
dirx = 0.25 * speed
diry = 0.25 * speed

# paddle variables
wall_marg = 30
paddl1_pos = pg.Vector2(wall_marg, screen.get_height() / 2)
paddl2_pos = pg.Vector2(screen.get_width() - wall_marg, screen.get_height() / 2)
paddle_h = 75
paddle_w = 10

# Declare Font
path = 'Grand9K Pixel.ttf'
font = pg.font.Font(path, 16)
lg_font = pg.font.Font(path, 30)
huge_font = pg.font.Font(path, 50)

# countdown timer
countdown, text = 3, '3'
pg.time.set_timer(pg.USEREVENT, 1000)


# player 1 score
p1_score, p1_text = 0, '0'


# player 2 score
p2_score, p2_text = 0, '0'


dt = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.USEREVENT: 
            countdown -= 1
            if countdown > 0:
                text = str(countdown)
            elif countdown == 0:
                text = 'Start!'
            else:
                text = ''

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    if p2_score < WIN and p1_score < WIN:

        if p1_score >= 4 or p2_score >= 4:
            speed = 1.2
        if p1_score >= 4 or p2_score >= 4:
            speed = 1.4
        if p1_score >= 6 or p2_score >= 6:
            speed = 1.6
        if p1_score >= 8 or p2_score >= 8:
            speed = 1.8
        if p1_score >= 10 or p2_score >= 10:
            speed = 2

        keys = pg.key.get_pressed()

        # ball and position
        RADIUS = 10
        pg.draw.circle(screen, "white", ball_pos, RADIUS)
        
        if countdown > 0:
            screen.blit(font.render(text, True, (255, 255, 255)), (screen.get_width()/2 - 15, 100))
        else:
            ball_pos.y += diry * dt * speed
            ball_pos.x += dirx * dt * speed

        # collision detection for ball
        if ball_pos.y + RADIUS >= screen.get_height() or ball_pos.y - RADIUS <= 0:
            diry *= -1 
        if ball_pos.x + RADIUS >= paddl2_pos.x - paddle_w/2 and paddl2_pos.y + paddle_h/2 >= ball_pos.y >= paddl2_pos.y - paddle_h/2  \
            or ball_pos.x - RADIUS <= paddl1_pos.x + paddle_w/2 and paddl1_pos.y + paddle_h/2 >= ball_pos.y >= paddl1_pos.y - paddle_h/2: 
            dirx *= -1
        if ball_pos.x + RADIUS >= screen.get_width():
            ball_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)
            countdown = 4
            p1_score += 1
            p1_text = str(p1_score)
        if ball_pos.x - RADIUS <= 0:
            ball_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)
            countdown = 4
            p2_score += 1
            p2_text = str(p2_score)

        # draw paddle 1
        pg.draw.rect(screen, "white", pg.Rect((paddl1_pos.x - paddle_w/2, paddl1_pos.y - paddle_h/2),(paddle_w, paddle_h)))

        # draw player 1 score
        screen.blit(lg_font.render(p1_text, True, (255, 255, 255)), (100, 75))

        # draw paddle 2
        pg.draw.rect(screen, "white", pg.Rect((paddl2_pos.x - paddle_w/2, paddl2_pos.y - paddle_h/2),(paddle_w, paddle_h)))

        # draw player 2 score
        screen.blit(lg_font.render(p2_text, True, (255, 255, 255)), (screen.get_width() - 100, 75))

        # paddle movements
        if keys[pg.K_w]:
            if paddl1_pos.y - paddle_h/2 > 0:
                paddl1_pos.y -= 0.3 * dt
        if keys[pg.K_s]:
            if paddl1_pos.y + paddle_h/2 < screen.get_height():
                paddl1_pos.y += 0.3 * dt

        if keys[pg.K_o]:
            if paddl2_pos.y - paddle_h/2 > 0:
                paddl2_pos.y -= 0.3 * dt
        if keys[pg.K_l]:
            if paddl2_pos.y + paddle_h/2 < screen.get_height():
                paddl2_pos.y += 0.3 * dt

    else:
        if p1_score == WIN:
            win_text = "Player 1 Wins!"
        if p2_score == WIN:
            win_text = "Player 2 Wins!"

        screen.blit(huge_font.render(win_text, True, (7, 240, 7)), (screen.get_width()/2 - 160, screen.get_height() / 2 - 50))

    # flip() the display to put your work on screen
    pg.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60)
    

pg.quit()
