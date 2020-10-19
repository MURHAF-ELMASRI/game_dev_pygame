import random

import pygame as pg
from os import path
import time
from helpfull_class import button

purple=(160, 4, 244)

def load_image(name, colorkey=None):
    fullpath = path.join("data", name)
    try:
        image = pg.transform.scale(pg.image.load(fullpath), (30, 30))

    except pg.error:
        print("couldn't find image")
        raise SystemExit()
    image = image.convert_alpha()
    if (colorkey):
        if (colorkey == -1):
            image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

class Apple(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image,self.rect=load_image("apple.png")
        self.t=0
        self.eated_time=0
        screen=pg.display.get_surface()
        self.area=screen.get_rect()
        self.farx=0
        self.fary=0
        self.eatable=True
        self.dirty = 0

    def update(self):
        if(not self.eatable):
            self._time_passed()  #time pass from last eaten apple
            if(self.t>3):
                self._rand_apple()


    def _rand_apple(self):
        x,y=random.randint(10,490),random.randint(10,490)

        self.image=load_image("apple.png")[0]
        self.rect.topright=x%self.area[2],y%self.area[3]
        self.eatable=True
        self.t=0
        print("hello")

    def get_dist(self,x,y):
        self.farx,self.fary=x,y

    def _time_passed(self):
        if(not self.eatable):
            self.t=time.time()-self.eated_time

    def eated(self):
        print("eated")
        self.eated_time=time.time()
        self.eatable=False
        self.image=pg.Surface((self.image.get_size())).convert()
        self.image.fill((250, 250, 240))





class body(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("body.bmp")


class Snake(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("head.bmp")
        self.rect[0] = 360
        self.bod = [body() for _ in range(2)]

        self.bod[0].rect = self.rect.move((-20, 0))

        for i in range(1, 2):
            self.bod[i].rect = self.bod[i - 1].rect.move((-20, 0))
        self.dirc = 1
        self.dx=0
        self.dy=0
        self.doublex,self.doubley=0,0
        screen=pg.display.get_surface()
        self.area=screen.get_rect()
        self.tall=0


    def update(self):
        self._walk()
        self.dirc=5


    def move_right(self):
        self.dirc = 1

    def move_left(self):
        self.dirc = 2

    def move_up(self):
        self.dirc = 3

    def move_down(self):
        self.dirc = 4

    def _walk(self):
        for i in range(len(self.bod)-1):
            self.bod[len(self.bod)-1-i].rect=self.bod[len(self.bod)-2-i].rect
        self.bod[0].rect=self.rect
        if(self.dirc==1):
            if(self.dx==20):self.doublex=20
            if(self.dx!=-20):
                self.dx=20
                self.dy=0
        if(self.dirc==2):
            if (self.dx == -20): self.doublex = -20
            if(self.dx!=20):
                self.dx=-20
                self.dy=0
        if(self.dirc==3):
            if (self.dy == -20): self.doubley = -20
            if(self.dy!=20):
                self.dy=-20
                self.dx=0
        if(self.dirc==4):
            if (self.dy == 20): self.doubley = 20
            if(self.dy!=-20):
                self.dy=20
                self.dx=0
        self.rect=self.rect.move((self.dx+self.doublex,self.dy+self.doubley))

        self.rect[0],self.rect[1]=self.rect[0]%self.area[2],self.rect[1]%self.area[3]

        self.doublex,self.doubley=0,0
        
    def eat(self,target,g):
        resize=target.rect.inflate((-10,-10))
        if(self.rect.colliderect(resize) and target.eatable):
            target.eated()
            self.grow(g)
            return True


    def grow(self,group):
        b=body()
        b.rect=self.bod[len(self.bod)-1].rect
        self.bod.append(b)
        self.tall+=1
        group.add(self.bod)

    def eatself(self):
        for i in self.bod:
            if(self.rect.center == i.rect.center):
                return True
        return False

def gameover(screen):
    restart_but=button(200,200,100,50,"Restart",purple)
    quit_but=button(200,300,100,50,"Exit",purple)
    restart=False

    while(True):
        keys = 0
        posx,posy=pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type==pg.QUIT:
                quit()
            if(event.type==pg.MOUSEBUTTONDOWN):
                keys=event.button

        if(keys==1 and restart_but.isclicked(posx,posy)):
            restart=True
            break
        if(keys==1 and quit_but.isclicked(posx,posy)):
            pg.quit()
            quit()
        restart_but.draw_button(screen,posx,posy)
        quit_but.draw_button(screen,posx,posy)
        pg.display.flip()
        #pg.display.update([restart_but.img.get_rect(),quit_but.img.get_rect()])

    if(restart):
        main()



def main():
    pg.init()
    screen = pg.display.set_mode((500, 500))
    font=pg.font.Font(None,40)

    bg = pg.Surface(screen.get_size())
    bg = bg.convert()
    bg.fill((250, 250, 240))
    screen.blit(bg, (0, 0))

    snake = Snake()
    apple=Apple()
    going = True
    allsprite = pg.sprite.RenderPlain((apple,snake))
    allsprite.add(snake.bod)
    clock=pg.time.Clock()

    while (going):
        clock.tick(10)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False

        snake.eat(apple,allsprite)
        if(snake.eatself()):
            gameover(screen)
            going=False

        keys=pg.key.get_pressed()
        if(keys[pg.K_UP]):
            snake.move_up()
        elif(keys[pg.K_DOWN]):
            snake.move_down()
            gameover(screen)
        elif(keys[pg.K_RIGHT]):
            snake.move_right()
        elif(keys[pg.K_LEFT]):
            snake.move_left()

        txt = font.render("score: " + str(snake.tall), True, (10, 10, 10))

        allsprite.update()
        screen.blit(bg,(0,0))
        screen.blit(txt,(300,0))
        allsprite.draw(screen)

        pg.display.flip()



if (__name__ == "__main__"):
    main()
