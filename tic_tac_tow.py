import pygame as pg
from os import path
from random import randint
from helpfull_class import button
import random
table=list()
purple=(160, 4, 244)
black=(45, 52, 54)
white=(255,255,255)


def load_image(name,colorkey=None):
    full_name=path.join("data\\tec_tac_img\\",name)
    try:
        file=open(full_name,"r")
        image=pg.image.load(file).convert_alpha()
    except pg.error as er:
        print("can't load")
        raise SyntaxError(er)
    if colorkey:
        if colorkey==-1:
            colorkey=image.get_at((0,0))
        image.set_colorkey(colorkey,pg.RLEACCEL)
    return image,image.get_rect()

class player():
    def __init__(self,val,y,x):
        self.val=val
        name=''
        if val==1:
            circle_name=["x1.png","x2.png","x2.png"]
            name=circle_name[randint(0,2)]
        else:
            cross_name=["cercle1.png","cercle2.png","cercle3.png"]
            name=cross_name[randint(0,2)]
        self.img, self.rect = load_image(name)
        self.rect[0], self.rect[1] = x, y

#check_win_lose is a function to keep track of the location where it is possible to win or loose and tell AI function about the location
def inbound(dy,dx):
    return dx>=0 and dy>=0 and dx<3 and dy<3

def check_win_lose(turn):
    global table_matrix
    for i in range(3):
        for j in range(3):

            mark=table_matrix[i][j].val

            if  mark==turn: # for vertical,horizantal,dignosal for squares (0,0),(0,1),(1,0),(2,0),(0,2)
                
                if inbound(i+2,j+2) and table_matrix[i+1][j+1].val==mark and table_matrix[j+2][i+2].val==None:
                
                    return i+2,j+2
                elif inbound(i+2,j) and table_matrix[i+1][j].val==mark and table_matrix[i+2][j].val==None:
                   
                    return i+2,j
                elif inbound(i,j+2) and table_matrix[i][j+1].val==mark and table_matrix[i][j+2].val==None:
                    return i,j+2
                # for case where there is empty square between two for same previous mark
                elif inbound(i+2,j+2) and table_matrix[i+2][j+2].val==mark and table_matrix[i+1][j+1].val==None:
                    return i+1,j+1
                elif inbound(i,j+2) and table_matrix[i][j+2].val==mark and table_matrix[i][j+1].val==None:
                    return i,j+1
                elif inbound(i+2,j) and table_matrix[i+2][j].val==mark and table_matrix[i+1][j].val==None:
                     return  i+1,j
             # case where there it 2 marks in the last squares
                if inbound(i-2,j-2) and table_matrix[i-1][j-1].val==mark and table_matrix[i-2][j-2].val==None:
                    return i-2,j-2
                elif inbound(i-2,j) and table_matrix[i-1][j].val==mark and table_matrix[i-2][j].val==None:
                    return  i-2,j
                elif inbound(i,j-2) and table_matrix[i][j-1].val==mark and table_matrix[i][j-2].val==None:
                    return i,j-2
                elif inbound(i-2,j+2) and table_matrix[i-1][j+1].val==mark and table_matrix[i-2][j+2].val==None:
                    return i-2,j+2
                elif inbound(i+2,j-2) and table_matrix[i+1][j-1].val==mark and table_matrix[i+2][j-2].val==None:
                    return i+2,j-2
                elif inbound(i+2,j-2) and table_matrix[i+2][j-2].val==mark and table_matrix[i+1][j-1].val==None:
                    return i+1,j-1

