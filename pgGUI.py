"""
this file manages the pygame GUI
"""


import pygame
vec2 = pygame.math.Vector2

class GUI_Element():
    def __init__(self, position:vec2, size:vec2) -> None:
        self.pos = position
        self.size = size
        self.color  = (255, 255, 255)
    def update(self, event):
        pass
    def render(self, surface:pygame.surface):
        pygame.draw.rect(surface, self.color, (self.pos.x, self.pos.y, self.size.x, self.size.y))

class GuiHandler():
    def __init__(self) -> None:
        self.gui_elements = []
        

    def get_gui_elements(self):
        if self.gui_elements == []:
            return
        return self.gui_elements
    def addElement(self, new_element):
        print(new_element)
        #self.gui_elements.append[new_element]

    def update(self, event:pygame.event):
        if self.gui_elements == []:
            return
        for elem in self.gui_elements:
            elem.update(event)
    def render(self, surface:pygame.surface):
        if self.gui_elements == []:
            return
        for elem in self.gui_elements:
            elem.render(surface)

class Button(GUI_Element):
    def __init__(self, position: vec2, size: vec2, function) -> None:
        super().__init__(position, size)
        self.function = function # function which is executed on buttonpress
        self.__isHovered = False
    
    def onPress(self):
        self.function()

    def update(self, event:pygame.event):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.isHovered = True
        else:
            self.isHovered = False

        if event == pygame.MOUSEBUTTONDOWN:
            if self.isHovered:
                print("click")
