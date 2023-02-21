"""
this file provides the logic for the binary tree being created
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
vec2 = pygame.math.Vector2

import tkinter as tk
from tkinter import simpledialog

# tkinter popup returns str input
def input_string_popup():
    root = tk.Tk()
    root.withdraw()
    result = simpledialog.askstring("Input", "Enter a string:", parent=root)
    if result == "":
        return None
    return result

class BinTree():
    def __init__(self):
        self.root = None
        self.left = None
        self.right = None

        self.depth = 0
        self.height = 0

        self.rect = None
        self.pos = None
        self.size = None

        self.zoom_horizontal = 1

        self.col_preview = (150,150,150)
        self.col_preview_hovered = (170,170,170)
        self.col_fill = (255,255,255)
        self.col_fill_hovered = (240,240,240)
        self.col_outline = (10,10,10)
        self.col_lines = (20,20,20)

        self.isHovered = False
        self.photomode = False

    # calculates the factor of the child's x distace to it's root
    def __dist_to_root(self)->int:
        # if it's an empty tree the factor is 1
        if self.root == None:
            return 1
        else:
            # else it is the distances of all children combined
            if self.left != None and self.right != None: 
                dl = self.left.__dist_to_root()
                dr = self.right.__dist_to_root()
                return max(dl, dr)*2 +1
    # called when preview / empty tree is clicked on 
    # creates left and right trees
    def __create(self)->None:
        # cancel creation if photomode is true
        if self.photomode:
            return
        # creates popup where str can be inserted/root has to be named
        # empty str input -> func returns None -> creation canceled
        self.root = input_string_popup()
        if self.root == None:
            return
        # create child obj:
        self.left = BinTree()
        self.left.pos = self.pos + vec2(-100,50)
        self.left.size = self.size
        self.left.depth = self.depth + 1
        self.right = BinTree()
        self.right.pos = self.pos + vec2(100,50)
        self.right.size = self.size 
        self.right.depth = self.depth + 1

    def toggle_photoMode(self):
        print(f"Photomode is now {self.photomode != True}")
        if self.photomode:
            self.photomode = False
            if self.root != None:
                self.left.toggle_photoMode()
                self.right.toggle_photoMode()
            return
        self.photomode = True
        if self.root != None:
                self.left.toggle_photoMode()
                self.right.toggle_photoMode()

    def delete(self):
        self.root = None

    def update(self, event)->None:
        # update self.rect
        self.rect = pygame.Rect(self.pos.x-self.size, self.pos.y-self.size, self.size*2, self.size*2)
        # get mouse position and check if self is hovered
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.isHovered = True
        else:
            self.isHovered = False
        # check if being clicked on
        if event.type == pygame.MOUSEBUTTONDOWN:
            #pygame.mouse.get_pressed(num_buttons=3)
            if pygame.mouse.get_pressed(3)[0]: # left click
                if self.isHovered:
                    if self.root == None:
                        self.__create()      
            if pygame.mouse.get_pressed(3)[1]: # middle click
                pass
            if pygame.mouse.get_pressed(3)[2]: # right click
                if self.isHovered:
                    self.delete()
    
        # update left and right
        if self.root != None:
            # update child pos
            self.left.pos = self.pos + vec2(-self.__dist_to_root()*self.size*self.zoom_horizontal, self.size * 4)
            self.right.pos = self.pos + vec2(self.__dist_to_root()*self.size*self.zoom_horizontal, self.size * 4)
            # update child 
            self.left.update(event)
            self.right.update(event)
            # update child size
            self.left.size = self.size 
            self.right.size = self.size
            self.left.zoom_horizontal = self.zoom_horizontal
            self.right.zoom_horizontal = self.zoom_horizontal
    
    def render(self, surface)->None:
        if self.pos == None or self.size == None:
            return   
        # render self:
        # checks if self is empty -> just draw previw 
        if self.root == None:
            if self.photomode is False:
                if self.isHovered:
                    pygame.draw.circle(surface, self.col_preview_hovered, self.pos, self.size) # fill preview hovered
                else:
                    pygame.draw.circle(surface, self.col_preview, self.pos, self.size) # fill preview
        else:
            # draw lines to left and right if existing
            if self.left.root != None:
                pygame.draw.line(surface, self.col_lines, self.pos, self.left.pos, self.size//7)
            if self.right.root != None:
                pygame.draw.line(surface, self.col_lines, self.pos, self.right.pos, self.size//7) 
            # draw self
            if self.isHovered:
                pygame.draw.circle(surface, self.col_fill_hovered, self.pos, self.size) # fill hovered
            else:
                pygame.draw.circle(surface, self.col_fill, self.pos, self.size) # fill
            pygame.draw.circle(surface, self.col_outline, self.pos, self.size, self.size//7) # outline
            
            # adaptive font size (if str len > 5 font size is reduced)
            font_size = self.size
            if len(self.root) > 5:
                font_size -= self.size//((self.size//2)*(len(self.root)-5))
            font = pygame.font.SysFont(None, int(font_size))
            text = font.render(self.root, True, (100,100,255))
            surface.blit(text, text.get_rect(center =  self.pos))
        # render left/right once self is created
        if self.root != None:
            self.left.render(surface)
            self.right.render(surface)