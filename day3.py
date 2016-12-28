# -*- coding=utf-8 -*-
# !/usr/bin/env python

"""
获得机器支持的显示模式
>>> import pygame
>>> pygame.init()
>>> pygame.display.list_modes()

"""

import pygame
from pygame.locals import *
from sys import exit
from config import static_path

background_image_filename = static_path + '/1.jpg'


def key_f_change_size():
    """
    按f键切换全屏
    :return:
    """
    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)
    background = pygame.image.load(background_image_filename).convert()

    Fullscreen = False

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        if event.type == KEYDOWN:
            if event.key == K_f:
                Fullscreen = not Fullscreen
                if Fullscreen:
                    # 全屏显示
                    screen = pygame.display.set_mode((640, 480), FULLSCREEN, 32)
                else:
                    screen = pygame.display.set_mode((640, 480), 0, 32)

        screen.blit(background, (0, 0))
        pygame.display.update()


def bind_size():
    """
    自定义大小
    :return:
    """
    SCREEN_SIZE = (640, 480)

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)

    background = pygame.image.load(background_image_filename).convert()

    while True:

        event = pygame.event.wait()
        if event.type == QUIT:
            exit()
        if event.type == VIDEORESIZE:
            SCREEN_SIZE = event.size
            screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
            pygame.display.set_caption("Window resized to " + str(event.size))

        screen_width, screen_height = SCREEN_SIZE
        # 这里需要重新填满窗口
        for y in range(0, screen_height, background.get_height()):
            for x in range(0, screen_width, background.get_width()):
                screen.blit(background, (x, y))

        # pygame.display.update()
        pygame.display.flip()


if __name__ == '__main__':
    bind_size()
