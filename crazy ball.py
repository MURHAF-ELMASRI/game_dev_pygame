import threading
import time

import pygame as pg
from os import path

from pygame.compat import geterror


def load_image(name,colorkey=None):
    fullpath=path.join("data",name)
    try:
        image=pg.transform.scale(pg.image.load(fullpath),(100,100))


    except pg.error:
        print("couldn't find image")
        raise SystemExit()
    image=image.convert_alpha()
    if(colorkey):
        if(colorkey==-1):
            print("girimis")
            image.set_alpha(0)
        image.set_colorkey(colorkey,pg.RLEACCEL)
    return image,image.get_rect()

def load_sound(name):
    fullpath=path.join("data",name)
    class Nonesound:
        def play(self): pass
    if not pg.mixer or pg.mixer.get_init():
        return Nonesound()
    try:
        sound=pg.mixer.Sound(fullpath)
    except pg.error:
        print("error")
        SystemExit((geterror()))
    return sound


class ball(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image,self.rect=load_image("head.bmp")
        self.move=9
        screen=pg.display.get_surface()
        self.area=screen.get_rect()
        self.x2=0
        self.y2=0
        self.holding=0
        self.vx=2
        self.vy=2

    def update(self):
        if self.holding:
            self._move_by_mouse()
        else:
            self._walk()


    def _walk(self):

        newpos=self.rect.move((self.vx,0))
        if(self.rect.left < self.area.left or self.rect.right > self.area.right ):
                self.vx=-self.vx
                self.image=pg.transform.flip(self.image,1,0)
                newpos=self.rect.move((self.vx,0))
        self.rect=newpos
        newpos = newpos.move((0, self.vy))
        if(newpos.top < self.area.top or newpos.bottom >self.area.bottom):
            self.vy= -self.vy
            self.image = pg.transform.flip(self.image, 0, 1)
            newpos = self.rect.move((0, self.vy))

        self.rect=newpos

    def _move_by_mouse(self):
        pos=pg.mouse.get_pos()
        self.rect.center=pos


    def let(self):
        if(self.holding):
            self.holding = 0
            self.stop=True
            print(self.vx)

    def hold(self):
        if(not self.holding):
            self.holding=1
            self.stop=False
            self.vol=threading.Thread(target=self.take_pos,args=(lambda: self.stop,),daemon=True)
            self.vol.start()

    def intersict(self):
        pos=pg.mouse.get_pos()
        mose = pg.Rect([pos[0], pos[1], 1, 1])

        if (self.rect.inflate(100,100).colliderect(mose)):
            return True
        return False

    def take_pos(self,stop):  #take postion every specific time using threading
        while(True):
            x,y=pg.mouse.get_pos()
            self.vx=(x-self.x2)//50
            self.vy=(y-self.y2)//50
            time.sleep(0.01)
            self.x2,self.y2=x,y
            if(stop()):break


def main():
    pg.init()
    screen=pg.display.set_mode((600,600))

    bg=pg.Surface(screen.get_size())
    bg.fill((60,250,200))
    bg=bg.convert()
    bal=ball()

    allsprit=pg.sprite.RenderPlain((bal))

    going=True
    while(going):
        for event in pg.event.get():
            if(event.type==pg.QUIT):
                going=False
            if(event.type==pg.MOUSEBUTTONDOWN and bal.intersict()):
                bal.hold()

            if(event.type==pg.MOUSEBUTTONUP):
                bal.let()


        allsprit.update()
        screen.blit(bg,(0,0))
        allsprit.draw(screen)
        pg.display.flip()

if(__name__=="__main__"):
    main()
