#Eoin Minaker & Dhruvit Bhavsar
#graphics9.py

from pygame import *
from math import *
from random import *
import heapq
import collections

wave = 1
newWave = False

#y = 0.2x^2 + 10 THIS MIGHT BE THE WAY TO MAKE ZOMBIES SPAWN PER LEVEL

screen = display.set_mode((800,600))
mouse.set_visible(True)

#BACKGROUND STUFF
background = image.load('map.png').convert_alpha()
fog = image.load('fog.png')
offx = -100 #image offset
offy = -1000 #image offset
mask = image.load('mask.png')
GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)
menu = image.load('menu.png')
controls = image.load('controls.png')
end = image.load('game over.png')

#LOAD BARRICADE PICTURES FOR DIFFERENT LEVELS OF DAMAGE
barricadepic =  image.load('barricade.png')
barricadepic = transform.scale(barricadepic,(250,170))
barricade2pic = image.load('barricade2.png')
barricade2pic = transform.scale(barricade2pic,(250,170))
barricade3pic = image.load('barricade3.png')
barricade3pic = transform.scale(barricade3pic,(250,170))


rightbarricadepic =  image.load('barricade.png')
rightbarricadepic = transform.scale(barricadepic,(250,170))
rightbarricadepic = transform.rotate(barricadepic,270)
rightbarricade2pic = image.load('barricade2.png')
rightbarricade2pic = transform.scale(barricade2pic,(250,170))
rightbarricade2pic = transform.rotate(barricade2pic,270)
rightbarricade3pic = image.load('barricade3.png')
rightbarricade3pic = transform.scale(barricade3pic,(250,170))
rightbarricade3pic = transform.rotate(barricade3pic,270)

botbarricadepic =  image.load('barricade.png')
botbarricadepic = transform.scale(barricadepic,(250,170))
botbarricadepic = transform.rotate(barricadepic,180)
botbarricade2pic = image.load('barricade2.png')
botbarricade2pic = transform.scale(barricade2pic,(250,170))
botbarricade2pic = transform.rotate(barricade2pic,180)
botbarricade3pic = image.load('barricade3.png')
botbarricade3pic = transform.scale(barricade3pic,(250,170))
botbarricade3pic = transform.rotate(barricade3pic,180)

leftbarricadepic =  image.load('barricade.png')
leftbarricadepic = transform.scale(barricadepic,(250,170))
leftbarricadepic = transform.rotate(barricadepic,90)
leftbarricade2pic = image.load('barricade2.png')
leftbarricade2pic = transform.scale(barricade2pic,(250,170))
leftbarricade2pic = transform.rotate(barricade2pic,90)
leftbarricade3pic = image.load('barricade3.png')
leftbarricade3pic = transform.scale(barricade3pic,(250,170))
leftbarricade3pic = transform.rotate(barricade3pic,90)




#MUSIC
mixer.init()
mixer.music.load("music.mp3")
shot = mixer.Sound('pistolshot.wav')
reload = mixer.Sound('pistolreload.wav')
mixer.music.play()

#SHOOTING
crosshair = image.load('crosshair.png')
crosshair = transform.scale(crosshair,(32,32))
active_bullets = []
clip = 16 #max clip size
reload_time = 120 #time it takes to reload
reload_ticks = 0  #the counter for reload timer
start_reload = False #whether or not they have started reloading
gun = "pistol" #your active gun
gun_dmg = 18
rifle = False #if certain guns are unlocked or not
shotgun = False
gun_selection = True #if there is more than just the pistol available
guns = ['pistol'] #list of the guns the player owns
switching_guns = False
bulletimg = image.load('bullet.png')
#SPRITES FOR DIFFERENT GUNS
rotBullet = 0
pistolmove = []
shotgunmove = []
riflemove = []

