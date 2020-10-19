from pygame import Rect,Surface
from pygame import font
from pygame import  transform
class button():
    def __init__(self, x, y, width, length, text,color,pic=None):
        self.img=Surface((width,length))
        self.cover=Surface((width,length))
        self.cover.fill((0,0,0))
        self.color=color
        self.img.fill((color))
        self.x,self.y=x,y
        font1 =font.Font(font.get_default_font(), int(width*0.09))
        self.txt = font1.render(str(text), True, (255, 255, 255))
        if pic:
            pic=transform.scale(pic,(width,length),)
        self.icon=pic

    def draw_button(self, screen, posx, posy):
        self.ishover(posx,posy)
        screen.blit(self.img,(self.x,self.y))
        screen.blit(self.cover,(self.x,self.y))
        screen.blit(self.txt, (self.x + (self.img.get_size()[0] / 2 - self.txt.get_width() / 2), self.y + (self.img.get_size()[1] / 2 - self.txt.get_height() / 2)))
        if(self.icon):
            screen.blit(self.icon,(self.x + (self.img.get_size()[0] / 2 - self.icon.get_width() / 2), self.y + (self.img.get_size()[1] / 2 - self.icon.get_height() / 2)))

    def ishover(self, posx, posy):
        if (posx >= self.x and posx <= self.x + self.img.get_size()[0] and posy >= self.y and posy <= self.y + self.img.get_size()[1]):
            self.cover.set_alpha(100)
        else:
            self.cover.set_alpha(0)


    def isclicked(self, posx, posy):
        if (posx >= self.x and posx <= self.x + self.img.get_size()[0] and posy >= self.y and posy <= self.y + self.img.get_size()[1]):
            return True
        return False
