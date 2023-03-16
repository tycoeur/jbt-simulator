# -*- coding: utf-8 -*-
import glob
import math
import sys
from typing import Final

import numpy as np
import pygame
from pygame.locals import *
from mutagen.mp3 import MP3

from utils import processing_measure
from gevent import os
from utils.chart_analyzer import fumen_load, get_marker_frames


def split_image(image):
    imageList = []
    for i in range(0, PANEL_SIZE * 5, PANEL_SIZE):
        for j in range(0, PANEL_SIZE * 5, PANEL_SIZE):
            surface = pygame.Surface((PANEL_SIZE, PANEL_SIZE), SRCALPHA)
            surface.blit(image, (0, 0), (j, i, j + PANEL_SIZE, i + PANEL_SIZE))
            surface.set_colorkey((0, 0, 0), RLEACCEL)
            imageList.append(surface)
    return imageList


@processing_measure.measure
def get_nearest_value(list, num):
    """
    概要: リストからある値に最も近い値を返却する関数
    @param list: データ配列
    @param num: 対象値
    @return 対象値に最も近い値
    """
    idx = np.abs(np.asarray(list) - num).argmin()
    return list[idx]


@processing_measure.measure
def get_makers(maker_path_list: list[str]):
    makers = [split_image(pygame.image.load(maker_frame).convert_alpha()) for maker_frame in maker_path_list]
    if not makers:
        raise TypeError('maker images not found.')
    return makers


@processing_measure.measure
def play(music: str, fumen: str):
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    makers = get_makers(glob.glob(os.path.join('img', 'makers', '*.png')))
    background = pygame.image.load(os.path.join('img', 'babckgroundimages', 'blue.png')).convert()
    handclap = pygame.mixer.Sound('soundeffects/handclap.wav')
    font = pygame.font.Font(None, 24)
    notes, offset = fumen_load(fumen)

    # TODO warning, changed x and y, check I did not destroy the code :)
    PANELS: Final[list[Rect]] = [Rect(x, y, PANEL_SIZE, PANEL_SIZE)
                                 for x in range(0, WINDOW_W, PANEL_SIZE + PANEL_GAP)
                                 for y in range(0, WINDOW_H, PANEL_SIZE + PANEL_GAP)]

    TRACK_END: Final[int] = USEREVENT + 1
    pygame.mixer.music.set_endevent(TRACK_END)
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()

    start_time = pygame.time.get_ticks()
    music_length = MP3(music).info.length * 1000  # ms

    bpm = 200  # TODO 1ノーツ毎にbpmを設定する

    maker_index = 0

    BLACK: Final[Color] = (0, 0, 0)
    WHITE: Final[Color] = (255, 255, 255)
    while True:
        diff_time = pygame.time.get_ticks() - start_time
        clock.tick(30)

        # ----------------------------------------------------------------------
        # Draw background
        # ----------------------------------------------------------------------
        screen.fill(BLACK)
        bpm_time = 60 * 1000 / bpm  # 現在のbpmにおける拍動アニメーション時間
        scale = 1 + (math.cos(math.pi / 2 / bpm_time * ((diff_time + offset) % bpm_time))) / 10
        anim_background = pygame.transform.rotozoom(background, 0, scale)
        anim_x = (WINDOW_W - anim_background.get_width()) / 2
        anim_y = (WINDOW_H - anim_background.get_height()) / 2
        for panel in PANELS:
            screen.set_clip(panel)
            screen.blit(anim_background, (anim_x, anim_y))

        # ----------------------------------------------------------------------
        # Draw panels
        # ----------------------------------------------------------------------
        positions: list[int]
        frame: int
        for positions, frame in get_marker_frames(notes, diff_time):
            for position in positions:
                panel = PANELS[position - 1]
                screen.set_clip(panel)
                screen.blit(makers[maker_index][frame], (panel[0], panel[1]))
        screen.set_clip(None)

        # ----------------------------------------------------------------------
        # Process inputs
        # ----------------------------------------------------------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == TRACK_END:
                pygame.mixer.music.stop()
                pygame.mixer.music.play()
                start_time = pygame.time.get_ticks()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    set_time = x * MP3(music).info.length / WINDOW_W  # sec
                    pygame.mixer.music.play(0, set_time)
                    start_time = pygame.time.get_ticks() - set_time * 1000
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    maker_index += 1
                    maker_index %= len(makers)
                    print(maker_index)
                if event.key == K_DOWN:
                    maker_index -= 1
                    maker_index %= len(makers)
                    print(maker_index)

        # ----------------------------------------------------------------------
        # FPS and music progression
        # ----------------------------------------------------------------------
        screen.blit(font.render(f'{clock.get_fps():.2f}', True, WHITE), dest=(8, 8))
        screen.blit(font.render(f'{int(100 * diff_time / music_length)} %', True, WHITE), dest=(8, 24))

        # ----------------------------------------------------------------------
        # Draw everything
        # ----------------------------------------------------------------------
        pygame.display.update()


@processing_measure.measure
def pygame_init():
    pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.DOUBLEBUF)
    pygame.display.set_caption("jbt-simulator")
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
    pygame.font.init()


if __name__ == "__main__":
    WINDOW_W, WINDOW_H, PANEL_SIZE, PANEL_GAP = 512, 512, 110, 24
    if len(sys.argv) == 1:
        pygame_init()
        play('music/Our Faith.mp3', 'fumen/sample.jbt')
        pygame.quit()
    elif len(sys.argv) == 3:
        pygame_init()
        play(sys.argv[1], sys.argv[2])
        pygame.quit()
    else:
        print("Invalid argument error!!")
        sys.exit(1)