def AI_play_o():
    global table_matrix
    turn=0
    corner=[[0,0],[0,2],[2,0],[2,2]]
    middle_m=[[0,1],[1,0],[2,1],[1,2]]
    game_turn=1         # to indicate the in wich round where in
    for i in table_matrix:
        for j in i:
            if j.val!=None:
                game_turn+=1
    y,x=0,0
    if game_turn==2:
        for i in range(len(table_matrix)):
            for j in range(len(table_matrix)):
                if table_matrix[i][j].val!=turn and table_matrix[i][j].val!=None:
                     # to check wheather the opponent on the corner or the middle 
                    if (i!=1 and j!=1 ) or (abs(i-j)==1) : # if the opponent in the corner or middle
                        y,x=1,1
                    else:
                        y,x=randint(0,2),randint(0,2)
                        corner=[[0,0],[0,2],[2,0],[2,2]]
                        random.shuffle(corner)
                        for ls in corner:
                            y,x=ls[0],ls[1]
                            if table_matrix[y][x].val==None:
                                break
                            
                    return y,x

    elif game_turn==4:
            for i in range(len(table_matrix)):
                for j in range(len(table_matrix)):
                    if(abs(i-j)==0 or abs(i-j)==2) and table_matrix[1][1].val!=abs(turn-1) and table_matrix[i][j].val!=turn and table_matrix[i][j].val!=None: # find an 1- empty 2- corner if the opponent put the mark in the corner
                        print(121)
                        y,x=randint(0,2),randint(0,2)
                        
                        random.shuffle(middle_m)
                        for ls in middle_m:
                            y,x=ls[0],ls[1]
                            if table_matrix[y][x].val==None:
                                break
                        return y,x
                    elif table_matrix[i][j].val!=turn and table_matrix[i][j].val!=None:
                        for ls in middle_m:
                            y,x=ls[0],ls[1]
                            if table_matrix[y][x].val!=turn and table_matrix[y][x].val!=None and y!=i and x!=j :
                                return y+i-1,x+j-1

                        y,x=randint(0,2),randint(0,2)
                        random.shuffle(corner)
                        for ls in corner:
                            y,x=ls[0],ls[1]
                            if table_matrix[y][x].val==None:
                                print(y,x)
                                break 
                        return y,x

plan_for_x=0
def AI_play_x():
    global table_matrix
    global plan_for_x
    turn=1
    corner=[[0,0],[0,2],[2,0],[2,2]]
    middle_m=[[0,1],[1,0],[2,1],[1,2]]
    plan3=[1,-1,1,-1,1,-1]
    game_turn=1         # to indicate the in wich round where in
    for i in table_matrix:
        for j in i:
            if j.val!=None:
                game_turn+=1
    if plan_for_x: plan_for_x=randint(1,3) 
    if game_turn==1:
        if plan_for_x==1:
            return 0,0
        elif plan_for_x==2:
            random.shuffle(corner)
            return corner[0]
        elif plan_for_x==3:
            random.shuffle(middle_m)
            return middle_m[0]
    elif game_turn==3:
        if plan_for_x==1 or plan_for_x==2:
            random.shuffle(corner)
            for ls in corner:
                if table_matrix[ls[0]][ls[1]].val==None:
                    return ls
        elif plan_for_x==3:
            for i in range(len(table_matrix)):
                for j in range(len(table_matrix)):
                    if table_matrix[i][j].val==turn:
                        return abs(i+plan3[randint(0,5)]),abs(j+plan3[randint(0,5)])
    elif game_turn==5:
            random.shuffle(corner)
            for ls in corner:
                if table_matrix[ls[0]][ls[1]].val==None:
                    return ls






def AI(turn,hard):
    global table_matrix
    
    rt=check_win_lose(turn)
    if rt!=None:
        return rt
    rt=check_win_lose(abs(turn-1))
    if rt!=None:
        return rt
    if hard:
        if turn==0:
            ls=AI_play_o()
            if ls:
                return ls
        else:
            ls=AI_play_x()
            if ls:
                return ls

                        
    y,x=randint(0,2),randint(0,2)

    while table_matrix[y][x].val!=None:
        y,x=randint(0,2),randint(0,2)

    return y,x

# table variable means the image of the table
# this function is the main game , it work every loop and takes the pos of the mouse to blit the hovering square,then return false if any change had happen to the table to switch
# to another player
# I Used the same function to control the game of one/tow player.
#We can run the one player option by passing an argument to <<computer_turn>> variable

def game(turn,posx,posy,table,computer_turn=None,hard=None):

    global table_matrix
    section_x,section_y=table[2]//3,table[3]//3

    if turn==computer_turn:
        y,x=AI(turn,hard)
        table_matrix[y][x]=player(turn,table[1]+y*section_y,table[0]+x*section_x)
        return True

    

    if posx>=table[0]+table[2] or posy>=table[1]+table[3] or posy<table[1]  or posx<table[0] :
        return False

    posx-=table[0]
    posy-=table[1]
    table_pos_x=posx//section_x
    table_pos_y=posy//section_y

    if  table_matrix[table_pos_y][table_pos_x].val!=None:
        return False
    table_matrix[table_pos_y][table_pos_x]=player(turn,table[1]+table_pos_y*section_y,table[0]+table_pos_x*section_x)
    return True


