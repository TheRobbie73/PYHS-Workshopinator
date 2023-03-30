import pygame, numpy

SLIDER_WIDTH = 10

class Slider():
    def __init__(
        self,
        rect: pygame.rect.Rect,
        range: tuple[float, float]
    ):
        self.rect = rect
        self.range = range

        self.value = range[0]
        self.state: int = 0
        self.alt_value: str = ""
        self.hover: bool = False

        self.adjust_rect()
    
    def event(self, event: pygame.event.Event):
        self.state_process(event)
        if event.type == pygame.KEYDOWN and self.state == 2: self.text_input(event)
    
    def update(self, mouse_pos: tuple[int, int]):
        self.hover = self.rect.collidepoint(mouse_pos)
        if self.state == 1: self.pos_to_value(mouse_pos)
        self.clamp()
    
    def render(self, screen: pygame.surface.Surface):
        ratio = (self.rect.width - SLIDER_WIDTH) / (self.range[1] - self.range[0])
        pygame.draw.rect(
            screen, 
            "#62586C", 
            self.rect, 
            border_radius = int(SLIDER_WIDTH/2)
        )
        pygame.draw.circle(
            screen, 
            "#E8B9D4",
            (
                self.rect.left + int(self.rect.height/2 + (self.value - self.range[0]) * ratio), 
                self.rect.centery
            ),
            int(SLIDER_WIDTH/2)
        )
    


    def adjust_rect(self):
        self.rect.height = SLIDER_WIDTH

    def state_process(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover:
                if event.button == 1: self.state = 1
                if event.button == 3: 
                    self.state = 2
                    self.alt_value = ""
            else:
                if self.state == 2 and event.button in {1, 3}: self.state = 0
        if event.type == pygame.MOUSEBUTTONUP:
            if self.state == 1 and event.button == 1: self.state = 0
    
    def text_input(self, event: pygame.event.Event):
        whitelist = "-1234567890."
        if event.key == pygame.K_RETURN:
                self.check_input()
                self.state = 0
        elif event.key == pygame.K_BACKSPACE:
                self.alt_value = self.alt_value[:-1]
        elif (event.unicode in whitelist) or (whitelist == ""):
                self.alt_value += event.unicode

    def pos_to_value(self, mouse_pos: tuple[int, int]):
        ratio = (self.rect.width - SLIDER_WIDTH) / (self.range[1] - self.range[0])
        self.value = (mouse_pos[0] - (self.rect.left + self.rect.height / 2)) / ratio + self.range[0]
        
    def clamp(self):
        if self.value > self.range[1]:
            self.value = self.range[1]
        if self.value < self.range[0]:
            self.value = self.range[0]
    
    def check_input(self):
        try:
            self.value = float(self.alt_value)
        except:
            pass # throw error or something idk lol

class IntSlider(Slider):
    def pos_to_value(self, mouse_pos: tuple[int, int]):
        super().pos_to_value(mouse_pos)
        self.value = int(self.value)

    def check_input(self):
        try:
            self.value = int(self.alt_value)
        except:
            pass # throw error or something idk lol