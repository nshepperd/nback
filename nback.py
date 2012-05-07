#!/usr/bin/python2
# encoding: UTF-8
import pygame, os, sys, stat
import pygame.font
import pygame.gfxdraw
import time, random

def choice(set):
    return random.choice(list(set))

def message(screen, text):
    raster = font.render(text, True, (10, 255, 10))
    screen.blit(raster, ((screen.get_width() - raster.get_width()) // 2, 300 + (50 - raster.get_height()) // 2))

def square(x, y):
    px = x * 100 + 5
    py = y * 100 + 5
    return (px, py, 90, 90)

def drawsquare(screen, x, y):
    pygame.draw.rect(screen, (255, 255, 0), square(x, y))

def drawaxes(screen):
    color = (255, 255, 0, 128)
    for x in (100, 200):
        pygame.gfxdraw.vline(screen, x, 5, 295, color)
    for y in (100, 200):
        pygame.gfxdraw.hline(screen, 5, 295, y, color)

visual_points = {(0, 0), (0, 1), (0, 2), (2, 0), (2, 1), (2, 2), (1, 0), (1, 2)}
audio_points = set("AVSOMUIT")

def gentrials(n, points):
    trials = 2 + n
    tlist = []
    target = [True] * 6 + [False] * 14
    random.shuffle(target)
    for i in range(n):
        p = random.choice(list(points))
        tlist.append(p)
    for i in range(20):
        if target[i]:
            p = tlist[i]
        else:
            p = choice(points.difference({tlist[i]}))
        tlist.append(p)
    return tlist

def nback(screen, n, type):
    """An n-back session. Type determines single or double n-back"""
    trials = 20 + n
    score = 0
    visual = gentrials(n, visual_points)
    if (type > 1):
      audio = gentrials(n, audio_points)

    # Set up the screen
    drawaxes(screen)
    message(screen, "STARTING")
    pygame.display.flip()
    time.sleep(2.0)
    pygame.event.clear()

    # Draw the trials
    for i in range(trials):
        screen.fill((0, 0, 0))
        drawaxes(screen)
        message(screen, "TRIAL {0}/{1}".format(i + 1, trials))
        (x, y) = visual[i]
        drawsquare(screen, x, y)
        if (type > 1):
            os.system("espeak -w snd {0} & paplay snd &".format(audio[i]))
        pygame.display.flip()

        if (type > 1):
            time.sleep(2.500)
        else:
            time.sleep(0.500)

        screen.fill((0, 0, 0))
        drawaxes(screen)
        message(screen, "TRIAL {0}/{1}".format(i + 1, trials))
        pygame.display.flip()
        if (type == 1):
            time.sleep(2.500)
        vmark = False
        if (type > 1):
            amark = False

        # Handle keyboard input
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                # Visual
                if event.unicode == u'a':
                    vmark = True
                # Audio
                if event.unicode == u'l' and type > 1:
                    amark = True
        if i >= n:
            if vmark:
                if (visual[i] == visual[i - n]):
                    score += 1

                elif (visual[i] != visual[i - n]):
                    score -= 1

            if amark:
                if audio[i] == audio[i - n]:
                    score += 1
                else:
                    score -= 1

    screen.fill((0, 0, 0))
    drawaxes(screen)

    if (type == 1):
        message(screen, "SCORE: {0}/6".format(score))
        print "SCORE: {0}/6".format(score)
    else:
        message(screen, "SCORE: {0}/12".format(score))
        print "SCORE: {0}/12".format(score)

    pygame.display.flip()
    time.sleep(0.5)
    return score

if __name__ == '__main__':
    if not os.path.exists('snd'):    
        os.mknod('snd', stat.S_IFIFO | 0600)
    pygame.init()
    fontname = pygame.font.get_default_font()
    font = pygame.font.Font(fontname, 24)
    screen = pygame.display.set_mode((300, 350), 0, 24)

    # Dual n-back with n = 1
    nback(screen, n=1, type=2)

    ## Single n-back with n = 2
    #nback(screen, n=2, type=1)
