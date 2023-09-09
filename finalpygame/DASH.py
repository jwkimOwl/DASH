import os, random
import pygame
from pygame.locals import *
##############################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800 # 가로 크기
SCREEN_HEIGHT = 600 # 세로 크기
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 화면 타이틀 설정
pygame.display.set_caption("Dash!")

# FPS
clock = pygame.time.Clock()

##############################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") # images 폴더 위치 반환
Font = pygame.font.SysFont( "ariel", 60, True, False)
BigFont=pygame.font.SysFont("ariel",200,True,False)

# 배경 데이터
BACKGROUND = pygame.image.load(os.path.join(image_path, "background.png"))
TITLE_IMAGE=pygame.image.load(os.path.join(image_path, "title.png"))

# 캐릭터 데이터
CHARACTER_SPRITESHEET = pygame.image.load(os.path.join(image_path, "character.png"))
CHARACTER_IMAGES = []
for i in range(7):
    image = pygame.Surface((60,60))
    image.blit(CHARACTER_SPRITESHEET, (0,0), Rect((i%3)*60, (i//3)*60, (i%3)*60+60,(i//3)*60+60))
    image.set_colorkey((0,0,0))
    CHARACTER_IMAGES.append(image.convert_alpha())
CHARACTER_SIZE = CHARACTER_IMAGES[0].get_rect().size
CHARACTER_WIDTH = CHARACTER_SIZE[0]
CHARACTER_HEIGHT = CHARACTER_SIZE[1]
CHARACTER_X=SCREEN_WIDTH/2
CHARACTER_Y=SCREEN_HEIGHT/2
JUMPSPEED=-30
BLOCK_HEIGHT=50
BLOCK_WIDTH=100

#아이템 데이터
FASTER_ICON= pygame.image.load(os.path.join(image_path, "faster.png"))
SLOWER_ICON= pygame.image.load(os.path.join(image_path, "slower.png"))
HIGHER_ICON= pygame.image.load(os.path.join(image_path, "higher.png"))
GRAVITY_ICON= pygame.image.load(os.path.join(image_path, "gravity.png"))

#기타 데이터
GRAVITY=2.5
GAME_SPEED=2
##############################################################
# Player Class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = CHARACTER_IMAGES
        self.current_image = 0
        self.image = self.images[0].convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.xspeed=0
        self.yspeed=0
        self.x=0
        self.y=0
        self.jumping=False
        self.doublejumping=False
        self.rect = self.image.get_rect()
        self.rect[0] = CHARACTER_X - (CHARACTER_WIDTH / 2)
        self.rect[1] = CHARACTER_Y - (CHARACTER_HEIGHT /2)

    def update(self):
        if self.jumping:
            self.current_image=3
            self.image=self.images[3]
        else:
            self.current_image = (self.current_image + 1) % 7
            self.image = self.images[self.current_image]
        self.x+=self.xspeed
        self.y+=self.yspeed
        self.yspeed += GRAVITY
        #print(self.x,self.y)

    def player_draw(self, screen):
        screen.blit(self.image.convert_alpha(),(CHARACTER_X-CHARACTER_HEIGHT/2,CHARACTER_Y-CHARACTER_HEIGHT/2))

    def jump(self):
        self.yspeed+=JUMPSPEED
        if not self.jumping:
            self.jumping=True
        else:
            self.doublejumping=True

    def begin(self):
        self.current_image = (self.current_image + 1) % 7
        self.image = self.images[self.current_image]
    def change_color(self,col):
        CHARACTER_IMAGES = []
        if col=='white':
            CHARACTER_SPRITESHEET=pygame.image.load(os.path.join(image_path, "character.png"))
        if col=='red':
            CHARACTER_SPRITESHEET = pygame.image.load(os.path.join(image_path, "character_red.png"))
        if col=='green':
            CHARACTER_SPRITESHEET = pygame.image.load(os.path.join(image_path, "character_green.png"))
        if col=='yellow':
            CHARACTER_SPRITESHEET = pygame.image.load(os.path.join(image_path, "character_yellow.png"))
        if col=='purple':
            CHARACTER_SPRITESHEET = pygame.image.load(os.path.join(image_path, "character_purple.png"))
        for i in range(7):
            image = pygame.Surface((60, 60))
            image.blit(CHARACTER_SPRITESHEET, (0, 0),
                       Rect((i % 3) * 60, (i // 3) * 60, (i % 3) * 60 + 60, (i // 3) * 60 + 60))
            image.set_colorkey((0, 0, 0))
            CHARACTER_IMAGES.append(image.convert_alpha())
        self.images = CHARACTER_IMAGES

class Block(pygame.sprite.Sprite):

    def __init__(self,x,y,len,item,pl_x,pl_y):
        pygame.sprite.Sprite.__init__(self)
        self.images = CHARACTER_IMAGES
        self.current_image = 0
        self.image = self.images[0].convert_alpha()
        self.x=x
        self.y=y
        self.z=-100
        self.len=len
        self.rect = None
        self.item=item
        self.rect=None
        self.mask=None


    def update(self,pl_x,pl_y):
        self.z+=GAME_SPEED
        self.rect[0]= self.x-pl_x+CHARACTER_X-BLOCK_WIDTH/2
        self.rect[1]= self.y-pl_y+CHARACTER_Y-BLOCK_HEIGHT/2

    def begin(self,pl_x,pl_y):
        self.rect = Rect(self.x - pl_x + CHARACTER_X-BLOCK_WIDTH/2, self.y - pl_y + CHARACTER_Y-BLOCK_HEIGHT/2,
                         BLOCK_WIDTH, BLOCK_HEIGHT)

##############################################################
def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_block(pl_x,pl_y):
    item=None
    rand=random.random()
    if rand<0.05:
        item='faster'
    elif rand<0.1:
        item='slower'
    elif rand<0.15:
        item='higher'
    elif rand<0.2:
        item='gravity'
    return Block(round(pl_x/BLOCK_WIDTH)*BLOCK_WIDTH+random.randrange(-10*BLOCK_WIDTH,11*BLOCK_WIDTH,BLOCK_WIDTH),
                 round(pl_y/BLOCK_HEIGHT)*BLOCK_HEIGHT+random.randrange(-30*BLOCK_HEIGHT,31*BLOCK_HEIGHT,BLOCK_HEIGHT),
                 200*random.random()+100,item,pl_x,pl_y)

def upsidedown_player(player):
    CHARACTER_IMAGES=[]
    CHARACTER_SPRITESHEET = pygame.image.load(os.path.join(image_path, "character_purple.png"))
    for i in range(7):
        image = pygame.Surface((60, 60))
        image.blit(CHARACTER_SPRITESHEET, (0, 0),
                   Rect((i % 3) * 60, (i // 3) * 60, (i % 3) * 60 + 60, (i // 3) * 60 + 60))
        image.set_colorkey((0, 0, 0))
        CHARACTER_IMAGES.append(pygame.transform.flip(image.convert_alpha(), False, True))
    player.images = CHARACTER_IMAGES

def right_player(player):
    CHARACTER_IMAGES = []
    for i in range(7):
        image = pygame.Surface((60, 60))
        image.blit(CHARACTER_SPRITESHEET, (0, 0),
                   Rect((i % 3) * 60, (i // 3) * 60, (i % 3) * 60 + 60, (i // 3) * 60 + 60))
        image.set_colorkey((0, 0, 0))
        CHARACTER_IMAGES.append(image.convert_alpha())
    player.images = CHARACTER_IMAGES

###########################################################################
def starting():
    GAME_SPEED = 2
    JUMPSPEED = -30
    GRAVITY = 2.5
    player = Player()
    player.change_color('white')
    right_player(player)
    block_group = pygame.sprite.Group()
    coming_block_group = []
    first_block = Block(0, 150, 300, None, 0, 0)
    first_block.z = 0
    first_block.begin(0, 0)
    block_group.add(first_block)
    coming_block_group.append(first_block)
    running = True
    score=''
    while running:
        clock.tick(30)
        player.update()
        block_group.update(player.x,player.y)
        first_block.z=-100
        dict = pygame.sprite.spritecollide(player, block_group, False, pygame.sprite.collide_rect)
        for block in dict:
            if player.rect[1] < block.rect[1] and GRAVITY>0:
                player.yspeed = 0
                player.y = block.y -BLOCK_HEIGHT/2 + 1 - CHARACTER_HEIGHT / 2
        screen.blit(BACKGROUND, (0, 0))
        for block in coming_block_group:
            temppolygon = [(block.rect.left, block.rect.top),
                           (block.rect.right, block.rect.top),
                           (SCREEN_WIDTH / 2 + (block.rect.right - SCREEN_WIDTH / 2) * (max(0,block.z - block.len + 200)) / 200,block.rect.top * (max(0,200 - block.len + block.z)) / 200),
                           (SCREEN_WIDTH / 2 + (block.rect.left - SCREEN_WIDTH / 2) * (max(0,block.z - block.len + 200) )/ 200,block.rect.top * (max(0,200 - block.len + block.z)) / 200)]
            sidecol = (222, 222, 222)
            blockcol = (202, 202, 202)
            pygame.draw.polygon(screen, sidecol, temppolygon)
            pygame.draw.polygon(screen, (255, 255, 255), temppolygon, 2)
            pygame.draw.rect(screen, blockcol, block.rect)
        player.player_draw(screen)
        screen.blit(TITLE_IMAGE,(SCREEN_WIDTH/2-TITLE_IMAGE.get_width()/2,SCREEN_HEIGHT/2-TITLE_IMAGE.get_height()/2))
        screen.blit(BigFont.render(score, True, (255,255,255)),(300,400))
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    score=playing()

def playing():
    global GAME_SPEED
    global JUMPSPEED
    global GRAVITY
    GAME_SPEED = 2
    JUMPSPEED = -30
    GRAVITY = 2.5
    player=Player()
    player.change_color('white')
    block_group=pygame.sprite.Group()
    coming_block_group=[]
    first_block=Block(0,150,300,None,0,0)
    first_block.z=0
    first_block.begin(0,0)
    block_group.add(first_block)
    coming_block_group.append(first_block)
    running = True
    frame=0
    effect=None
    for _ in range(30):
        new_block = get_random_block(player.x, player.y)
        coming_block_group.append(new_block)
    while running:
        frame+=1
        clock.tick(30)
        # 2. 이벤트 처리 (키보드, 마우스 등)
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            player.x-=12
        if keys[K_RIGHT]:
            player.x+=12
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if (event.key == K_SPACE or event.key == K_UP)and (not player.doublejumping):
                    player.jump()
        if abs(player.yspeed)>100:
            pygame.QUIT
            return str(frame//10)
        if frame%30==0:
            for _ in range(15):
                new_block=get_random_block(player.x,player.y)
                coming_block_group.append(new_block)
        if effect==frame:
            GAME_SPEED=2
            JUMPSPEED=-30
            GRAVITY=2.5
            right_player(player)
            player.change_color('white')

        #충돌 처리
        player.update()
        block_group.update(player.x,player.y)
        dict = pygame.sprite.spritecollide(player, block_group, False, pygame.sprite.collide_rect)
        for block in dict:
            if player.rect[1] < block.rect[1] and GRAVITY>0:
                player.yspeed = 0
                player.y = block.y -BLOCK_HEIGHT/2 + 1 - CHARACTER_HEIGHT / 2
                player.jumping=False
                player.doublejumping=False
                if block.item != None:
                    effect=frame+200
                if block.item=='faster':
                    GAME_SPEED=3
                    JUMPSPEED=-30
                    GRAVITY=2.5
                    right_player(player)
                    player.change_color('red')
                if block.item=='slower':
                    GAME_SPEED=1
                    JUMPSPEED=-30
                    GRAVITY=2.5
                    right_player(player)
                    player.change_color('green')
                if block.item=='higher':
                    GAME_SPEED=2
                    JUMPSPEED=-50
                    GRAVITY=2.5
                    right_player(player)
                    player.change_color('yellow')
                if block.item=='gravity':
                    GAME_SPEED=3
                    GRAVITY=-2.5
                    JUMPSPEED=30
                    player.change_color('purple')
                    upsidedown_player(player)
            if player.rect[1] > block.rect[1] and GRAVITY<0:
                player.yspeed = 0
                player.y = block.y +BLOCK_HEIGHT/2 - 1 + CHARACTER_HEIGHT / 2
                player.jumping=False
                player.doublejumping=False
                if block.item != None:
                    effect=frame+200
                if block.item=='faster':
                    GAME_SPEED=3
                    JUMPSPEED=-30
                    GRAVITY=2.5
                    right_player(player)
                    player.change_color('red')
                if block.item=='slower':
                    GAME_SPEED=1
                    JUMPSPEED=-30
                    GRAVITY=2.5
                    right_player(player)
                    player.change_color('green')
                if block.item=='higher':
                    GAME_SPEED=2
                    JUMPSPEED=-50
                    GRAVITY=2.5
                    right_player(player)
                    player.change_color('yellow')
                if block.item=='gravity':
                    GAME_SPEED=2
                    GRAVITY=-2.5
                    JUMPSPEED=30
                    player.change_color('purple')
                    upsidedown_player(player)


        # 5. 화면에 그리기
        screen.blit(BACKGROUND, (0, 0))
        coming_block_group.sort(key=lambda x : -x.y)
        for block in coming_block_group:
            block.z+=GAME_SPEED
            if block.rect==None:
                temprect=pygame.Rect(SCREEN_WIDTH/2+(block.x-player.x+CHARACTER_X-SCREEN_WIDTH/2)*(block.z+100)/100-BLOCK_WIDTH*(100+block.z)/200,
                                     (block.y-player.y+CHARACTER_Y)*(block.z+100)/100-BLOCK_HEIGHT*(100+block.z)/200,
                                     max(BLOCK_WIDTH*(100+block.z)/100,0),max(BLOCK_HEIGHT*(100+block.z)/100,0))
                temppolygon=[(temprect.left,temprect.top),
                             (temprect.right,temprect.top),
                             (SCREEN_WIDTH/2+(temprect.right-SCREEN_WIDTH/2)*(max(0,block.z-block.len+200))/200,temprect.top*(max(0,200-block.len+block.z))/200),
                             (SCREEN_WIDTH/2+(temprect.left-SCREEN_WIDTH/2)*(max(0,block.z-block.len+200))/200,temprect.top*(max(0,200-block.len+block.z))/200)]
                print(temprect,temppolygon,temprect.top,temprect.top*(max(0,200-block.len+block.z))/200)
                if temprect.left>SCREEN_WIDTH/2:
                    temppolygon2=[(temprect.left,temprect.top),
                                 (temprect.left,temprect.bottom),
                                 (SCREEN_WIDTH/2+(temprect.left-SCREEN_WIDTH/2)*(max(0,block.z-block.len+200))/200,temprect.bottom*(max(0,200-block.len+block.z))/200),
                                 (SCREEN_WIDTH/2+(temprect.left-SCREEN_WIDTH/2)*(max(0,block.z-block.len+200))/200,temprect.top*(max(0,200-block.len+block.z))/200)]
                if temprect.right<SCREEN_WIDTH/2:
                    temppolygon3=[(temprect.right,temprect.top),
                                 (temprect.right,temprect.bottom),
                                 (SCREEN_WIDTH/2+(temprect.right-SCREEN_WIDTH/2)*(max(0,block.z-block.len+200))/200,temprect.bottom*(max(0,200-block.len+block.z))/200),
                                 (SCREEN_WIDTH/2+(temprect.right-SCREEN_WIDTH/2)*(max(0,block.z-block.len+200))/200,temprect.top*(max(0,200-block.len+block.z))/200)]
            else:
                temppolygon = [(block.rect.left, block.rect.top),
                               (block.rect.right, block.rect.top),
                               (SCREEN_WIDTH / 2 + (block.rect.right - SCREEN_WIDTH / 2) * (max(0,block.z - block.len + 200)) / 200,block.rect.top * (max(0,200 - block.len + block.z)) / 200),
                               (SCREEN_WIDTH / 2 + (block.rect.left - SCREEN_WIDTH / 2) * (max(0,block.z - block.len + 200) )/ 200,block.rect.top * (max(0,200 - block.len + block.z)) / 200)]
                if block.rect.left>SCREEN_WIDTH/2:
                    temppolygon2=[(block.rect.left,block.rect.top),
                                 (block.rect.left,block.rect.bottom),
                                 (SCREEN_WIDTH/2+(block.rect.left-SCREEN_WIDTH/2)*(max(0,block.z-block.len+200))/200,block.rect.bottom*(max(0,200-block.len+block.z))/200),
                                 (SCREEN_WIDTH/2+(block.rect.left-SCREEN_WIDTH/2)*(max(0,block.z-block.len+200))/200,block.rect.top*(max(0,200-block.len+block.z))/200)]
                if block.rect.right<SCREEN_WIDTH/2:
                    temppolygon3=[(block.rect.right,block.rect.top),
                                 (block.rect.right,block.rect.bottom),
                                 (SCREEN_WIDTH/2+(block.rect.right-SCREEN_WIDTH/2)*(max(0,block.z-block.len+200))/200,block.rect.bottom*(max(0,200-block.len+block.z))/200),
                                 (SCREEN_WIDTH/2+(block.rect.right-SCREEN_WIDTH/2)*(max(0,block.z-block.len+200))/200,block.rect.top*(max(0,200-block.len+block.z))/200)]
            if block.rect == None:
                sidecol=(220+2*block.z,220+2*block.z,220+2*block.z)
                blockcol=(202+2*block.z,202+2*block.z,202+2*block.z)
                if block.item=='faster':
                    sidecol = (220 + 2 * block.z, 110 + block.z, 110 + block.z)
                    blockcol = (202 + 2 * block.z, 101 + block.z, 101 + block.z)
                elif block.item=='slower':
                    sidecol = (110 + block.z, 220 + 2 * block.z, 110 + block.z)
                    blockcol = (101 + block.z, 202 + 2 * block.z, 101 + block.z)
                elif block.item=='higher':
                    sidecol = (220 + 2 * block.z, 220 + 2 * block.z, 110 + block.z)
                    blockcol = (202 + 2 * block.z, 202 + 2 * block.z, 101 + block.z)
                elif block.item=='gravity':
                    sidecol = (220 + 2 * block.z, 110 + block.z, 220 + 2 * block.z)
                    blockcol = (202 + 2 * block.z, 101 + block.z, 202 + 2 * block.z)
                pygame.draw.polygon(screen,sidecol,temppolygon)
                #print(temppolygon)
                pygame.draw.polygon(screen, (249+2*block.z,249+2*block.z,249+2*block.z), temppolygon,2)
                if temprect.left>SCREEN_WIDTH/2:
                    pygame.draw.polygon(screen, sidecol, temppolygon2)
                    pygame.draw.polygon(screen, (249+2*block.z,249+2*block.z,249+2*block.z), temppolygon2, 2)
                if temprect.right<SCREEN_WIDTH/2:
                    pygame.draw.polygon(screen, sidecol, temppolygon3)
                    pygame.draw.polygon(screen, (249+2*block.z,249+2*block.z,249+2*block.z), temppolygon3, 2)
                pygame.draw.rect(screen, blockcol, temprect)
                pygame.draw.rect(screen, (249+2*block.z,249+2*block.z,249+2*block.z), temprect,2)
                if block.item=='faster':
                    screen.blit(pygame.transform.scale(FASTER_ICON, (30*(100+block.z)/100, 30*(100+block.z)/100)).convert_alpha(),(temprect.centerx-15*(100+block.z)/100,temprect.centery-15*(100+block.z)/100))
                elif block.item=='slower':
                    screen.blit(pygame.transform.scale(SLOWER_ICON, (30*(100+block.z)/100, 30*(100+block.z)/100)).convert_alpha(),(temprect.centerx-15*(100+block.z)/100,temprect.centery-15*(100+block.z)/100))
                elif block.item=='higher':
                    screen.blit(pygame.transform.scale(HIGHER_ICON, (30*(100+block.z)/100, 30*(100+block.z)/100)).convert_alpha(),(temprect.centerx-15*(100+block.z)/100,temprect.centery-15*(100+block.z)/100))
                elif block.item=='gravity':
                    screen.blit(pygame.transform.scale(GRAVITY_ICON, (30*(100+block.z)/100, 30*(100+block.z)/100)).convert_alpha(),(temprect.centerx-15*(100+block.z)/100,temprect.centery-15*(100+block.z)/100))
                temprect=pygame.Rect(block.x-player.x+CHARACTER_X-BLOCK_WIDTH/2,block.y-player.y+CHARACTER_Y-BLOCK_HEIGHT/2,BLOCK_WIDTH,BLOCK_HEIGHT)
                pygame.draw.rect(screen,(249+2*block.z,249+2*block.z,249+2*block.z),temprect,2)
            else:
                sidecol = (222, 222, 222)
                blockcol = (202, 202, 202)
                if block.item == 'faster':
                    sidecol = (222,111,111)
                    blockcol = (202,101,101)
                elif block.item == 'slower':
                    sidecol = (111,222,111)
                    blockcol = (101,202,101)
                elif block.item == 'higher':
                    sidecol = (222,222,111)
                    blockcol = (202,202,101)
                elif block.item == 'gravity':
                    sidecol = (222,111,222)
                    blockcol = (202,101,202)
                pygame.draw.polygon(screen, sidecol, temppolygon)
                pygame.draw.polygon(screen, (255, 255, 255), temppolygon, 2)
                if block.rect.left>SCREEN_WIDTH/2:
                    pygame.draw.polygon(screen, sidecol, temppolygon2)
                    pygame.draw.polygon(screen, (255, 255, 255), temppolygon2, 2)
                if block.rect.right<SCREEN_WIDTH/2:
                    pygame.draw.polygon(screen, sidecol, temppolygon3)
                    pygame.draw.polygon(screen, (255, 255, 255), temppolygon3, 2)
                pygame.draw.rect(screen, blockcol, block.rect)
                if block.item=='faster':
                    screen.blit(pygame.transform.scale(FASTER_ICON, (30, 30)).convert_alpha(),(block.rect.centerx-15,block.rect.centery-15))
                elif block.item=='slower':
                    screen.blit(pygame.transform.scale(SLOWER_ICON, (30, 30)).convert_alpha(),(block.rect.centerx-15,block.rect.centery-15))
                elif block.item=='higher':
                    screen.blit(pygame.transform.scale(HIGHER_ICON, (30, 30)).convert_alpha(),(block.rect.centerx-15,block.rect.centery-15))
                elif block.item=='gravity':
                    screen.blit(pygame.transform.scale(GRAVITY_ICON, (30, 30)).convert_alpha(),(block.rect.centerx-15,block.rect.centery-15))
            if block.z>=0 and block.rect==None:
                block.begin(player.x,player.y)
                block_group.add(block)
                #coming_block_group.remove(block)
            if block.z-block.len>0:
                coming_block_group.remove(block)
        #block_group.draw(screen)
        #print(player.rect[0], player.rect[1], player.rect[2], player.rect[3])
        for tblock in block_group:
            if tblock.z>tblock.len:
                block_group.remove(tblock)
                continue
            #print(tblock.z,tblock.rect[0],tblock.rect[1],tblock.rect[2],tblock.rect[3])

            pygame.draw.rect(screen, (255, 0, 0), tblock.rect,2)
        screen.blit(Font.render(str(frame//10), True, (255,200,200)), (50,30))
        player.player_draw(screen)
        pygame.display.update()

starting()
pygame.quit()