def show_tabel(screen,table,posx,posy):#it shows the table and allowed postion
    global table_matrix
    for i in table_matrix:
        for j in i:
            if(j.val==0 or j.val==1):
                screen.blit(j.img,(j.rect[0],j.rect[1]))

    if posx>=table[0]+table[2] or posy>=table[1]+table[3] or posy<table[1]  or posx<table[0] :
        return
    section_x,section_y=table[2]//3,table[3]//3
    posx-=table[0]
    posy-=table[1]
    table_pos_x=posx//section_x
    table_pos_y=posy//section_y
    if not table_matrix[table_pos_y][table_pos_x]:
    #--------
        hover=pg.Surface((section_x-50,section_y-10))
        hover.fill(purple)
        hover.set_alpha(100)
        screen.blit(hover,(table[0]+table_pos_x*section_x,table[1]+table_pos_y*section_y))

def is_inboundry(i):
    if i>= 3 or i<0:
        return False
# algorithm to test if the game have been finished or not and determent the result
#first_algorith : after reaching a cell in table we can make 3 for loop and control them using if statement to control how the we scan the vertical line
# or the horizontal line or the diagonal line

#second_algorithm: using dynamic programming to save the value of the cell we want to scant it >>>>> I have chose this the easiest one
# third_algorithm: make a lot of if-else statement : brute force algorithm

def test_game():
    global table_matrix
    t=table_matrix
    y=True

    if t[0][0].val!=None and t[0][0].val==t[0][1].val and t[0][0].val==t[0][2].val:
        return 1
    elif t[1][0].val!=None and t[1][0].val==t[1][1].val and t[1][0].val==t[1][2].val:
        return 2
    elif t[2][0].val!=None and t[2][0].val==t[2][1].val and t[2][0].val==t[2][2].val:
        return 3
    elif t[0][0].val!=None and t[0][0].val==t[1][1].val and t[0][0].val==t[2][2].val:
        return 4
    elif t[2][0].val!=None and t[2][0].val==t[1][1].val and t[2][0].val==t[0][2].val:
        return 5
    elif t[0][2].val!=None and t[0][2].val==t[1][2].val and t[0][2].val==t[2][2].val:
        return 6
    elif t[0][1].val!=None and t[0][1].val==t[1][1].val and t[0][1].val==t[2][1].val:
        return 7
    elif t[0][0].val!=None and t[0][0].val==t[1][0].val and t[0][0].val==t[2][0].val:
        return 8

    for i in t:
        for j in i:
            if j.val==None:
                y=False
    if y:
        return 'equal'
    else:
        return 0

def show_dig(win):
    if len(win)==2:
        i1,j1,i2,j2=win[0][0],win[0][1],win[1][0],win[1][1]
        if i2==i1:
            return i1+1
        elif i1>i2==1:
            if j1>j2:
                return 4
            elif j1<j2: return 5

        else:
            pass