for i in range(0,19): 
    pistolmove.append(image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_%d.png" % (i)))
    shotgunmove.append(image.load("Top_Down_Survivor/shotgun/move/survivor-move_shotgun_%d.png" % (i)))
    riflemove.append(image.load("Top_Down_Survivor/rifle/move/survivor-move_rifle_%d.png" % (i)))


#ROOMS AND DOORS AND BARRICADES

barricade3 = (680,890) #horiz top
barricade4 = (1280,900) #horiz top
barricade5 = (1640,900) #horiz top
barricade10 = (2450,1060) # horz top
barricade9 = (3660,1500) #vert right
barricade12 = (3700,1860) # vert right
barricade11 = (3140,2560) #horiz bot
barricade8 = (1780,3420) #horiz bot
barricade7 = (920,3150) #horiz bot
barricade6 = (350,2820) #vert left
barricade2 = (350,1900) #vert left
barricade1 = (350,1180) #vert left
spawn1 = (20,1180)
spawn2 = (20,1900)


b1_health = 100 #barricades' health
b2_health = 100
spawn3 = (680,20)

b3_health = 100
room1 = False
spawn4 = (1280,20)

b4_health = 100
spawn5 = (1640,20)

b5_health = 100
room2 = False
spawn6 = (20,2820)

b6_health = 100
room3 = False
spawn7 = (3980,3150)

b7_health = 100
spawn8 = (3980,3420)

b8_health = 100
spawn9 = (3980,1500)

b9_health = 100
spawn10 = (20,1060)

b10_health = 100
room4 = False
room5 = False
spawn11 = (3140,3980)

b11_health = 100
room6 = False
room7 = False
spawn12 = (3980,1860)

b12_health = 100
room8 = False


spawn_points = [spawn1,spawn2,spawn3,spawn4,spawn5,spawn6,spawn7, #POSSIBLE SPAWN POINTS FOR ENEMIES
spawn8,spawn9,spawn10,spawn11,spawn12,(2000,2000),(500,1600)]
#SORT BARRICADES
topbarricades = [barricade3,barricade4,barricade5,barricade10]
rightbarricades = [barricade9,barricade12]
botbarricades = [barricade11,barricade8,barricade7]
leftbarricades = [barricade6,barricade2,barricade1]
barricades = [barricade1,barricade2,barricade3,barricade4,barricade5,
barricade6,barricade7,barricade8,barricade9,barricade10,barricade11,barricade12]


barricade_health = [1000,1000,1000,1000,1000,1000,
1000,1000,1000,1000,1000,1000]

game_timer = 0 #TIME FOR WAVES
#CLASS FOR DRAWING BULLETS
class Bullet:
    "x,y,mx,my,speed,offx,offy"
    def __init__(self,x,y,mx,my,speed,offx,offy):
        self.x = x
        self.y = y
        self.mx = mx
        self.my = my
        self.speed = speed
        bulletx_big = mx - offx - x #the total distance between guy and crosshair
        bullety_big = my - offy - y
        self.bulletx_small = speed*(bulletx_big /hypot(bulletx_big,bullety_big)) #for a hypotenuse of one
        self.bullety_small = speed*(bullety_big /hypot(bulletx_big,bullety_big)) #but also factoring speed of bullet
        self.clip = 16
        self.angle = degrees(atan2(mx-self.x-offx,self.my-self.y-offy)) #angle between player and mouse
    def move(self):
        self.x += self.bulletx_small
        self.y += self.bullety_small
        if self.x > 4000 - 50: 
            return False
        elif self.x < 0 + 50: #if the bullets go off the screen
            return False
        elif self.y < 0 + 50:
            return False
        elif self.y > 4000 - 50:
            return False
    def drawBullet(self,offx,offy):
        rotBullet = transform.rotozoom(bulletimg,self.angle,1) #rotates and scales bullet
        screen.blit(rotBullet,(self.x+offx-rotBullet.get_width()//2,self.y+offy-rotBullet.get_height()//2))

#CLASS FOR RELOADING AND KEEPING TRACK OF AMMO
class Ammo:
    "clip size, and time it takes to reload"
    def __init__(self,clip,reload_time):
        self.original_clip = clip
        self.clip = clip
        self.reload_time = reload_time
    def reload(self):
        self.clip = self.original_clip 

#CLASS FOR THE PLAYER        
class Player:
    "starting x, y,speed,damage"
    def __init__(self,x,y,speed,angle,damage,health):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = 0
        self.health = health
        self.damage = damage
    def move(self,keys):
        global movepics, frame
        self.angle = degrees(atan2(mx-self.x-offx,my-self.y-offy))-90
        if keys[K_d]:
            if mask.get_at((self.x+64,self.y)) != GREEN and mask.get_at((self.x+64,self.y)) != RED: 
                if self.x < 4000 - 10:
                    self.x += self.speed 
        if keys[K_a]:
            if mask.get_at((self.x-64,self.y)) != GREEN and mask.get_at((self.x-64,self.y)) != RED:
                if self.x > 0 + 10: 
                    self.x -= self.speed
        if keys[K_s]:
            if mask.get_at((self.x,self.y+64)) != GREEN and mask.get_at((self.x,self.y+64)) != RED:
                if self.y < 4000 - 10:
                    self.y += self.speed
        if keys[K_w]:
            if mask.get_at((self.x,self.y-64)) != GREEN and mask.get_at((self.x,self.y-64)) != RED:
                if self.y > 0 + 10:
                    self.y -= self.speed
        if keys[K_d] or keys[K_a] or keys[K_s] or keys[K_w]:
            frame += 1 #advances sprites
        if frame >= len(movepics):
            frame = 1
    def drawPlayer(self,offx,offy):
        global rotPlayer
        pic = (movepics)[frame]
        rotPlayer = transform.rotozoom(pic,self.angle,1) #ROTATE
        screen.blit(rotPlayer,(self.x+offx-rotPlayer.get_width()//2,self.y+offy-rotPlayer.get_height()//2))
        draw.rect(screen,(255,0,0),(30,30,3.5*100,10)) #health bar
        if self.health > 0:
            draw.rect(screen,(0,255,0),(30,30,3.5*self.health/10,10))
        if self.health <= 0: #DEATH SCREEN
            screen.blit(end,(0,0))
 
#CLASS FOR THE ZOMBIES
class Enemy:
    def __init__(self,x,y,speed,damage,health):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.health = health
        self.moved = False #if they have made a movement in any direction
        self.finding_door = False
        self.angle = 0
        self.closest_door = 0
        self.closest_barricade = 0
        self.not_breaking = False #the barricades
        self.got_in = False
        self.stuck = False
        self.distance = []
        self.doors = [(800,2780),(1010,1540),(1260,1400),(1290,2090),(2020,1400),
(2060,2360),(2460,1650),(3400,1400),(3300,2400),(3140,1640),(1010,1160),
(1830,1200),(2350,1240),(2810,1210),(3460,1640),(3310,1740),(2060,1800),
(2380,2570),(1820,2380),(1840,1780),(1500,1630),(1540,2560),(1010,2090),
(540,2270)]
        self.removedDists = []
        self.removedDoors = []
    def findAngle(self):
        if self.finding_door:
            if self.closest_door != 0:
                self.angle = degrees(atan2(self.closest_door[0]-self.x,self.closest_door[1]-self.y)) - 180
        else:
            self.angle = degrees(atan2(player.x-self.x,player.y-self.y)) - 180
    def get_in(self,barricades):
        if not self.got_in:
            global barricade_health
            distance = []
            distance_entry = []
            for i in barricades:
                distance.append(((i[0]-self.x)**2 + (i[1]-self.y)**2)**0.5)
            self.closest_barricade = barricades[distance.index(min(distance))]
            not_breaking = False
            if self.x < self.closest_barricade[0]:
                if mask.get_at((self.x+10,self.y)) != RED:
                        self.x += self.speed
                        self.not_breaking = True
            if self.x > self.closest_barricade[0]:
                    if mask.get_at((self.x-10,self.y)) != RED:
                        self.x -= self.speed
                        self.not_breaking = True
            if self.y < self.closest_barricade[1]:
                    if mask.get_at((self.x,self.y+10)) != RED:
                        self.y += self.speed
                        self.not_breaking = True
            if self.y > self.closest_barricade[1]:
                    if mask.get_at((self.x,self.y-10)) != RED:
                        self.y -= self.speed
                        self.not_breaking = True
            else:
                self.not_breaking = False
        if self.not_breaking == False:
            if barricade_health[barricades.index(self.closest_barricade)] <= 0:
                self.got_in = True
                self.move(player.x,player.y)
                return False
            else:
                barricade_health[barricades.index(self.closest_barricade)] -= self.damage

    def find_door(self):
        if self.finding_door:
            self.stuck = True
            self.moved = False
            self.distance = [] #for calculating the distance from the doors at the current time
            for i in self.doors:
                self.distance.append(((i[0]-self.x)**2 + (i[1]-self.y)**2)**0.5)
            self.closest_door = self.doors[self.distance.index(min(self.distance))]

            if self.x < self.closest_door[0]:
                if mask.get_at((self.x+40,self.y)) != GREEN:
                        self.x += self.speed
                        self.stuck = False
                        self.moved = True
            if self.x > self.closest_door[0]:
                    if mask.get_at((self.x-40,self.y)) != GREEN:
                        self.x -= self.speed
                        self.stuck = False
                        self.moved = True
            if self.y < self.closest_door[1]:
                    if mask.get_at((self.x,self.y+40)) != GREEN:
                        self.y += self.speed
                        self.stuck = False
                        self.moved = True
            if self.y > self.closest_door[1]:
                    if mask.get_at((self.x,self.y-40)) != GREEN:
                        self.y -= self.speed
                        self.stuck = False
                        self.moved = True

            if self.moved==False:
                if len(self.distance) > 1 and len(self.doors) > 1:
                    self.removedDists.append(self.distance[self.distance.index(min(self.distance))])
                    self.removedDoors.append(self.doors[self.distance.index(min(self.distance))])
                    del self.distance[self.distance.index(min(self.distance))]
                    del self.doors[self.distance.index(min(self.distance))]
            #print (self.stuck)
            if abs(self.x-self.closest_door[0]) < 10 and abs(self.y-self.closest_door[1]) < 10:
                self.finding_door = False
                self.moved = False
                for i in range(len(self.removedDists)):
                    self.doors.append(self.removedDoors[i])
                    self.distance.append(self.removedDists[i])
                return False
    def move(self,playerx,playery):
        self.moved = False
        if self.finding_door == False:
            if not hitbox.collidepoint((self.x,self.y)):
                if self.x < playerx:
                    if mask.get_at((self.x+40,self.y)) != GREEN and mask.get_at((self.x+40,self.y)) != BLACK :
                        self.x += self.speed
                        self.moved = True
                if self.x > playerx:
                    if mask.get_at((self.x-40,self.y)) != GREEN and mask.get_at((self.x-40,self.y)) != BLACK:
                        self.x -= self.speed
                        self.moved = True
                if self.y < playery:
                    if mask.get_at((self.x,self.y+40)) != GREEN and mask.get_at((self.x,self.y+40)) != BLACK:
                        self.y += self.speed
                        self.moved = True
                if self.y > playery:
                    if mask.get_at((self.x,self.y-40)) != GREEN and mask.get_at((self.x,self.y-40)) != BLACK:
                        self.y -= self.speed
                        self.moved = True
            if hitbox.collidepoint((self.x,self.y)):
                self.moved = True
            if self.moved == False:
                self.finding_door = True
            
    def drawEnemy(self,offx,offy,angle):
        rotZombie = transform.rotozoom(zombieimg,self.angle,1)
        screen.blit(rotZombie,(self.x+offx-rotZombie.get_width()//2,self.y+offy-rotZombie.get_height()//2))
    def attack(self):
        if hitbox.collidepoint(self.x,self.y):
            player.health -= self.damage

def makeMove(start,end):
    movepics = []
    for i in range(start,end+1):
        movepics.append(image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_%d.png" % (i)))
    return movepics


frame = 0
movepics = 0
rotPlayer = 0 #rotation for the character
player = Player(500,1300,4,0,gun_dmg,1000)
rotZombie = 0
zombieimg = image.load('Zombies/citizenzombie1.png')
zombies = []
for i in range(10):
    spawn_place = choice(spawn_points)
    zombies.append(Enemy(spawn3[0],spawn3[1],randint(4,5),0.5,randint(15,20)))

ammo = Ammo(16,reload_time)
open_doors = [(800,2780),(1010,1540),(1260,1400),(1290,2090),(2020,1400),
(2060,2360),(2460,1650),(3400,1400),(3300,2400),(3140,1640),(1010,1160),
(1830,1200),(2350,1240),(2810,1210),(3460,1640),(3310,1740),(2060,1800),
(2380,2570),(1820,2380),(1840,1780),(1500,1630),(1540,2560),(1010,2090),
(540,2270)]
paused = True
main_menu = True
controls_menu = False

play_button = Rect(300,250,200,50)
controls_button = Rect(300,300,200,50)
quit_button = Rect(300,350,200,50)

running = True
myClock = time.Clock()
while running:
    click = False
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            click = True
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    edgepan = False
    keys = key.get_pressed()
    if main_menu:
        screen.blit(controls,(0,0))
        if mb[0]:
            paused = False
            main_menu = False
        display.flip()
        
    if not paused:
        if newWave == True:
            wave += 1
            for i in range(int(0.2*(wave**2) + 10)):
                spawn_place = choice(spawn_points)
                zombies.append(Enemy(spawn_place[0],spawn_place[1],randint(3,5),1+wave/20,randint(15,25)+wave*2))
            newWave = False
        player = Player(player.x,player.y,10,player.angle,gun_dmg,player.health)

        #DOORS AND BARRICADES AND ROOMS
        if room1:
            if spawn4 not in spawn_points and spawn5 not in spawn_points:
                spawn_points.append(spawn4,spawn5)
                barricades.append(barricade4,barricade5)
                barricade_health.append(100,100)
        if room2:
            if spawn6 not in spawn_points:
                spawn_points.append(spawn6)
                barricades.append(barricade6)
                barricade_health.append(100)
        if room3:
            if spawn7 not in spawn_points and spawn8 not in spawn_points and spawn9 not in spawn_points and spawn10 not in spawn_points:
                spawn_points.append(spawn7,spawn8,spawn9,spawn10)
                barricades.append(barricade7,barricade8,barricade9,barricade10)
                barricade_health.append(100,100,100,100)
        if room5:
            if spawn11 not in spawn_points:
                spawn_points.append(spawn11)
                barricades.append(barricade11)
                barricade_health.append(100)
        if room7:
            if spawn12 not in spawn_points:
                spawn_points.append(spawn12)
                barricades.append(barricade12)
                barricade_health.append(100)
        
        #GUN SELECTION ETC
        if rifle:
            if 'rifle' not in guns:
                guns.append('rifle')
        if shotgun:
            if 'shotgun' not in guns:
                guns.append('shotgun')
        if gun == 'pistol':
            gun_dmg = 8
            movepics = pistolmove
        if gun == 'rifle':
            gun_dmg = 6
            movepics = riflemove
        if gun == 'shotgun':
            gun_dmg = 21
            movepics = shotgunmove
        if gun_selection:
            if keys[K_e] and switching_guns == False:
                switching_guns = True
                if guns.index(gun) + 1 <= len(guns) - 1:
                    gun = guns[guns.index(gun)+1] #the next gun in the list
                else:
                    gun = guns[0]
            if keys[K_q] and switching_guns == False:
                switching_guns = True
                if guns.index(gun) - 1 >= 0:
                    gun = guns[guns.index(gun)-1]
                else:
                    gun = guns[len(guns)-1]
            if keys[K_q] == False and keys[K_e] == False:
                switching_guns = False

        #BASIC STUFF
        screen.blit(background,(offx,offy))
        screen.blit(fog,(offx,offy))
        screen.blit(crosshair,(mx-16,my-16))
        hitbox = Rect(player.x-40,player.y-40,80,80)
        for i in topbarricades:
            if barricade_health[topbarricades.index(i)] > 500:
                screen.blit(barricadepic,(i[0]+offx-125,i[1]+offy-85))
            elif 0 < barricade_health[topbarricades.index(i)] <= 500:
                screen.blit(barricade2pic,(i[0]+offx-125,i[1]+offy-85))
            elif barricade_health[topbarricades.index(i)] <= 0:
                screen.blit(barricade3pic,(i[0]+offx-125,i[1]+offy-85))
        for i in rightbarricades:
            if barricade_health[rightbarricades.index(i)] > 500:
                screen.blit(rightbarricadepic,(i[0]+offx-85,i[1]+offy-125))
            elif 0 < barricade_health[rightbarricades.index(i)] <= 500:
                screen.blit(rightbarricade2pic,(i[0]+offx-85,i[1]+offy-125))
            elif barricade_health[rightbarricades.index(i)] <= 0:
                screen.blit(rightbarricade3pic,(i[0]+offx-85,i[1]+offy-125))
        for i in botbarricades:
            if barricade_health[botbarricades.index(i)] > 500:
                screen.blit(botbarricadepic,(i[0]+offx-125,i[1]+offy-85))
            elif 0 < barricade_health[botbarricades.index(i)] <= 500:
                screen.blit(botbarricade2pic,(i[0]+offx-125,i[1]+offy-85))
            elif barricade_health[botbarricades.index(i)] <= 0:
                screen.blit(botbarricade3pic,(i[0]+offx-125,i[1]+offy-85))
        for i in leftbarricades:
            if barricade_health[leftbarricades.index(i)] > 500:
                screen.blit(leftbarricadepic,(i[0]+offx-85,i[1]+offy-125))
            elif 0 < barricade_health[leftbarricades.index(i)] <= 500:
                screen.blit(leftbarricade2pic,(i[0]+offx-85,i[1]+offy-125))
            elif barricade_health[leftbarricades.index(i)] <= 0:
                screen.blit(leftbarricade3pic,(i[0]+offx-85,i[1]+offy-125))

        #SPAWNING ENEMIES
        for i in zombies:
            if i.health <= 0:
                zombies.remove(i)
            else:
                if len(zombies) > 0:
                    i.findAngle()
                    i.drawEnemy(offx,offy,i.angle)
                    i.get_in(barricades)
                    i.find_door()
                    i.attack()

        #MOVEMENT FOR CHARACTERS
        player.move(keys)
        player.drawPlayer(offx,offy)

        #CENTER ON PLAYER
        if keys[K_SPACE]:
            edgepan = False
            offxdist = player.x #x distance from edge of map to player
            offydist = player.y #y distance from edge of map to player
            centerxdist = 400 + abs(offx) #x distance from center of window to edge
            centerydist = 300 + abs(offy) #y distance from center of window to edge
            off_centerx = offxdist - centerxdist
            off_centery = offydist - centerydist
            if offx - off_centerx > -3200 and offx - off_centerx < 0:
                offx -= off_centerx
            if offy - off_centery > -3400 and offy - off_centery < 0:
                offy -= off_centery
            if offx - off_centerx < -3200:
                offx = -3200
            if offx - off_centerx > 0:
                offx = 0
            if offy - off_centery < -3400:
                offy = -3400
            if offy - off_centery > 0:
                offy = 0
        #EDGEPAN
        if edgepan:
            if mx > 750:
                if offx > -3200:
                    offx -= 10
            if mx < 50:
                if offx < 0:
                    offx += 10
            if my > 550:
                if offy > -3400:
                    offy -= 10
            if my < 50:
                if offy < 0:
                    offy += 10
        
        #SHOOTING AND OTHER GUN RELATED STUFF

        bx = player.x + 50*cos(radians(-player.angle+30))
        by = player.y + 50*sin(radians(-player.angle+30))
        if start_reload == False:
            if click:
                if ammo.clip > 0:

                    
                    active_bullets.append(Bullet(bx,by,mx,my,20,offx,offy))
                    ammo.clip -= 1
                else:
                    start_reload = True
                    if reload_ticks == reload_time:
                        ammo.reload()
                        reload_ticks = 0
                        reload_start = False
        for i in range(len(active_bullets)-1,-1,-1):
            if active_bullets[i].move() == False:
                del active_bullets[i]
            else: #checking each direction the bullet could be going
                active_bullets[i].drawBullet(offx,offy)
                if active_bullets[i].bulletx_small > 0 and active_bullets[i].bullety_small > 0:
                    if mask.get_at((int(active_bullets[i].x+active_bullets[i].speed),(int(active_bullets[i].y+active_bullets[i].speed)))) == GREEN:
                        del active_bullets[i]
                elif active_bullets[i].bulletx_small < 0 and active_bullets[i].bullety_small > 0:
                    if mask.get_at((int(active_bullets[i].x-active_bullets[i].speed),(int(active_bullets[i].y+active_bullets[i].speed)))) == GREEN:
                        del active_bullets[i]
                elif active_bullets[i].bulletx_small < 0 and active_bullets[i].bullety_small < 0:
                    if mask.get_at((int(active_bullets[i].x-active_bullets[i].speed),(int(active_bullets[i].y-active_bullets[i].speed)))) == GREEN:
                        del active_bullets[i]
                elif active_bullets[i].bulletx_small > 0 and active_bullets[i].bullety_small < 0:
                    if mask.get_at((int(active_bullets[i].x+active_bullets[i].speed),(int(active_bullets[i].y-active_bullets[i].speed)))) == GREEN:
                        del active_bullets[i]
                for i in active_bullets:
                        for j in zombies:
                            if abs(i.x - j.x) < 25 and abs(i.y - j.y) < 25:
                                if i in active_bullets:
                                    j.health -= player.damage
                                    active_bullets.remove(i) 
        if keys[K_r]:
            if ammo.clip < clip:
                start_reload = True

        if reload_ticks == reload_time:
            ammo.reload()
            reload_ticks = 0
            start_reload = False

        if start_reload == True:
            reload_ticks += 1


        if game_timer == 1800:
            newWave = True
            game_timer = 0

        #QUITTING THE GAME
        if keys[K_ESCAPE]:
            quit()
        game_timer += 1

        display.flip()
        myClock.tick(60)
        
quit()
