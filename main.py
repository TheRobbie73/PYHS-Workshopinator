import pygame as pg
import sys
import fileparser

class Main():
    def __init__(self):
        self.screen = pg.display.set_mode((960, 720))
        self.clock = pg.time.Clock()
        self.quit = False

        self.data_list = fileparser.main()
        self.test = 0
        

    def main(self):
        while not self.quit:
            self.clock.tick(10)
            self.event()
            self.update()
            self.render()
    
    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True
    
    def update(self):
        self.surface = pg.surface.Surface((1880, 470))
        self.surface.fill("#000000")
        self.surface = fileparser.render_all(self.data_list, 78, self.surface)

    def render(self):
        self.screen.fill("#B744B8")

        self.screen.blit(self.surface, (-940, 10))

        pg.display.flip()

if __name__ == "__main__":
    pg.init()
    main = Main()
    main.main()
    pg.quit()
    sys.exit()