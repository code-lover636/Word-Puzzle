import pygame
import sys
from random import choice

pygame.init()

# screen
WIDTH, HEIGHT = 600,600
pygame.display.set_icon(pygame.image.load('assets/icon.png'))
pygame.display.set_caption("WORD PUZZLE")
BACKGROUND = pygame.image.load('assets/blue_bg.jpg')
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Varilables
word_set = [ ["COMPUTER","SOFTWARE","WEBSITE","MOUSE","KEY","TECHNOLOGY"],
             ["KANGAROO","TORTOISE","GORILLA","ZEBRA","CAT","   ANIMALS"],
             ["INCENDIO","ASCENDIO","STUPEFY","LUMOS","NOX","    SPELLS"],]

# vertical (col,row_start,row_end,index) & horizontal (row,col_start,col_end,index)
combs =[ [ ((6,1,8,2),(4,5,8,4),(9,0,8,0)), ((3,0,5,3),(8,1,9,1)) ],
         [ ((7,3,10,2),(9,7,10,4)), ((9,1,6,3),(0,0,8,0),(2,0,8,1)) ]  ]

cross_list = []
mouse = "normal"
score = 0
Tiles=[None]

# Sound
correct = pygame.mixer.Sound("assets/correct.wav")
wrong   = pygame.mixer.Sound("assets/wrong.wav")
applause = pygame.mixer.Sound("assets/applause.wav")

# TEXT
HEADING_FONT = pygame.font.Font('freesansbold.ttf', 32)
LETTER_FONT  = pygame.font.Font('freesansbold.ttf', 25)
SCORE_FONT   = pygame.font.Font('freesansbold.ttf', 20)

# Tiles
TILE_POS = [ (col,row) for row in range(80,580,50) for col in range(55,555,50)]
TILE= pygame.image.load('assets/tile.png')


# Solve button
SOLVE = pygame.image.load('assets/solve.png')
slv_cor = (500,555,10,65)


def solve():
    shuffled_list = [ letter for row in shuffled_letters for letter in row ]
    for word in words:
        for x in range(100):
            if shuffled_list[x:x+len(word)] == list(word):
                cross_list.append( (TILE_POS[x], (abs(TILE_POS[x][0]-TILE_POS[x+len(word)-1][0])+10,5))  )
            elif shuffled_list[x:x+len(word)*10:10] == list(word):
                cross_list.append( (TILE_POS[x], (5,abs(TILE_POS[x][1]-TILE_POS[x+len(word)*10-10][1])+10))  )
    heading("   You lost")
    
    
# Display window
DISPLAY = pygame.image.load('assets/display.png')

def heading(new_header):
    global header
    if new_header=="    You Won":        
        pygame.mixer.Sound.play(applause)
        pygame.mixer.music.stop()
    elif new_header=="   You lost": 
        pygame.mixer.Sound.play(correct)
        pygame.mixer.music.stop()      
    if new_header != header and (header not in ("    You Won","   You lost")): header = new_header
    


# New game button
NEW_GAME = pygame.image.load('assets/new_game.png')
ng_cor = (50,105,10,65)

def randomize():
    global shuffled_letters, words, mouse, comb, header, cross_list, already_answered, score
    mouse="normal"; cross_list = []; already_answered=[]; score = 0
    shuffled_letters =  [[choice([chr(ch) for ch in range(65,91)]) for _ in range(10)] for __ in range(10)]
    words = choice(word_set); header = words[-1]; comb = choice(combs)
    # vertical
    for ver in comb[0]:
        for c in range(ver[1],ver[2]): shuffled_letters[c][ver[0]] = words[ver[-1]][c-ver[1]]
    # horizontal
    for hor in comb[1]: shuffled_letters[hor[0]][hor[1]:hor[2]] = list(words[hor[-1]])
randomize()

def new_game():
    screen.blit(NEW_GAME,(50, 10)); screen.blit(DISPLAY, (130, 10))
    screen.blit( HEADING_FONT.render(header, True, (255,0,0)), (190,20))
    counter = 0
    for row in range(10):
        for col in range(10):
            puzzle = LETTER_FONT.render(shuffled_letters[row][col], True, (0,255,0)) 
            screen.blit(puzzle,(TILE_POS[counter][0]+13,TILE_POS[counter][1]+10))
            counter+=1


# Click and drag selection & checking answer         
selected_tile = pygame.image.load('assets/selection.png')
line = pygame.image.load('assets/line.png') 

def find_tile(mouse_pos, state):
    global posx,posy,mouse
    for pos in TILE_POS:
        if pos[0] < mouse_pos[0] < (pos[0]+45) and pos[1] < mouse_pos[1] < (pos[1]+44): mouse = state; posx,posy= pos