def main():
   
    global table_matrix
    pg.init()
    screen=pg.display.set_mode((700,500))

    #------------ load the images --------------------
    player_1 = button(300, 100, 200, 100, '', white, load_image("1player_txt.png")[0])
    player_2 = button(300, 300, 200, 100, '', white, load_image("2player_txt.png")[0])
    o_pic = load_image("cercle1.png")[0]
    x_pic = load_image("x1.png")[0]
    table_img = load_image("tic_tabel.png")
    pg.display.set_icon(load_image("ticlogo.png")[0])
    logo_1_player=pg.transform.scale(load_image("1player.png")[0],(100,100))
    logo_2_player=pg.transform.scale(load_image("2player.png")[0],(100,100))
    logo_turn=load_image("turn.png")[0]
    logo_win=load_image("winer.png")[0]
    logo_turn_x=load_image("x1.png")[0]
    logo_turn_o=load_image("cercle1.png")[0]
    logo_choose=load_image("choose.png")[0]
    finish_line=None
    eqal_logo=load_image("equal.png")[0]
    hard_logo=load_image("hard.png")[0]
    easy_logo=load_image("easy.png")[0]
    #-------------------------------------------------

    table_matrix=[[ player(None,0,0) for _ in range(3)] for _ in range(3)]
    pg.display.set_caption("tic tac tow")
    going=True

    table_img[1][0],table_img[1][1]=220,80

    choose_x=button(75,200,150,150,"",purple,x_pic)
    choose_o=button(375,200,150,150,'',white,o_pic)

    easy_button=button(75,200,150,150,'',purple,easy_logo)
    hard_button=button(375,200,150,150,'',white,hard_logo)

    quit_button=button(10,420,120,70,'QUITE THE GAME',purple)
    rest_button=button(150,420,120,70,'RESTART THE GAME',purple)
    font1=pg.font.Font(pg.font.get_default_font(),20)
    txt=font1.render("choose",True,(0,0,0))
    num=1
    turn=1
    hard=0
    while(going):
        posx,posy=pg.mouse.get_pos()


        if num == 1: # the first window to choose between the 1,2 player options
            screen.fill(white)
            pg.draw.rect(screen, purple, [0, 0, screen.get_width() / 2, screen.get_height()])
            player_1.draw_button(screen, posx, posy)
            player_2.draw_button(screen, posx, posy)
            screen.blit(logo_1_player,(500,100))
            screen.blit(logo_2_player,(500,300))


        elif num == 2: # choose between x and o window
            screen.fill(white)
            pg.draw.rect(screen, purple, [0, 0, screen.get_width() / 2, screen.get_height()]) # some of user front end to beautfy the window
            screen.blit(logo_choose,(500,100))
            choose_o.draw_button(screen,posx,posy)
            choose_x.draw_button(screen,posx,posy)

        elif num==3:   # 2 player game window
            screen.fill(white)
            screen.blit(logo_turn,(20,100))
            screen.blit(logo_turn_o,(20,300)) if turn==0 else screen.blit(logo_turn_x,(20,300))
            screen.blit(table_img[0],(table_img[1][0],table_img[1][1]))
            show_tabel(screen,table_img[1],posx,posy)
            test_var=test_game()

            if test_var:
                num=4
                finish_line=load_image(str(test_var)+".png")[0]
                finish_line.set_alpha(200)
                turn += 1
                turn %= 2

        elif num==4:   #window that appear as the result of playing the game
            screen.blit(finish_line,(table_img[1][0],table_img[1][1]))
            quit_button.draw_button(screen, posx, posy)
            rest_button.draw_button(screen, posx, posy)
            if test_var!='equal':
                s=pg.Surface((200,400))
                s.fill(white)
                screen.blit(s,(0,0))
                screen.blit(logo_turn_o,(20,300)) if turn==0 else screen.blit(logo_turn_x,(20,300))
                screen.blit(logo_win, (20, 100))

        elif num == 5: # one player game window
            
            screen.fill(white)
            screen.blit(logo_turn, (20, 100))
            screen.blit(logo_turn_o, (20, 300)) if turn == 0 else screen.blit(logo_turn_x, (20, 300))
            screen.blit(table_img[0], (table_img[1][0], table_img[1][1]))
            show_tabel(screen, table_img[1], posx, posy)
            test_var = test_game()
           
            
            if test_var:
                
                num = 4
                finish_line = load_image(str(test_var) + ".png")[0]
                #finish_line.set_alpha(200)
                turn += 1
                turn %= 2
                continue

            if turn==computer_turn:
                game(turn,posx,posy,table_img[1],computer_turn,hard)
                turn+=1
                turn%=2
            
            show_tabel(screen, table_img[1], posx, posy)
        elif num==6: # to show the diffuclty option
                screen.fill(white)
                pg.draw.rect(screen, purple, [0, 0, screen.get_width() / 2, screen.get_height()]) # some of user front end to beautfy the window
                screen.blit(logo_choose,(500,100))
                easy_button.draw_button(screen,posx,posy)
                hard_button.draw_button(screen,posx,posy)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                going=False

            if event.type == pg.MOUSEBUTTONDOWN:
                if num==1:
                    if(player_1.isclicked(posx,posy)):
                        num=2
                    elif(player_2.isclicked(posx,posy)):
                        num=3

                elif num==2:
                    if choose_o.isclicked(posx,posy):
                        computer_turn=1
                        num=6
                    elif choose_x.isclicked(posx,posy):
                        computer_turn=0
                        num=6

                elif num==3:

                    if game(turn,posx,posy,table_img[1]):
                        turn+=1
                        turn%=2

                elif num==4:
                    table_matrix=[[ player(None,0,0) for _ in range(3)] for _ in range(3)]
                    if rest_button.isclicked(posx,posy):
                        turn=1
                        num=1
                        print("-----------------------------------------")
                    elif quit_button.isclicked(posx,posy):
                        pg.quit()
                        going = False

                elif num==5:
                    if game(turn,posx,posy,table_img[1],computer_turn,hard):
                        turn+=1
                        turn%=2

                elif num==6:
                    if easy_button.isclicked(posx,posy):
                        hard=0
                        num=5
                    elif hard_button.isclicked(posx,posy):
                        hard=1
                        num=5


if __name__=="__main__":
    main()