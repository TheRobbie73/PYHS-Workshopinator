import pygame as pg
import sys
import fileparser
import slider

class Main():
    def __init__(self):
        self.screen = pg.display.set_mode((960, 720))
        self.clock = pg.time.Clock()
        self.quit = False

        self.data_meta = fileparser.main()
        self.test = 0
        
        self.graph = pg.surface.Surface((940, 470))

        self.slider = slider.IntSlider(
            pg.rect.Rect((10, 490), (293, 10)),
            (0, 155),
            "freq"
        )
        

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
            self.slider.event(event)
    
    def update(self):
        mouse_pos = pg.mouse.get_pos()
        self.slider.update(mouse_pos)
        freq = self.slider.value

        self.graph.fill("#000000")
        self.graph = fileparser.graph_all(self.data_meta, None, freq, self.graph)
        
    def render(self):
        self.screen.fill("#B744B8")

        self.screen.blit(self.graph, (10, 10))
        self.slider.render(self.screen)

        pg.display.flip()

if __name__ == "__main__":
    pg.init()
    main = Main()
    main.main()
    pg.quit()
    sys.exit()