def score_update(right_ans,tiles=None):
    global score, Tiles
    if right_ans: 
        score += 10
        pygame.mixer.Sound.play(correct)
        pygame.mixer.music.stop()
    elif tiles != Tiles[-1] and len(already_answered) != 5: 
        score -= 5
        pygame.mixer.Sound.play(wrong)
        pygame.mixer.music.stop()
    Tiles[-1]=tiles

already_answered = []
def check_answer(stiles,direction):
    global header,cross_list,shuffled_list 
    shuffled_list = [ letter for row in shuffled_letters for letter in row ]
    flag = False
    i1 = TILE_POS.index(stiles[0])
    i2 = TILE_POS.index(stiles[1])
    if direction == "horizontal":
        # +X direction
        if i1<i2:
            for word in words:
                if list(word) == shuffled_list[i1:i2+1]: 
                    flag = True
                    if word not in already_answered:  
                        heading("  Excellent")
                        already_answered.append(word)
                        cross_list.append( (stiles[0], (abs(stiles[0][0]-stiles[1][0])+10,5)) )      
                        score_update(True)      
        # -X direction
        elif i1>i2:
            for word in words:
                if list(word) == shuffled_list[i2:i1+1]: 
                    flag = True
                    if word not in already_answered: 
                        heading("  Marvellous")
                        already_answered.append(word)
                        cross_list.append( (stiles[1], (abs(stiles[0][0]-stiles[1][0])+10,5)) )
                        score_update(True)
                                  
    elif direction == "vertical":
        # +Y direction
        if i1<i2:
            for word in words:
                if list(word) == shuffled_list[i1:i2+1:10]: 
                    flag = True
                    if word not in already_answered: 
                        heading("     Perfect")
                        already_answered.append(word)
                        cross_list.append( (stiles[0], (5,abs(stiles[0][1]-stiles[1][1])+10)) )
                        score_update(True)
        # -Y direction
        elif i1>i2:
            for word in words:
                if list(word) == shuffled_list[i2:i1+1:10]: 
                    flag = True
                    if word not in already_answered: 
                        heading(" Wonderfull")
                        already_answered.append(word)
                        cross_list.append( (stiles[1], (5,abs(stiles[0][1]-stiles[1][1])+10)) )
                        score_update(True)
                    
    if not flag: heading("    Try again"); score_update(False,(i1,i2))
    cross_list = list(set(cross_list))


stiles = [None,None]
def select():
    global stiles, mouse
    
    if   mouse == "down": stiles[0] = (posx,posy)
    elif mouse == "up": 
        stiles[1] = (posx,posy)
        # Vertical
        if stiles[0][0] == stiles[1][0]:
            for  pos in range(stiles[0][1], stiles[1][1]+50, 50):
                screen.blit(selected_tile,(stiles[1][0],pos))
            for  pos in range(stiles[1][1], stiles[0][1]+50, 50):
                screen.blit(selected_tile,(stiles[1][0],pos))
            check_answer(stiles,"vertical")
        # horizontal
        elif stiles[0][1] == stiles[1][1]:
            for  pos in range(stiles[0][0], stiles[1][0]+50, 50):
                screen.blit(selected_tile,(pos,stiles[0][1]))
            for  pos in range(stiles[1][0], stiles[0][0]+50, 50):
                screen.blit(selected_tile,(pos,stiles[0][1]))
            check_answer(stiles,"horizontal")
        
        
def cross():
    global header
    for p in cross_list:
        cross_line = pygame.transform.scale(line,p[1])
        screen.blit(cross_line,( p[0][0]+20, p[0][1]+20 ))
        
    if len(cross_list) == 5:
        heading("    You Won")


# MAIN LOOP
while 1:
    
    screen.fill((0, 0, 0))
    screen.blit(BACKGROUND, (0, 0))
    screen.blit( SCORE_FONT.render(f"SCORE:{score}", True, (245,10,5)), (WIDTH-150,HEIGHT-20))
    # displaying tiles
    for pos in TILE_POS: screen.blit(TILE, pos) 
    screen.blit(SOLVE,(500, 10))
    if mouse != "normal": select()
    new_game()
    cross()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            find_tile(pos,"down")
            if ng_cor[0]<pos[0]<ng_cor[1] and ng_cor[2]<pos[1]<ng_cor[3]: randomize()
            elif slv_cor[0]<pos[0]<slv_cor[1] and slv_cor[2]<pos[1]<slv_cor[3]: solve()
            
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            find_tile(pos,"up")
            
    pygame.display.update()