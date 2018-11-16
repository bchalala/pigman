"""
Draw rectangles in pymunk and run a simulation.
"""

"""
Derivative of the veritcal stack demo from the box2d testbed.
"""

import math

import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
from pymunk import Vec2d
import pymunk.pygame_util

#blocks tuple = (x_pos,y_pos,size_x,size_y)

class drawrects():
    def __init__(self, blocks):
        self.running = True
        self.drawing = True
        self.w, self.h = 600,600
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()
        self.blocks = blocks
        self.XPOS = 0
        self.YPOS = 1
        self.XSIZE = 2
        self.YSIZE = 3
        self.create_world()
        
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.draw_options.flags = self.draw_options.DRAW_SHAPES 

    def create_world(self):
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0.,-1000.)
        self.space.sleep_time_threshold = 0.3
        
        static_lines = [pymunk.Segment(self.space.static_body, 
            Vec2d(0,0), Vec2d(600,0), 1)]
        for l in static_lines:
            l.friction = 0.5
        self.space.add(static_lines)
        
        for b in self.blocks:
            mass = b[self.XPOS]*b[self.YPOS]
            moment = pymunk.moment_for_box(mass, (b[self.XSIZE], b[self.YSIZE]))
            body = pymunk.Body(mass, moment)
            body.position = Vec2d(b[self.XPOS], b[self.YPOS])
            shape = pymunk.Poly.create_box(body, (b[self.XSIZE], b[self.YSIZE]))
            shape.friction = 0.5
            self.space.add(body,shape)
                
        
    def update(self, dt):
        # Here we use a very basic way to keep a set space.step dt. 
        # For a real game its probably best to do something more complicated.
        step_dt = 1/250.
        x = 0
        while x < dt:
            x += step_dt
            self.space.step(step_dt)
            

    def on_draw(self):
        self.clear()
        self.fps_display.draw()  
        self.space.debug_draw(self.draw_options)

    def draw(self):
        ### Clear the screen
        self.screen.fill(THECOLORS["white"])
        
        ### Draw space
        self.space.debug_draw(self.draw_options)

        ### All done, lets flip the display
        pygame.display.flip() 

    def run(self):
        while self.running:
            self.loop() 


    def loop(self):  
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(self.screen, "box2d_pyramid.png")
            elif event.type == KEYDOWN and event.key == K_d:
                self.drawing = not self.drawing
            
        fps = 60.
        dt = 1.0/fps/5        
        self.space.step(dt)
        if self.drawing:
            self.draw()
        
        ### Tick clock and update fps in title
        self.clock.tick(fps)
        pygame.display.set_caption("fps: " + str(self.clock.get_fps()))
        

def defaultblocks():
    blocks = []
    size = 20
    for x in range(1):
        for y in range(10):
            blocks.append((300, 0 + (size/2) + y * (size), size, size))

    return blocks

def main():
    demo = drawrects(defaultblocks())
    demo.run()

if __name__ == '__main__':
    main()