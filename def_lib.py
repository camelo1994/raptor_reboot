import pygame
from render import *

def create_text(str,ttf_file,size,color,cx,cy):
    #print('loading file: ' + ttf_file)
    font=pygame.font.Font(ttf_file,size)
    text=font.render(str, 1, color)
    textpos=text.get_rect(centerx=cx,centery=cy)
    return text,textpos

    