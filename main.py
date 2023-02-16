"""
This is the main script, for information on usage see README.md
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.init()
import math
from binTree import*
import random
from tkinter import * 
from tkinter import messagebox
import pgGUI
import sys



current_Version = "v1.1.3"

vec2 = pygame.math.Vector2

WIDTH, HEIGHT = 1920 , 1080
window = pygame.display.set_mode((WIDTH, HEIGHT))

# set window icon
icon_window = pygame.image.load(".\Assets\icon_Window.png")
pygame.display.set_icon(icon_window)

# set window caption
pygame.display.set_caption("")

color_bg = pygame.Color(220,220,220)#dark mode:(30,30,50)

bT = BinTree()
bT.pos = vec2(WIDTH//2, HEIGHT*0.1)
bT.size = 50

# minimum size of tree (prevent infinite zooming)
min_size = 10

# list of all systhem available fonts
allFonts = pygame.font.get_fonts()

def starting_window():
    print("starting...")
    randomFontProbability = 100 # 1  in 100
    randomNum = random.randint(1, randomFontProbability)
    shuffle_Fonts = False
    if randomNum == 50:
        shuffle_Fonts = True

    # text
    randomFont = allFonts[random.randint(0, len(allFonts)-1)]
    # appname font + text
    font1 = pygame.font.SysFont(randomFont, 150)
    text1 = font1.render('BinTree-Maker', True, (0, 0, 0))
    # creator font + text
    font2 = pygame.font.SysFont(None, 30)
    text2 = font2.render('made by Lukas Buschauer', True, (0, 0, 0))
    # version Text
    font3 = pygame.font.SysFont(None, 50)
    text3 = font3.render(current_Version, True, (0,0,0))
    # animation
    frames = 1000
    bg_brightness = (color_bg.r + color_bg.g + color_bg.b)//3
    for i in range(frames):
        if bg_brightness > 255/2:
            # starts from dark goes to bright
            brightness = int(min(255*i/frames, bg_brightness))       
        else:
            # starts from bright goes to dark
            brightness = int(max(bg_brightness, 255-(255*i/(frames))))
        # fill background
        window.fill((brightness,brightness,brightness))

        # display appname (calculated window center)
        if shuffle_Fonts:
            randomFont = allFonts[random.randint(0, len(allFonts)-1)]
            font1 = pygame.font.SysFont(randomFont, 150)
            text1 = font1.render('BinTreeMaker', True, (0, 0, 0))
        window.blit(text1, text1.get_rect(center = window.get_rect().center))
        # display creator name (bottom left)
        window.blit(text2, text2.get_rect(bottomleft = window.get_rect().bottomleft))
        # display current version (top left)
        window.blit(text3, text2.get_rect(topleft = window.get_rect().topleft))

        # update window
        pygame.display.update()

def closeApp():
    if messagebox.askquestion("Y u goin? :(", "Do You want to quit?") == "yes":
        pygame.quit()
        sys.exit()
        

def main():
    moving_tree = False
    shift_pressed = False
    ctrk_pressed = False
    
    # initialising gui handler
    GUI_handler = pgGUI.GuiHandler()
    
    # GUI-SETUP:
    #   button photomode
    gui_Button_photomode = pgGUI.Button(vec2(10,60), vec2(50,50), bT.toggle_photoMode)    #GUI_Element(vec2(10, 10), vec2(100,100))
    gui_Button_photomode.addImageBackground(pygame.image.load(".\Assets\icon_camera.png"))
    
    #   button options

        #   option window setup
    gui_Container_options = pgGUI.Container(vec2(70, 10), vec2(70,130))
    gui_Container_options.col = (250, 250, 250)

    gui_Button_options = pgGUI.Button(vec2(10,10), vec2(50,50), gui_Container_options.toggle)
    gui_Button_options.addImageBackground(pygame.image.load(".\Assets\icon_Optionwheel.png"))

    gui_Button_close = pgGUI.Button(gui_Container_options.pos+vec2(10,10), vec2(50,50),closeApp)
    gui_Button_close.addImageBackground(pygame.image.load(".\Assets\icon_Close.png"))
    gui_Container_options.addElement(gui_Button_close)

    # add gui elements to gui_handeler
    GUI_handler.gui_elements.append(gui_Button_photomode)
    GUI_handler.gui_elements.append(gui_Button_options)
    GUI_handler.gui_elements.append(gui_Container_options)

    # display starting window
    starting_window()
    print("Programm started")

    # app loop
    running = True
    while running:
        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            # update gui
            GUI_handler.update(event)

            if event.type == pygame.QUIT:
                running = False
            # Mouse Input:
            if event.type == pygame.MOUSEBUTTONUP:
                moving_tree = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(3)[1]: # middle click
                    moving_tree = True
                    mouse_tree_offset = bT.pos - vec2(mx, my)

            elif event.type == pygame.MOUSEWHEEL: # zoom
                if shift_pressed:
                    bT.zoom_horizontal = max(0.3, bT.zoom_horizontal + event.y/20)
                else:
                    if ctrk_pressed:
                        bT.size = max(min_size, bT.size + event.y)
                    else:
                        bT.size = max(min_size, bT.size + event.y*10)

            # Keyboard Input:
            if event.type == pygame.KEYDOWN: # keydown
                if event.key == pygame.K_ESCAPE: # ESC
                    closeApp()
                if event.key == pygame.K_LSHIFT: # LSHIFT
                    shift_pressed = True
                if event.key == pygame.K_LCTRL: # CTRL
                    ctrk_pressed = True
                if event.key == pygame.K_F1: # F1
                    bT.toggle_photoMode()
            if event.type == pygame.KEYUP: # keyup
                if event.key == pygame.K_LSHIFT: # LSHIFT
                    shift_pressed = False
                if event.key == pygame.K_LCTRL: # CTRL
                    ctrk_pressed = False

            bT.update(event)

        if moving_tree:
            bT.pos = vec2(mx, my) + mouse_tree_offset

        # update tree
        bT.update(event)
        # fill background
        window.fill(color_bg)

        # render tree
        bT.render(window)
        # render gui
        GUI_handler.render(window)
        
        # update display
        pygame.display.update()
    pygame.quit()

main()