import mouse_spots,colors,def_lib,render,sound_engine
import sqlite3,pygame,pyganim,random,colorama,copy,math,csv
from render import *
from sound_engine import *
from colorama import Fore
from copy import copy

data_db=None
data_db_cursor=None
items_db=None
items_db_cursor=None
shop_magazine=[]
shop_description_lines=[]
big_boom_list=[]
sprites_dict={}
audio_dict={}
enemy_dict={}
items_dict={}

SFXVOL=None
BGMVOL=None
enable_shadows=None
sresH=None
sresV=None


#######################################
######### INICIALIZAÇÃO ##############
#######################################
def init(a,b):
    global data_db,items_db,data_db_cursor,items_db_cursor
    # connect to Database
    print('SQL: Connecting to SQL database: '+a)
    data_db=sqlite3.connect(a)
    data_db_cursor=data_db.cursor()
    print('SQL: Connecting to SQL database: '+b)
    items_db=sqlite3.connect(b)
    items_db_cursor=items_db.cursor()
    start_sprite_dict()
    start_audio_dict()
    start_enemy_dict()
    start_items_dict()
    start_shop_magazine()
    start_big_boom_list()



class sprite_data:
    def __init__(self,anim,w,h):
        self.Animation=anim
        self.h=h
        self.w=w


def start_sprite_dict():
    global sprites_dict
    # inicia um dicionario global de sprites - leva um tempora carregar
    print('Initializing sprites dictionary -  may take some time!')

    ''' ---TEMPLATE---
    #hit do tiro de laser
    if 1:
        name='laser_turret_hit'<- nome da pasta
        w=80 <-largura
        h=80<- alktura
        t=50<- tempo de cada frame na tela
        n=4<- numero de frames
        spritelist=[]
        for i in range(n):
            aux='sprites/'+name+'/'+str(i)+'.png'
            spritelist.append((aux,t))
            aux=pyganim.PygAnimation(spritelist)
            sprites_dict[name]=sprite_data(aux,w,h)
    '''

    # 'small_explosion'
    if 1:
        spritelist=[]
        for i in range(14):
            aux='sprites/small_explosion/'+str(i)+'.png'
            spritelist.append((aux,50))
            aux=pyganim.PygAnimation(spritelist)
            sprites_dict['small_explosion']=sprite_data(aux,64,64)

    # 'medium_explosion'
    if 1:
        spritelist=[]
        for i in range(14):
            aux='sprites/medium_explosion/'+str(i)+'.png'
            spritelist.append((aux,60))
            aux=pyganim.PygAnimation(spritelist)
            sprites_dict['medium_explosion']=sprite_data(aux,160,160)

    # 'blue spark'
    if 1:
        name='blue_spark'
        spritelist=[]
        for i in range(6):
            aux='sprites/'+name+'/'+str(i)+'.png'
            spritelist.append((aux,20))
            aux=pyganim.PygAnimation(spritelist)
            sprites_dict[name]=sprite_data(aux,60,60)

    # 'red_spark'
    if 1:
        name='red_spark'
        spritelist=[]
        for i in range(6):
            aux='sprites/'+name+'/'+str(i)+'.png'
            spritelist.append((aux,20))
            aux=pyganim.PygAnimation(spritelist)
            sprites_dict[name]=sprite_data(aux,60,60)

            # 'yellow_spark'
            name='yellow_spark'
            spritelist=[]
            for i in range(6):
                aux='sprites/'+name+'/'+str(i)+'.png'
                spritelist.append((aux,20))
                aux=pyganim.PygAnimation(spritelist)
                sprites_dict[name]=sprite_data(aux,60,60)

    # shield da nave
    if 1:
        spritelist=[]
        for i in range(7):
            aux='images/ship/shield/'+str(i)+'.png'
            spritelist.append((aux,50))
            sprites_dict['ship_shield']=pyganim.PygAnimation(spritelist)

    # hit do tiro de laser turret
    if 1:
        name='laser_turret_hit'
        w=80
        h=80
        t=50
        n=4
        spritelist=[]
        for i in range(n):
            aux='sprites/'+name+'/'+str(i)+'.png'
            spritelist.append((aux,t))
            aux=pyganim.PygAnimation(spritelist)
            sprites_dict[name]=sprite_data(aux,w,h)

    # hit do twin laser
    if 1:
        name='twin_laser_hitmark'
        w=60
        h=60
        t=60
        n=1
        spritelist=[]
        for i in range(n):
            aux='sprites/'+name+'/'+str(i)+'.png'
            spritelist.append((aux,t))
            aux=pyganim.PygAnimation(spritelist)
            sprites_dict[name]=sprite_data(aux,w,h)


def start_audio_dict():
    global audio_dict,SFXVOL,BGMVOL
    # inicia um dicionario global de soms
    print('Initializing audio dictionary (SFX:'+str(SFXVOL)+' BGM:'+str(BGMVOL)+')')

    ''' ---TEMPLATE---
    #barulho do prefire laser turret
    if 1:
        name='laser_turret_prefire'<- nome do arquivo
        vol=0.6<- volume de compensação
        aux='sounds/weapons/'+name+'.ogg'
        aux=pygame.mixer.Sound(aux)
        aux.set_volume(SFXVOL*vol)
        audio_dict[name]=aux'''

    # transição de menu
    if 1:
        name='menu_swap'
        aux='sounds/menu/transition.ogg'
        aux=pygame.mixer.Sound(aux)
        aux.set_volume(SFXVOL*0.8)
        audio_dict[name]=aux

    # erro menu
    if 1:
        name='menu_error'
        aux='sounds/menu/error.ogg'
        aux=pygame.mixer.Sound(aux)
        aux.set_volume(SFXVOL*0.8)
        audio_dict[name]=aux

    # barulho da arma flak - 'flak'
    if 1:
        name='flak'
        aux='sounds/weapons/flak.ogg'
        aux=pygame.mixer.Sound(aux)
        aux.set_volume(SFXVOL*0.5)
        audio_dict[name]=aux

    # barulho da explosao media - 'medium_explosion'
    if 1:
        name='medium_explosion'
        aux='sounds/medium_explosion.ogg'
        aux=pygame.mixer.Sound(aux)
        aux.set_volume(SFXVOL)
        audio_dict[name]=aux

    # barulho do casco da nave
    if 1:
        name='ship_hull'
        aux='sounds/ship/hull.ogg'
        aux=pygame.mixer.Sound(aux)
        aux.set_volume(SFXVOL)
        audio_dict[name]=aux

    # barulho do prefire laser turret
    if 1:
        name='laser_turret_prefire'
        vol=0.5
        aux='sounds/weapons/'+name+'.ogg'
        aux=pygame.mixer.Sound(aux)
        aux.set_volume(SFXVOL*vol)
        audio_dict[name]=aux

    # barulho da laser turret
    if 1:
        name='laser_turret_fire'
        vol=1
        aux='sounds/weapons/'+name+'.ogg'
        aux=pygame.mixer.Sound(aux)
        aux.set_volume(SFXVOL*vol)
        audio_dict[name]=aux

    # barulho do big boom
    if 1:
        name='death_boom'
        vol=1
        aux='sounds/ship/'+name+'.ogg'
        aux=pygame.mixer.Sound(aux)
        aux.set_volume(SFXVOL*vol)
        audio_dict[name]=aux

    #twin laser
    if 1:
        name='twin_laser_fire'
        vol=0.8
        aux='sounds/weapons/'+name+'.ogg'
        aux=pygame.mixer.Sound(aux)
        aux.set_volume(SFXVOL*vol)
        audio_dict[name]=aux

    # leave_wave
    if 1:
        name='leave_wave'
        vol=0.8
        aux='sounds/ship/'+name+'.ogg'
        aux=pygame.mixer.Sound(aux)
        aux.set_volume(SFXVOL*vol)
        audio_dict[name]=aux

def start_enemy_dict():
    print('Initializing enemies dictionary')

    # enemy #0
    # aux=enemy_ship_0()
    # enemy_dict['0']=enemy_ship_0()


def start_items_dict():
    print('Initializing items dictionary')

    # ENERGY MODULE
    name='Energy Module'
    aux=Energy_module(name,1)
    items_dict[name]=aux

    # Phase Shield
    name='Phase Shield'
    aux=Shield(name,1)
    items_dict[name]=aux


    #os items do player temn qte rumn index melhorzin, pro magazine de arma funcionar das ships
    # Machine gun
    name='a'
    real_name='Machine Gun'
    aux=Machine_gun(real_name)
    items_dict[name]=aux

    # AA Missle
    name='0'
    real_name='Air/Air Missle'
    aux=AA_missle(real_name)
    items_dict[name]=aux

    # Laser Turret
    name='4'
    real_name='Laser Turret'
    aux=Laser_turret(real_name)
    items_dict[name]=aux

    # Twin Laser
    name='9'
    real_name='Twin Laser'
    aux=Twin_Laser(real_name)
    items_dict[name]=aux


def start_shop_magazine():
    print('Starting shop magazine...')


    #0
    shop_magazine.append(Energy_module('Energy Module',100))
    if 1:
        aux=[]
        aux.append('REPLENISHES NORMAL SHIELDS. THE')
        aux.append('LIFEBLOOD OF ALL PILOTS, THIS')
        aux.append('LITTLE PACKAGE IS USUALLY THE')
        aux.append('FRIST THING ON ALL PILOTS WISH')
        aux.append('LISTS')
        aux.append('SOLD IN 25 UNIT INCREMENTS ONLY!')
        shop_description_lines.append(aux)

    #1
    shop_magazine.append(Shield('Phase Shield',100))
    if 1:
        aux=[]
        aux.append('THE SA17 ARES IS AN ENHANCEMENT')
        aux.append('FOR NORMAL SHIELDS. THE ARES')
        aux.append('RAISES A ENERGY FIELD AROUND THE')
        aux.append('FIGHTER, WHICH WILL ABSORB ENEMY')
        aux.append('FIRE UNTIL ITS POWER SUPPLY ')
        aux.append('IS DEPLETED')
        shop_description_lines.append(aux)

    #2
    shop_magazine.append(Mega_Bomb('Mega Bomb'))
    if 1:
        aux=[]
        aux.append('NOT IMPLEMENTED YET')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        shop_description_lines.append(aux)

    #3
    shop_magazine.append(Machine_gun('Machine Gun'))
    if 1:
        aux=[]
        aux.append('FIRING 21MM ROUNDS AT 7500')
        aux.append('ROUNDS/MIN MAKES THE REAVER')
        aux.append('THE BASIC WEAPON OF CHOICE')
        aux.append('FOR MOST PILOTS')
        aux.append('')
        aux.append('CANT BE SOLD - JUST FOR SHOW!')
        shop_description_lines.append(aux)

    #4
    shop_magazine.append(Plasma_Cannon('Plasma Cannon'))
    if 1:
        aux=[]
        aux.append('NOT IMPLEMENTED YET')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        shop_description_lines.append(aux)

    #5
    shop_magazine.append(Micro_Missle('Micro Missle'))
    if 1:
        aux=[]
        aux.append('NOT IMPLEMENTED YET')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        shop_description_lines.append(aux)

    #6
    shop_magazine.append(AA_missle('Air/Air Missle'))
    if 1:
        aux=[]
        aux.append('THE AIM-31 MAULER HAS BEEN THE')
        aux.append('MAINSTAY OF MOST MILITARY FORCES')
        aux.append('SINCE ITS INTRODUCTION IN 1997.')
        aux.append('THE UNRIVALED RELIABILITY OF THE')
        aux.append('MAULER MAKES IT A NECESSITY IN')
        aux.append('ANY DOGFIGHT')
        shop_description_lines.append(aux)

    #7
    shop_magazine.append(AG_missle('Air/Ground Missle'))
    if 1:
        aux=[]
        aux.append('NOT IMPLEMENTED YET')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        shop_description_lines.append(aux)

    #8
    shop_magazine.append(Dumbfire_missle('Dumbfire Missle'))
    if 1:
        aux=[]
        aux.append('NOT IMPLEMENTED YET')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        shop_description_lines.append(aux)

    #9
    shop_magazine.append(Missle_Pod('Misslepod'))
    if 1:
        aux=[]
        aux.append('NOT IMPLEMENTED YET')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        shop_description_lines.append(aux)

    #10
    shop_magazine.append(Auto_Machine_Gun('Auto Machine Gun'))
    if 1:
        aux=[]
        aux.append('NOT IMPLEMENTED YET')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        shop_description_lines.append(aux)

    #11
    shop_magazine.append(Power_disruptor('Power Disruptor'))
    if 1:
        aux=[]
        aux.append('NOT IMPLEMENTED YET')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        shop_description_lines.append(aux)

    #12
    shop_magazine.append(Laser_turret('Laser Turret'))
    if 1:
        aux=[]
        aux.append("THE OD55 'ODIN' LASER TURRET IS")
        aux.append('A PILOTS BEST CHOICE OFR AIR ')
        aux.append('COMBAT. SIMILAR TO THE TH19')
        aux.append('THOR, THE ODIN HAS A FASTER')
        aux.append("RESPONSE TIME WITH THE LASER'S")
        aux.append('INCREASED FIREPOWER.')
        shop_description_lines.append(aux)

    #13
    shop_magazine.append(Pulse_Cannon('Pulse Cannon'))
    if 1:
        aux=[]
        aux.append('NOT IMPLEMENTED YET')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        shop_description_lines.append(aux)

    #14
    shop_magazine.append(Deathray('Plasma Ray'))
    if 1:
        aux=[]
        aux.append('NOT IMPLEMENTED YET')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        aux.append('')
        shop_description_lines.append(aux)

    #15
    shop_magazine.append(Twin_Laser('Twin Laser'))
    if 1:
        aux=[]
        aux.append('THE CAL-10 ECLIPSE IS THE MOST')
        aux.append('POWERFUL WEAPON AVAILABLE')
        aux.append('TWIN BEAMS OF AZURE FIRE')
        aux.append('WILL INCINERATE ANYTHING IN')
        aux.append('THEIR PATH.')
        aux.append('ps: use headfones!')
        shop_description_lines.append(aux)

    #16 intro
    if 1:
        aux=[]
        aux.append('WELCOME TO THE ONE')
        aux.append('AND ONLY AUTOMATED')
        aux.append('ONE STOP SHOP. ALL')
        aux.append('PURCHASES WILL BE LOADED')
        aux.append('AND INSTALLED FREE OF CHARGE.')
        aux.append('CHECK OUT THE BARGAINS TODAY!')
        shop_description_lines.append(aux)

    # 17 erro -1 falta de dinheiro
    if 1:
        aux=[]
        aux.append('YOU SEEM TO HAVE COME TO THE')
        aux.append('LIMIT OF YOUR FINANCES. CASH')
        aux.append('AND CARRY ONLY. THANK YOU')
        aux.append("FOR CHOOSING AUDREY'S WEAPONS")
        aux.append('EMPORIUM, THE ONLY SHOP FOR')
        aux.append('THE DISCERNING MERCENARY')
        shop_description_lines.append(aux)

    # 18 erro -2 nave lotada
    if 1:
        aux=[]
        aux.append('YOU HAVEREACHED THE MAXIMUM')
        aux.append('PAYLOAD CAPACITY FOR YOUR')
        aux.append('FIGHTER. WE CANNOT ADD ANOTHER')
        aux.append('ITEM WITHOUT EXCEEDING THE')
        aux.append('MANUFATURERS STRUCTURAL')
        aux.append('INTEGRITY SPECIFICATIONS.')
        shop_description_lines.append(aux)


def start_big_boom_list():
    big_boom_list.append((-40,-40))
    big_boom_list.append((0,-40))
    big_boom_list.append((+40,-40))
    big_boom_list.append((-40,0))
    big_boom_list.append((0,0))
    big_boom_list.append((+40,0))
    big_boom_list.append((-40,+40))
    big_boom_list.append((0,+40))
    big_boom_list.append((+40,+40))

    big_boom_list.append((-60,-60))
    big_boom_list.append((0,-60))
    big_boom_list.append((+60,-60))
    big_boom_list.append((-60,0))
    big_boom_list.append((0,0))
    big_boom_list.append((+60,0))
    big_boom_list.append((-60,+60))
    big_boom_list.append((0,+60))
    big_boom_list.append((+60,+60))

    big_boom_list.append((-80,-80))
    big_boom_list.append((0,-80))
    big_boom_list.append((+80,-80))
    big_boom_list.append((-80,0))
    big_boom_list.append((0,0))
    big_boom_list.append((+80,0))
    big_boom_list.append((-80,+80))
    big_boom_list.append((0,+80))
    big_boom_list.append((+80,+80))

# chamadas DE SPAWN - x,y é o centro da animação!!!
def spawn_sprite(x,y,key,dx=0,dy=0,loop=False):
    global sprites_dict
    if key in sprites_dict:
        n=len(render.sprites)
        aux=sprites_dict.get(key)
        render.sprites.append(Animation(aux.Animation,anim_rect(x,y,dx,dy,aux.w,aux.h)))
        if loop:
            render.sprites[n].animation._loop=True
        render.sprites[n].animation.play()
    else:
        if key=='null':
            a=1
        elif key==None:
            print('No key was provided')
        else:
            print(key+' was not found on the sprites dictionary!')


def play_sound(key):
    global audio_dict
    if key in audio_dict:
        n=sound_engine.mixer.find_channel()
        if n!=None:
            sound_engine.mixer.channel[n].play(audio_dict.get(key))
    else:
        print('There is no audio: '+key)


def spawn(ID,spawn_distance,pos_list):
    if ID==0:
        return enemy_ship_0(pos_list=pos_list,spawn_dist=spawn_distance)
    elif ID==1:
        return enemy_ship_1(pos_list=pos_list,spawn_dist=spawn_distance)


# leitura do arquivo csv, tipo pode melhorar bastante ainda!
def load_wave_list(id,list,loading_line=None):
    aux='waves/'+id+'.csv'
    file=open(aux,'+r')
    data=csv.reader(file,delimiter=',')
    ni=0  # numero da linha

    for i in data:
        if ni<2:
            if ni==1:
                b=int(i[0])  # numero de naves
                c=int(i[1])
            ni+=1
        else:
            ni+=1
            a=i
            distance=int(a[0])
            id=int(a[1])
            n=int(a[2])
            points=[]
            for j in range(1,n+1):
                if j<n:
                    k=j*3
                    aux=a[k]
                    if aux=='r':
                        aux=random.randrange(50,sresH-50)
                    else:
                        aux=int(aux)
                    p=(aux,int(a[k+1]),int(a[k+2]))
                    points.append(p)
                else:
                    k=j*3
                    aux=a[k]
                    if aux=='r':
                        aux=random.randrange(50,sresH-50)
                    else:
                        aux=int(aux)
                    p=(aux,int(a[k+1]))
                    points.append(p)

            if loading_line!=None:
                loading_line.update(ni/(b+2))
                # print(ni/(b+2))

            '''print('\n')
            print('ni'+str(ni)+' pts,id,dist')
            print(points)
            print(id)
            print(distance)'''

            list.append(spawn(id,distance,points))
    file.close()
    return b,c


#######################################
########## CLASSES GERAIS #############
#######################################
class text:  # (str,ttf_file,size,color,cx,cy,abs?) none=center / 1=topleft / 2=topright
    def __init__(self,str,ttf_file,size,color,cx,cy,abs=None):
        # local defs
        self.abs=abs
        self.cx=cx
        self.cy=cy
        self.color=color
        self.str=str
        self.defcolor=color
        self.defstr=str

        self.font=pygame.font.Font(ttf_file,size)
        self.text=self.font.render(self.str,1,self.color)
        if self.abs==1:
            self.rect=self.text.get_rect(left=self.cx,top=self.cy)
        elif self.abs==2:
            self.rect=self.text.get_rect(right=self.cx,top=self.cy)
        else:
            self.rect=self.text.get_rect(centerx=self.cx,centery=self.cy)

    def update_text(self,str=None,color=None):
        if color!=None:
            self.color=color
        if str!=None:
            self.str=str
        self.text=self.font.render(self.str,1,self.color)
        if self.abs==1:
            self.rect=self.text.get_rect(left=self.cx,top=self.cy)
        elif self.abs==2:
            self.rect=self.text.get_rect(right=self.cx,top=self.cy)
        else:
            self.rect=self.text.get_rect(centerx=self.cx,centery=self.cy)

    def add_text(self,str):
        self.str+=str
        self.text=self.font.render(self.str,1,self.color)


class line:  # (start,end,color,width)
    def __init__(self,start,end,color,width):
        self.start=start
        self.end=end
        self.color=color
        self.width=width

    def movex(self,a,abs=None):
        if abs:
            self.start=(a,self.start[1])
            self.end=(a,self.end[1])
        else:
            self.start=(self.start[0]+a,self.start[1])
            self.end=(self.end[0]+a,self.end[1])


class loading_line(line):
    def __init__(self,start,end,color,width,current=0):
        line.__init__(self,start,end,color,width)
        self.max=max
        self.current=current
        self.max_size=self.end[0]-self.start[0]
        self.start_point=self.start[0]
        self.update(self.current)

    def update(self,current):
        self.current=current
        a=self.max_size*self.current
        self.end=(self.start_point+a+10,self.end[1])


class Player:
    def __init__(self,aux):
        self.name=aux[1]
        self.callsign=aux[2]
        self.shipname=aux[3]
        self.imageindex=aux[4]
        self.shipindex=aux[5]

        self.ship=Ship(self.shipindex)

        # internal
        self.money=aux[6]

        # pygame stuff
        picture_file_path='images/profiles/'+str(self.imageindex)+'.jpg'
        print('loading file: '+picture_file_path)
        self.image=pygame.image.load(picture_file_path)
        self.rect=self.image.get_rect()

    def save(self,cursor):
        a='UPDATE profiles SET '
        a+='money='+str(self.money)
        a+=" WHERE name='"+self.name+"'"
        #print(a)
        cursor.execute(a)

        self.ship.save(cursor)

class Cursor:
    def __init__(self,image):
        self.image=image
        # self.rect=image.get_rect()
        self.buttons=(0,0,0)
        self.button_held=False
        self.posdX=0
        self.posdY=0
        self.posX,self.posY=pygame.mouse.get_pos()
        self.differential_mode=False
        render.cursors.append(Object(image,100,100,0,0))

    def update(self,renderer):
        if self.differential_mode:
            tempx,tempy=pygame.mouse.get_pos()
            self.posdX=tempx-(sresH/2)
            self.posdY=tempy-(sresV/2)
            self.posX+=self.posdX
            self.posY+=self.posdY
            pygame.mouse.set_pos((sresH/2,sresV/2))

            # atualiza os graficos do render
            renderer.cursorObj.moveabs(self.posX-20,self.posY-20)
        else:
            self.posX,self.posY=pygame.mouse.get_pos()
            renderer.cursorObj.moveabs(self.posX-20,self.posY-20)
        self.buttons=pygame.mouse.get_pressed()
        if not (self.buttons)[0]:
            self.button_held=False

    def diff_mode(self,bool=None):
        if bool==None:
            self.differential_mode=not self.differential_mode
        else:
            self.differential_mode=bool

        if self.differential_mode:
            self.posX=sresH/2
            self.posY=sresV/2
        else:
            self.posX=sresH/2
            self.posY=sresV/2
            self.posdX=0
            self.posdY=0

#menu -> VIC - Very Important Class
class menu:  # (settings_file,profiles_file,crosshair_file,bgm_file):
    def __init__(self,crosshair_file,bgm_file,bgm_file2,button_sound_file,button_select_file):
        print('\t')
        self.print('Initializing menu...')

        # control variables
        self.status='loading'
        self.next_status=''
        self.in_menu=True
        self.ops=[]
        self.player_list=[]
        self.lastop=None
        self.op=None
        self.player_text_index=None
        self.button_sound_held=False
        self.selected=False



        # read saved data
        self.read_user_settings()
        self.read_player_profiles()

        self.print('Active player: '+str(self.active_player))
        self.player=self.player_list[self.active_player-1]
        self.selected_player=self.active_player

        # start subsystems
        self.print('Initalizing audio')
        self.button_sound=None
        self.select_sound=None
        self.start_sounds(button_sound_file,button_select_file)
        self.cursor=None
        self.start_cursor(crosshair_file)

        # music
        self.bgm=pygame.mixer.Sound(bgm_file)
        self.bgm2=pygame.mixer.Sound(bgm_file2)
        self.bgm.set_volume(BGMVOL)
        self.bgm2.set_volume(BGMVOL)
        sound_engine.mixer.channel[0].play(self.bgm,fade_ms=500)

        self.print('Successfuly loaded!')

    def swap(self,menus):
        self.next_status=menus
        self.last_status=self.status
        self.lastop=None
        self.status='changing'
        self.changed=True
        self.ops=[]
        print('\nChanging menu to: '+menus)

    def done_loading(self):
        self.changed=False
        self.status=self.next_status
        print('Done!')

    def read_user_settings(self):
        global data_db_cursor
        self.print('Reading user settings')
        data_db_cursor.execute('SELECT * FROM settings')
        self.settings=data_db_cursor.fetchall()[0]

        self.bgm_volume=self.settings[0]
        self.bgm_status=self.settings[1]
        self.active_player=self.settings[2]

    def read_player_profiles(self):
        global data_db_cursor
        self.print('Reading profiles...')
        data_db_cursor.execute('SELECT * FROM profiles')
        self.profile_list=data_db_cursor.fetchall()
        n=len(self.profile_list)

        self.print(str(n)+' Profiles detected')
        for i in self.profile_list:
            self.print('\tProfile line: '+str(i))
            self.print('\tSetting player: #'+str(i[0]-1))
            self.player_list.append(Player(i))
        print('\t')

    def save_data(self):
        self.print('Saving data')
        self.print('\t Global settings..')
        global data_db_cursor,data_db

        aux='UPDATE settings SET'+' bgm_volume='+str(self.bgm_volume)+','+'last_player='+str(self.active_player)
        data_db_cursor.execute(aux)

        for i in self.player_list:
            i.save(data_db_cursor)
        self.print('\tCommiting database')
        data_db.commit()

    def start_cursor(self,file):
        self.cursor=Cursor(pygame.image.load(file).convert_alpha())
        self.print('Cursor management started')

    def start_sounds(self,bsound,selsound):
        self.button_sound=pygame.mixer.Sound(bsound)
        self.select_sound=pygame.mixer.Sound(selsound)
        self.button_sound.set_volume(SFXVOL)
        self.select_sound.set_volume(SFXVOL)

    def bgm_toogle(self,bool=None):
        if bool==None:
            self.bgm=not self.bgm
        else:
            self.bgm=bool

    def sel_update(self):

        # verifica onde o mouse ta
        op=mouse_spots.check_selection(self.status,self.cursor.posX,self.cursor.posY)
        self.op=op
        # se estuver em cmia de um botao, fala pra ele ficar selecionado
        # se nao nao
        if op!=None:
            for i in range(len(render.buttons)):
                if i!=op:
                    render.buttons[i].swap_image(False)
                else:
                    render.buttons[i].swap_image(True)
        # se td estiver descelecionado eh td descelecionado
        else:
            for i in render.buttons:
                i.swap_image(False)
        # se tiver uma op diferente toca sonzinho
        if op!=self.lastop and op!=None:
            self.button_sound.play()
        # segura a ultimia op pro p~óx ciclo
        self.lastop=op

        if (self.cursor.buttons)[0]==0:
            self.button_held=False

        if (self.cursor.buttons)[0]==1 and not self.button_held and op!=None:
            self.button_held=True
            action=mouse_spots.check_choice(self.status,op)
            # print(action)
            # para a??o interna:
            if action[0]=='$':
                # $-> troca de menu, ja se atualiza!
                if action[1]=='$':
                    self.swap(action[2:])
                    return action
                # %-> troca player selecionado
                elif action[1]=='%':
                    # print(action[2:])
                    self.swap_player(action[2:])
                # &-> salva os dados
                elif action[1]=='&':
                    self.save_user_profiles()
                    self.print('User data saved')
            else:

                return action

    def update(self,renderer):
        self.cursor.update(renderer)
        return self.sel_update()

    def swap_player(self,direction):
        if direction=='+' and (self.selected_player+1)<=(len(self.player_list)):
            self.selected_player+=1
            self.update_menu_profile_data()
            if self.selected:
                render.texts.pop()

        elif direction=='-' and (self.selected_player-1)>=0:
            self.selected_player-=1
            self.update_menu_profile_data()
            if self.selected:
                render.texts.pop()

        elif direction=='*':
            filepath='fonts/major_shift.ttf'
            self.print('loading file: '+filepath)
            render.texts.append(text('player selected',filepath,24,colors.RED,970,700,1))

            self.active_player=self.selected_player
            self.player=self.player_list[self.active_player-1]
            pygame.time.delay(400)
            self.swap('main')


        elif direction=='**':
            self.selected_player=self.active_player
            self.update_menu_profile_data()
            self.swap('main')

    def update_menu_profile_data(self):
        render.objects[len(render.objects)-1].change_image(self.player_list[self.selected_player-1].image)
        render.texts[self.player_text_index].update_text(self.player_list[self.selected_player-1].name)
        render.texts[self.player_text_index+1].update_text(self.player_list[self.selected_player-1].callsign)
        render.texts[self.player_text_index+2].update_text(self.player_list[self.selected_player-1].shipname)

    def print(self,str):
        print(Fore.BLUE+'[MENU] '+Fore.RESET+str)


class Object:  # (image,PosH,PosV,speedH,speedV):
    def __init__(self,image,PosH,PosV,speedH,speedV,mode=None):
        self.speedV=speedV
        self.speedH=speedH
        self.image=image
        self.rect=image.get_rect().move(PosH,PosV)
        if mode=='centered':
            self.rect.center=(PosH,PosV)

    def update_rect(self):
        self.rect=self.rect.move(self.speedH,self.speedV)
        return self.check_out()

    def check_out(self):
        if self.rect.bottom<=-100 or self.rect.top>=900:
            return True

    def moveabs(self,x,y):
        self.rect=self.image.get_rect().move(x,y)

    def moverel(self,x,y):
        self.rect=self.rect.move(x,y)

    def change_image(self,image):
        self.image=image

    def change_alpha(self,alpha):
        self.image.set_alpha(alpha)


class Projectile(Object):
    def __init__(self,image,PosH,PosV,speedH,speedV,mode=None,*kpos,**kwargs):
        Object.__init__(self,image,PosH,PosV,speedH,speedV,mode)

        if 'damage' in kwargs:
            self.damage=kwargs.get('damage')

        if 'origin' in kwargs:
            self.origin=kwargs.get('origin')
        else:
            self.origin=None

        if 'friendly' in kwargs:
            self.friendly=kwargs.get('friendly')
        else:
            self.friendly=False

        self.valid=True
        self.pseudo=False
        self.has_anim=False
        if 'anim' in kwargs:
            self.Animation=kwargs.get('anim')
            self.has_anim=True

    def check_out(self):
        if self.rect.bottom<=-100 or self.rect.top>=900 or self.valid==False:
            return True

    def blit(self,screen):
        screen.blit(self.image,self.rect)

        if self.has_anim:
            self.Animation.blit(screen)

    def update_rect(self):
        self.rect=self.rect.move(self.speedH,self.speedV)
        if self.has_anim:
            self.Animation.rect.update_rect()
        return self.check_out()


class pseudo_Projectile:
    def __init__(self,dmg,origin):
        self.damage=dmg
        self.origin=origin
        self.pseudo=True


class MenuButton(Object):  # (imagefileA,imagefileB,PosH,PosV,mode=None):
    def __init__(self,imagefileA,imagefileB,PosH,PosV,mode=None):
        self.imageB=pygame.image.load(imagefileB).convert_alpha()
        self.imageA=pygame.image.load(imagefileA).convert_alpha()
        Object.__init__(self,self.imageA,PosH,PosV,0,0)
        self.bool=True

        if mode==None:
            self.rect.right=580
        elif mode=='centered':
            self.rect.center=(PosH,PosV)
        elif mode=='abs':
            self.rect.top=PosV
            self.rect.left=PosH

    def swap_image(self,bool=None):
        if bool==None:
            self.bool=not self.bool
        else:
            self.bool=bool

        if self.bool:
            self.image=self.imageA
        else:
            self.image=self.imageB

    def update_image(self,a,b=None):
        if b==None:
            b=a
        self.imageB=pygame.image.load(a).convert_alpha()
        self.imageA=pygame.image.load(b).convert_alpha()


class Display:
    def __init__(self,money_id,picture_id,name_id,function_id,desc_texts,\
                 have_id,cost_id,value_id,button_id,have_str_id):
        self.money_id=money_id
        self.picture_id=picture_id
        self.name_id=name_id
        self.function_id=function_id
        self.desc_texts=desc_texts
        self.have_id=have_id
        self.cost_id=cost_id
        self.value_id=value_id
        self.button_id=button_id
        self.have_str_id=have_str_id
        #controle
        self.status='intro'
        self.shop_sell_magazine=[]

    def recover_from_error(self):
        render.objects[self.picture_id].rect.left=930
        render.objects[self.picture_id].rect.top=168
        render.texts[self.have_str_id].update_text('YOU HAVE')
        if self.lastmode=='selling':
            render.texts[self.cost_id].update_text('RESALE')
        else:
            render.texts[self.cost_id].update_text('COST')

    def swap(self,op,error_number=None):
        self.lastmode=self.status
        self.status=op
        if op=='error':
            play_sound('menu_error')
            render.objects[self.picture_id].rect.center=(-100,-100)
            render.texts[self.name_id].update_text('SORRY..')
            render.texts[self.function_id].update_text('')
            render.texts[self.cost_id].update_text('')
            render.texts[self.button_id].update_text('OK')
            render.texts[self.value_id].update_text('')
            render.texts[self.have_id].update_text('')
            render.texts[self.have_str_id].update_text('')

            if error_number==-1:
                k=0
                for i in self.desc_texts:
                    render.texts[i].update_text(shop_description_lines[17][k])
                    k+=1
            if error_number==-2:
                k=0
                for i in self.desc_texts:
                    render.texts[i].update_text(shop_description_lines[18][k])
                    k+=1

    def update(self,money,cursor,have,selling=False):
        if selling:
            render.texts[self.money_id].update_text('$'+str(money))
            render.objects[self.picture_id].image=self.shop_sell_magazine[cursor].image_2x
            render.texts[self.name_id].update_text(self.shop_sell_magazine[cursor].name)
            render.texts[self.function_id].update_text(self.shop_sell_magazine[cursor].function)
            render.texts[self.value_id].update_text(str(int(self.shop_sell_magazine[cursor].cost/2)))
            render.texts[self.have_id].update_text(str(int(have)))
            render.texts[self.button_id].update_text('SELL')
            k=0
            for i in self.desc_texts:
                render.texts[i].update_text(shop_description_lines[cursor][k])
                k+=1
        else:
            render.texts[self.money_id].update_text('$'+str(money))
            render.objects[self.picture_id].image=shop_magazine[cursor].image_2x
            render.texts[self.name_id].update_text(shop_magazine[cursor].name)
            render.texts[self.function_id].update_text(shop_magazine[cursor].function)
            render.texts[self.value_id].update_text(str(int(shop_magazine[cursor].cost)))
            render.texts[self.have_id].update_text(str(int(have)))
            render.texts[self.button_id].update_text('BUY')
            k=0
            for i in self.desc_texts:
                render.texts[i].update_text(shop_description_lines[cursor][k])
                k+=1

    def enter_sell_mode(self,player):
        self.status='sell'
        self.shop_sell_magazine=[]
        self.nones_items=[]
        self.shop_sell_magazine.append(player.ship.energy_module)
        self.shop_sell_magazine.append(player.ship.shield)
        if player.ship.bombs==0:
            self.shop_sell_magazine.append(None)
            self.nones_items.append(2)
        else:
            self.shop_sell_magazine.append(player.ship.megabomb_weapon)


        self.shop_sell_magazine.append(player.ship.weapon_magazine[10])
        self.shop_sell_magazine.append(player.ship.weapon_magazine[12])
        self.shop_sell_magazine.append(player.ship.weapon_magazine[11])
        self.shop_sell_magazine.append(player.ship.weapon_magazine[0])
        self.shop_sell_magazine.append(player.ship.weapon_magazine[1])
        self.shop_sell_magazine.append(player.ship.weapon_magazine[7])
        self.shop_sell_magazine.append(player.ship.weapon_magazine[2])
        self.shop_sell_magazine.append(player.ship.weapon_magazine[3])
        self.shop_sell_magazine.append(player.ship.weapon_magazine[5])
        self.shop_sell_magazine.append(player.ship.weapon_magazine[4])
        self.shop_sell_magazine.append(player.ship.weapon_magazine[6])
        self.shop_sell_magazine.append(player.ship.weapon_magazine[8])
        self.shop_sell_magazine.append(player.ship.weapon_magazine[9])


        for i in range(len(self.shop_sell_magazine)):
            if self.shop_sell_magazine[i]==None:
                self.nones_items.append(i)
        print(len(self.shop_sell_magazine))
        print(self.nones_items)

    def next(self,cursor):
        a=cursor+1
        if a==16:
            return 0
        elif a in self.nones_items:
            return self.next(a)
        return a

    def prev(self,cursor):
        a=cursor-1
        if a==-1:
            return self.prev(16)
        elif a==0:
            return a
        elif a in self.nones_items:
            return self.prev(a)

        return a


# BACKGROUND
class Background:
    def __init__(self,image,vy):
        print('Loading Background')
        self.objects=[]
        for i in range(3):
            self.objects.append(Object(image,0,0,0,0))
        self.vy=vy

        for i in self.objects:
            i.rect.centerx=(sresH/2)

        self.objects[0].rect.top=0
        self.objects[1].rect.top=-sresV
        self.objects[2].rect.top=-2*sresV

    def update_rect(self):
        for i in self.objects:
            i.rect.centery+=self.vy
            if i.rect.top>sresV:
                i.rect.bottom=(-(sresV/2))

    def blit(self,screen):
        for i in self.objects:
            screen.blit(i.image,i.rect)


# SPRITES
class anim_rect:
    def __init__(self,cx,cy,dx,dy,h,w):
        self.dx=dx
        self.dy=dy
        self.pos=[cx-(w/2),cy-(h/2)]
        self.h=h
        self.w=w

    def update_rect(self):
        self.pos[0]+=self.dx
        self.pos[1]+=self.dy
        if self.pos[0]>sresH+100 or self.pos[0]+self.w<-100 or self.pos[1]<-100 or self.pos[1]-self.h>sresV+100:
            return True


class Animation:
    def __init__(self,animation,rect,loop=False):
        self.animation=animation  # a do pyganim
        self.animation.play()
        self.rect=rect  # rect di aanim_rect
        self.loop=loop
        if loop==False:
            self.animation._loop=False

    def blit(self,screen):
        self.animation.blit(screen,(self.rect.pos[0],self.rect.pos[1]))

    def update_rect(self):
        if self.rect.update_rect():  # or (not self.loop and self.animation.state=='stopped'):
            return True
        elif self.loop==False:
            if self.animation.state=='stopped':
                return True


#######################################
############ WEAPONS ##################
#######################################
# CLASSE MÃE
class Weapon:
    def __init__(self,name):
        global items_db_cursor
        # read data

        items_db_cursor.execute('SELECT * FROM weapons WHERE name="'+name+'"')
        self.data=items_db_cursor.fetchall()[0]
        self.name=name
        self.damage=self.data[2]
        self.cost=self.data[4]

        # pygame stuff
        # image-self
        file='images/weapons/'+str(self.data[1])+'.png'
        self.image=pygame.image.load(file).convert_alpha()
        self.image_2x=self.image
        self.image=pygame.transform.scale(self.image,(50,50))


        self.rect=self.image.get_rect()
        self.rect.center=(sresH-60,28)
        # projectile
        self.projectile=None
        self.define_projectile()

        # clock
        self.clock=pygame.time.get_ticks()


# WEAPONS DO CLIENTE
class AA_missle(Weapon):
    def define_projectile(self):
        self.projectile_image=pygame.image.load('images/projectiles/aa_missle.png').convert_alpha()
        self.projectile_image=pygame.transform.scale(self.projectile_image,(8,20))
        self.projectile_speedV=-12
        self.cooldown=self.data[3]
        self.stringName='AIM-31 "Mauler" Air/Air Missile'
        self.movement_update=False

        self.function='Active'
        # audio
        aux='sounds/weapons/aa_missle.ogg'
        self.fire_sound=pygame.mixer.Sound(aux)
        self.fire_sound.set_volume(SFXVOL*0.5)

        self.missle_spritelist=[]
        for i in range(4):
            aux='sprites/missle_jet/'+str(i+1)+'.png'
            self.missle_spritelist.append((aux,25))
        self.anim=pyganim.PygAnimation(self.missle_spritelist)

    def fire(self,pos):
        # verifica se pode atirar
        if pygame.time.get_ticks()-self.clock>=self.cooldown:
            self.clock=pygame.time.get_ticks()
            # poe os 2 projeteis
            render.projectiles.append(Projectile(self.projectile_image,pos[0]+20,pos[1],0,self.projectile_speedV,
                                                 anim=Animation(self.anim,anim_rect(pos[0]+20+5,pos[1]+20,0,
                                                                                    self.projectile_speedV,8,20),True),
                                                 friendly=True,damage=self.damage,origin=self.name))
            render.projectiles.append(Projectile(self.projectile_image,pos[0]-27,pos[1],0,self.projectile_speedV,
                                                 anim=Animation(self.anim,
                                                                anim_rect(pos[0]-22,pos[1]+20,0,self.projectile_speedV,
                                                                          8,20),True),friendly=True,damage=self.damage,
                                                 origin=self.name))
            n=len(render.sprites)

            # toca barulinho
            sound_engine.mixer.channel[4].play(self.fire_sound)

        return None,None,self

    def unfire(self):
        pass

    def activate(self):
        pass


class AG_missle(Weapon):
    def define_projectile(self):
        self.not_implemented=True
        self.function='Active'


class Machine_gun(Weapon):
    def define_projectile(self):
        self.projectile_image=pygame.image.load('images/projectiles/mg.png').convert_alpha()
        self.projectile_image=pygame.transform.scale(self.projectile_image,(4,4))
        self.projectile_image_inv=pygame.transform.flip(self.projectile_image,True,False)
        self.projectile_speedV=-50
        self.proj_style_left=False
        self.proj_style_right=True
        self.cooldown=self.data[3]
        self.stringName='MG21C Twin Reaver Machine Guns'
        self.movement_update=False
        self.function='Passive - Always Equipped'

        # audio
        aux='sounds/weapons/mg.ogg'
        self.fire_sound=pygame.mixer.Sound(aux)
        self.fire_sound.set_volume(SFXVOL*0.4)

    def fire(self,pos):
        # verifica se pode atirar
        if pygame.time.get_ticks()-self.clock>=self.cooldown:
            self.clock=pygame.time.get_ticks()
            # poe os 2 projeteis
            a=random.randrange(11)
            b=random.randrange(11)
            if a>5:
                render.projectiles.append(
                    Projectile(self.projectile_image_inv,pos[0]+20,pos[1],0,self.projectile_speedV,damage=self.damage,
                               friendly=True,origin=self.name+'R'))
            else:
                render.projectiles.append(
                    Projectile(self.projectile_image,pos[0]+20,pos[1],0,self.projectile_speedV,damage=self.damage,
                               friendly=True,origin=self.name+'R'))
            if b>5:
                render.projectiles.append(
                    Projectile(self.projectile_image_inv,pos[0]-22,pos[1],0,self.projectile_speedV,damage=self.damage,
                               friendly=True,origin=self.name+'L'))
            else:
                render.projectiles.append(
                    Projectile(self.projectile_image,pos[0]-22,pos[1],0,self.projectile_speedV,damage=self.damage,
                               friendly=True,origin=self.name+'L'))

            # toca barulinho
            sound_engine.mixer.channel[5].play(self.fire_sound)

    def unfire(self):
        pass

    def activate(self):
        pass


class Laser_turret(Weapon):
    def define_projectile(self):
        self.cooldown=self.data[3]
        self.cooldown2=32
        self.target=None
        self.pseudo=True
        self.origin='Laser Turret'
        self.clock2=pygame.time.get_ticks()
        self.shot=False
        self.proj=pseudo_Projectile(self.data[2],'Laser Turret')
        self.movement_update=True
        self.stringName='OD55 "Odin" Laser Turret'
        self.function='Active'

    def enter_battle(self,n):
        self.line_n=n

    def activate(self):
        render.lines[self.line_n].color=colors.RED
        render.lines[self.line_n].width=4
        render.lines[self.line_n+1].color=colors.YELLOW
        render.lines[self.line_n+1].width=1

    def acquire_target(self,pos):
        if len(render.enemy_ships)>0:
            self.target=None
            k=0
            d=0
            for i in render.enemy_ships:
                dist=get_distance(i.rect.center,pos)
                if (dist<d or d==0):
                    if i.rect.centerx>0 and i.rect.top>0 and i.rect.centerx<sresH and i.rect.centery<sresV:
                        d=dist
                        self.target=k
                k+=1
        else:
            self.target=None

    def set_line(self,start,end):
        render.lines[self.line_n].start=start
        render.lines[self.line_n].end=end
        render.lines[self.line_n+1].start=start
        render.lines[self.line_n+1].end=end

    def update_line(self,pos):
        render.lines[self.line_n].start=pos
        render.lines[self.line_n+1].start=pos

    def reset_line(self):
        render.lines[self.line_n].start=(0,0)
        render.lines[self.line_n].end=(0,0)
        render.lines[self.line_n+1].start=(0,0)
        render.lines[self.line_n+1].end=(0,0)

    def fire(self,pos):
        if self.shot:
            if pygame.time.get_ticks()-self.clock2>=self.cooldown2:
                self.clock2=pygame.time.get_ticks()
                self.reset_line()
                self.shot=False

        if pygame.time.get_ticks()-self.clock>=self.cooldown:
            self.clock=pygame.time.get_ticks()
            self.acquire_target(pos)
            if self.target!=None:
                if check_if_on_screen(render.enemy_ships[self.target].rect):
                    play_sound('laser_turret_fire')
                    self.set_line(pos,render.enemy_ships[self.target].rect.center)
                    self.shot=True
                    self.clock2=pygame.time.get_ticks()
            else:
                play_sound('laser_turret_prefire')

            return self.target,None,self
        return None,None,self

    def unfire(self):
        self.reset_line()

    def update(self,pos):
        self.update_line(pos)


class Twin_Laser(Weapon):
    def define_projectile(self):
        self.cooldown=self.data[3]
        self.cooldown2=(self.cooldown/4)-2
        self.target=None
        self.clock2=pygame.time.get_ticks()
        self.origin='Twin Laser'
        self.shot=False
        self.offset=28
        self.list=[]
        self.tgt_list=[]
        self.current_frame=0
        self.proj=pseudo_Projectile(self.data[2],'Twin Laser')
        self.stringName='CAL-10 "Eclipse" Twin Lasers'
        self.function='Active'


        #carrega as bubbles dos tiros
        if 1:
            self.w=32
            self.h=36
            self.imagelist=[]
            n=4
            k=0
            for i in range(n):
                aux='sprites/twin_laser/'+str(i)+'.png'
                self.imagelist.append(pygame.image.load(aux))
                self.imagelist[k].convert_alpha()
                k+=1


        #bibliotecas de cores
        if 1:
            self.lineColor_OUTER=[]
            self.lineColor_OUTER.append((79,172,255))
            self.lineColor_OUTER.append((79,170,253))
            self.lineColor_OUTER.append((71,150,236))
            self.lineColor_OUTER.append((44,87,168))

            self.lineColor_INNER=[]
            self.lineColor_INNER.append((221,220,229))
            self.lineColor_INNER.append((221,233,244))
            self.lineColor_INNER.append((81,171,255))
            self.lineColor_INNER.append((56,111,192))

    def enter_battle(self,n,ship):
        #parametros a serem passados pela ship, asim que entrar na bvatalha
        self.origin='twin_laser'
        self.limitL=800
        self.limitR=800
        self.dr=-1
        self.dl=-1
        self.hitl=None
        self.hitr=None
        self.pseudo=True
        self.line_n=n
        self.my_ship=ship
        self.bubbles_n=len(render.static_objects)
        render.static_objects.append(Object(self.imagelist[self.current_frame],-50,-50,0,0))
        render.static_objects.append(Object(self.imagelist[self.current_frame],-50,-50,0,0))

    def set_bubbles(self,center,frame_number):
        a=abs(render.player.x)
        if a<5:
            self.offset=28
        elif a<12:
            self.offset=20
        else:
            self.offset=15
        render.static_objects[self.bubbles_n].rect.center=(center[0]-self.offset,center[1]+10)
        render.static_objects[self.bubbles_n].image=self.imagelist[frame_number]
        render.static_objects[self.bubbles_n+1].rect.center=(center[0]+self.offset,center[1]+10)
        render.static_objects[self.bubbles_n+1].image=self.imagelist[frame_number]

    def activate(self):
        # executa quando a arma é selecionada
        # fora-fora-dentro-dentro -> devido a ordem de plotagem
        render.lines[self.line_n].color=self.lineColor_OUTER[0]
        render.lines[self.line_n].width=16
        render.lines[self.line_n+1].color=self.lineColor_OUTER[0]
        render.lines[self.line_n+1].width=16

        render.lines[self.line_n+2].color=self.lineColor_INNER[0]
        render.lines[self.line_n+2].width=8
        render.lines[self.line_n+3].color=self.lineColor_INNER[0]
        render.lines[self.line_n+3].width=8

        self.current_frame=-1

    def deactivate(self):
        render.lines[self.line_n].start=(0,0)
        render.lines[self.line_n].end=(0,0)
        render.lines[self.line_n+1].start=(0,0)
        render.lines[self.line_n+1].end=(0,0)
        render.lines[self.line_n+2].start=(0,0)
        render.lines[self.line_n+2].end=(0,0)
        render.lines[self.line_n+3].start=(0,0)
        render.lines[self.line_n+3].end=(0,0)
        self.set_bubbles((-100,-100),0)
        self.set_line((-100,-100),0,0)

    def update_line_color(self):
        render.lines[self.line_n].color=self.lineColor_OUTER[self.current_frame]
        render.lines[self.line_n+1].color=self.lineColor_OUTER[self.current_frame]
        render.lines[self.line_n+2].color=self.lineColor_INNER[self.current_frame]
        render.lines[self.line_n+3].color=self.lineColor_INNER[self.current_frame]

    def set_line(self,pos,lenA,lenB):
        render.lines[self.line_n].start=(pos[0]-self.offset-1,pos[1]+10)
        render.lines[self.line_n].end=(pos[0]-self.offset-1,pos[1]-5-lenA)
        render.lines[self.line_n+2].start=(pos[0]-self.offset-1,pos[1]+10)
        render.lines[self.line_n+2].end=(pos[0]-self.offset-1,pos[1]-5-lenA)
        render.lines[self.line_n+1].start=(pos[0]+self.offset-1,pos[1]+10)
        render.lines[self.line_n+1].end=(pos[0]+self.offset-1,pos[1]-5-lenB)
        render.lines[self.line_n+3].start=(pos[0]+self.offset-1,pos[1]+10)
        render.lines[self.line_n+3].end=(pos[0]+self.offset-1,pos[1]-5-lenB)

    def move(self,force_deactivate=False):
        if self.current_frame>=0:
            self.set_bubbles(self.my_ship.rect.center,self.current_frame)
            #colocar aqui os limites e se estiver hitando alguem devolver a informação
            self.set_line(self.my_ship.rect.center,self.limitL,self.limitR)

        else:
            self.set_bubbles((-100,-100),0)
            self.set_line((-100,-100),0,0)

    def update_tgt_list(self,pos):
        oo=self.offset+8
        ool=pos[0]-oo
        ooli=ool-16
        oor=pos[0]+oo
        oori=oor-16
        flag=False


        for i in range(len(render.enemy_ships)):
            if render.enemy_ships[i].rect.left<oor and render.enemy_ships[i].rect.right>ool:
                self.list.append((i,render.enemy_ships[i].rect.bottom))
                flag=True
        if flag:
            tgt_L=-1
            tgt_R=-1
            chkd=[]
            while (tgt_L==-1) and (tgt_R==-1):
                d=0
                for i in self.list:
                    if (i[1]>d) and not(i[0] in chkd):
                        m=i[0]

                    if tgt_L==-1:
                        if render.enemy_ships[m].rect.right>ool and render.enemy_ships[m].rect.left<ooli:
                            tgt_L=m

                    if tgt_R==-1:
                        if render.enemy_ships[m].rect.right>oori and render.enemy_ships[m].rect.left<oor:
                            tgt_R=m

                    chkd.append(m)
                print(tgt_L,tgt_R)
            return tgt_L,tgt_R
        else:
            return None,None

    def fire(self,pos):
        self.move()
        self.hitl=None
        self.hitr=None
        if pygame.time.get_ticks()-self.clock2>=self.cooldown2:
            self.clock2=pygame.time.get_ticks()

            #verifica inimigos
            if self.current_frame!=-1:
                self.dl=-1
                self.dr=-1
                self.cr=None
                self.cl=None

                k=0
                for i in render.enemy_ships:
                    #se estiver dentro dos raio
                    if i.rect.left<self.my_ship.rect.right and i.rect.right>self.my_ship.rect.left:
                        #se tive na frente do raio esquerdo
                        if i.rect.right>self.my_ship.rect.left and i.rect.left<self.my_ship.rect.left+16:
                            if i.rect.bottom>self.dl:
                                self.dl=i.rect.bottom
                                self.cl=i.rect.centery
                                self.hitl=k
                        #se tiver na frente do raio direito
                        if i.rect.right>self.my_ship.rect.right-16 and i.rect.left<self.my_ship.rect.right:
                            if i.rect.bottom>self.dr:
                                self.dr=i.rect.bottom
                                self.cr=i.rect.centery
                                self.hitr=k
                k+=1
            if self.dl==-1:
                self.limitL=800
            else:
                self.limitL=self.my_ship.rect.centery-self.cl
                spawn_sprite(self.my_ship.rect.left,self.cl,'twin_laser_hitmark')

            if self.dr==-1:
                self.limitR=800
            else:
                self.limitR=self.my_ship.rect.centery-self.cr
                spawn_sprite(self.my_ship.rect.right,self.cr,'twin_laser_hitmark')

            if self.current_frame>=0:
                self.current_frame+=1

                if self.current_frame==4:
                    self.current_frame=-1
                else:
                    self.update_line_color()
            else:
                play_sound('twin_laser_fire')
                self.current_frame=0
                self.update_line_color()

        return self.hitl,self.hitr,self

    def unfire(self):
        self.move()
        if pygame.time.get_ticks()-self.clock2>=self.cooldown2:
            self.clock2=pygame.time.get_ticks()
            if self.current_frame>=0:
                self.current_frame+=1

                if self.current_frame==4:
                    self.current_frame=-1
                else:
                    self.update_line_color()


class Mega_Bomb(Weapon):
    def define_projectile(self):
        self.not_implemented=True

        self.function='Active'


class Plasma_Cannon(Weapon):
    def define_projectile(self):
        self.not_implemented=True
        self.function='Active'


class Micro_Missle(Weapon):
    def define_projectile(self):
        self.not_implemented=True
        self.function='Passive - Always Equipped'


class Dumbfire_missle(Weapon):
    def define_projectile(self):
        self.not_implemented=True
        self.function='Active'


class Missle_Pod(Weapon):
    def define_projectile(self):
        self.not_implemented=True
        self.function='Active'


class Auto_Machine_Gun(Weapon):
    def define_projectile(self):
        self.not_implemented=True

        self.function='Active'


class Power_disruptor(Weapon):
    def define_projectile(self):
        self.not_implemented=True
        self.function='Active'


class Pulse_Cannon(Weapon):
    def define_projectile(self):
        self.not_implemented=True
        self.function='Active'


class Deathray(Weapon):
    def define_projectile(self):
        self.not_implemented=True
        self.function='Active'


# WEAPONS INIMIGAS
class flak:
    def __init__(self,name):
        global items_db_cursor
        # read data
        items_db_cursor.execute('SELECT * FROM enemy_weapons WHERE name="'+name+'"')
        self.data=items_db_cursor.fetchall()[0]

        self.name=name
        self.damage=self.data[2]

        self.projectile=None
        self.define_projectile()

        # clock
        self.clock=pygame.time.get_ticks()

    def define_projectile(self):
        aux='images/projectiles/'+str(self.data[3])+'.png'
        self.projectile_image=pygame.image.load(aux).convert_alpha()
        self.projectile_speedV=self.data[2]
        self.cooldown=int((1/self.data[1])*1000)


#######################################
############## ITEMS ##################
#######################################
class Shield:
    def __init__(self,name,perc):
        global items_db_cursor
        # read data
        items_db_cursor.execute('SELECT * FROM items WHERE name="'+name+'"')
        self.data=items_db_cursor.fetchall()[0]
        self.stringName=name

        self.name=name
        self.function='Defensive'
        self.cost=75000
        self.hp=self.data[2]
        self.current_hp=int(self.hp*perc)
        self.multiplier=self.data[3]
        self.layers=0

        # pygame stuff
        file='images/items/'+str(self.data[1])+'.png'
        self.image=pygame.image.load(file).convert_alpha()
        self.image_2x=self.image
        self.rect=self.image.get_rect()

    def take_damage(self,dmg):
        # reduz a vida
        self.current_hp-=int(dmg*self.multiplier)
        if self.current_hp<=0:
            if self.layers>1:
                self.layers-=1
                self.current_hp=100
            else:
                self.current_hp=0
                self.layers-=1


class Energy_module:
    def __init__(self,name,perc):
        global items_db_cursor
        # read data
        items_db_cursor.execute('SELECT * FROM items WHERE name="'+name+'"')
        self.data=items_db_cursor.fetchall()[0]

        self.name=name
        self.stringName=name
        self.hp=self.data[2]
        self.current_hp=int(self.hp*perc)
        self.multiplier=self.data[3]

        #description
        self.cost=25000
        self.function=''

        # pygame stuff
        file='images/items/'+str(self.data[1])+'.png'
        self.image=pygame.image.load(file).convert_alpha()
        self.image_2x=self.image
        self.rect=self.image.get_rect()

    def take_damage(self,dmg):
        self.current_hp-=dmg
        if self.current_hp<0:
            self.current_hp=0


#######################################
######### SHIP DO PLAYER ##############
#######################################
class Ship:
    def __init__(self,index):
        global items_db_cursor,data_db_cursor

        data_db_cursor.execute('SELECT * FROM ships WHERE ID='+str(index))
        self.shipdata=data_db_cursor.fetchall()[0]
        self.index=index
        self.energy_module=copy(items_dict.get(self.shipdata[1]))
        self.energy_module.current_hp=self.energy_module.hp*self.shipdata[8]
        self.shield=copy(items_dict.get(self.shipdata[2]))
        self.shield.current_hp=self.shield.hp*self.shipdata[7]
        self.shield.layers=self.shipdata[9]

        self.skin=self.shipdata[3]

        # para colisao
        self.origin='Player'
        self.damage=self.energy_module.current_hp*1000

        #weapons
        self.load_weapons()

        # control
        self.movetime=pygame.time.get_ticks()
        self.jettime=pygame.time.get_ticks()
        self.jet_status_time=pygame.time.get_ticks()
        self.direction=None
        self.last_jet=0
        self.jet_status=False
        self.x=0
        self.has_no_weapons=False
        self.pseudo=True
        self.dead=False

        # lista com 5 images de inclina??o 0->4
        if 1:
            self.print('\t loading ship images...')
            imagespath='images/ship/'+str(self.skin)+'/ship_'
            self.images=[]
            aux=imagespath+'lean_left_2.png'
            self.images.append(pygame.image.load(aux).convert_alpha())
            aux=imagespath+'lean_left_1.png'
            self.images.append(pygame.image.load(aux).convert_alpha())
            aux=imagespath+'straight.png'
            self.images.append(pygame.image.load(aux).convert_alpha())
            aux=imagespath+'lean_right_1.png'
            self.images.append(pygame.image.load(aux).convert_alpha())
            aux=imagespath+'lean_right_2.png'
            self.images.append(pygame.image.load(aux).convert_alpha())

            for i in range(5):
                self.images[i]=pygame.transform.scale(self.images[i],(68,80))

            # assume a posi??o central como padrao
            self.image=self.images[2]
            self.rect=self.image.get_rect()
            self.rect.center=(640,750)

        # carrega os sprites
        # todos tem 8px de largura
        # só serao colocados no render qnd entrar em batalha
        if 1:
            self.print('\t loading jet sprays...')
            imagespath='images/ship/'+str(self.skin)+'/jet_spray/'
            self.images_spray=[]
            aux=imagespath+'spray10.png'
            self.images_spray.append(pygame.image.load(aux).convert_alpha())

            for i in range(11):
                aux=imagespath+'spray'+str(20+(i*2))+'.png'
                self.images_spray.append(pygame.image.load(aux).convert_alpha())

            # sprite do shield tomando dano
            self.shield_anim=sprites_dict.get('ship_shield')
            self.shield_anim._loop=False

            aux='images/ship/shield/0.png'
            self.shield_image=pygame.image.load(aux).convert_alpha()
            self.shield_rect=self.shield_image.get_rect()
            self.shield_rect.centerx=self.rect.centerx
            self.shield_rect.centery=self.rect.centery

        # audio para tomar dano
        if 1:
            aux='sounds/ship/shield.ogg'
            self.shield_sound=pygame.mixer.Sound(aux)
            self.shield_sound.set_volume(SFXVOL)

        # audio de trocar de arma
        if 1:
            aux='sounds/ship/change_weapon.ogg'
            self.switch_weapon_sound=pygame.mixer.Sound(aux)
            self.switch_weapon_sound.set_volume(SFXVOL*0.9)


        if 1:
            if enable_shadows:
                self.print('\t loading ship shadows...')
                imagespath='images/ship/'+str(self.skin)+'/shadows/ship_'
                self.shadow_images=[]
                aux=imagespath+'lean_left_2.png'
                self.shadow_images.append(pygame.image.load(aux).convert_alpha())
                aux=imagespath+'lean_left_1.png'
                self.shadow_images.append(pygame.image.load(aux).convert_alpha())
                aux=imagespath+'straight.png'
                self.shadow_images.append(pygame.image.load(aux).convert_alpha())
                aux=imagespath+'lean_right_1.png'
                self.shadow_images.append(pygame.image.load(aux).convert_alpha())
                aux=imagespath+'lean_right_2.png'
                self.shadow_images.append(pygame.image.load(aux).convert_alpha())

                # for i in self.shadow_images:
                # i.set_alpha(50)
                render.player_shadow=Object(self.shadow_images[2],400,400,0,0)
                # sombras

    def load_weapons(self):
        self.weapon_magazine=[]
        self.active_weapon=self.shipdata[5]
        if self.active_weapon==10:
            self.has_no_weapons=True
        weapons_to_load=self.shipdata[4]

        for i in range(13):
            self.weapon_magazine.append(None)
        j=0
        possibilidades=['0','1','2','3','4','5','6','7','8','9','a','b','c']
        for i in possibilidades:
            if i in weapons_to_load:
                self.weapon_magazine[j]=copy(items_dict.get(i))
            j+=1

        self.megabomb_weapon=Mega_Bomb('Mega Bomb')
        self.bombs=0

    def switch_weapon(self,weapon_object_number,op=None):
        if self.has_no_weapons:
            self.switch_weapon_sound.play()
        else:
            if op==None:
                lastwpn=self.active_weapon
                self.active_weapon+=1
                while(self.weapon_magazine[self.active_weapon]==None or self.active_weapon>=10):
                    self.active_weapon+=1
                    if self.active_weapon>=10:
                        self.active_weapon=0
                self.switch_weapon_sound.play()
            else:
                if self.weapon_magazine[op]!=None:
                    self.switch_weapon_sound.play()
                    self.active_weapon=op

            #ja troca o iconezinho do render!!
            if lastwpn in [9]:
                self.weapon_magazine[lastwpn].deactivate()
            self.weapon_magazine[self.active_weapon].activate()
            render.objects[weapon_object_number]=self.weapon_magazine[self.active_weapon]

    def redefine_magazine(self):
        self.active_weapon=10
        self.has_no_weapons=True
        for i in range(10):
            if self.weapon_magazine[i]!=None:
                self.active_weapon=i
                self.has_no_weapons=False

    def move(self,p):
        self.x=p[0]-self.rect.centerx
        y=p[1]-self.rect.centery
        if pygame.time.get_ticks()-self.movetime>=25:
            self.movetime=pygame.time.get_ticks()

            # anda a nave
            self.rect.move_ip(self.x,y)


            # anda a arma se necessário
            #if self.active_weapon in [9]:
            #    self.weapon_magazine[self.active_weapon].move(self.rect.center)

            if enable_shadows:
                render.player_shadow.rect.centerx=interpolate(self.rect.centerx,34,1246,-100,1380)
                render.player_shadow.rect.centery=interpolate(self.rect.centery,40,760,-80,880)

            # anda os jatinhos
            render.sprays[0].rect.move_ip(self.x,y)
            render.sprays[1].rect.move_ip(self.x,y)

            # acerta graficos da nave
            if self.direction==None or (self.direction==True and self.x<0) or (
                            self.direction==False and self.x>0) or pygame.time.get_ticks()-self.keep_pos>=500:
                self.keep_pos=pygame.time.get_ticks()

                # inclinação
                if self.x<-9:
                    self.image=self.images[0]
                    if enable_shadows:
                        render.player_shadow.image=self.shadow_images[0]
                    self.direction=False
                    render.sprays[0].rect.right=self.rect.centerx+2
                    render.sprays[1].rect.left=self.rect.centerx-2
                elif self.x<-5:
                    self.image=self.images[1]
                    if enable_shadows:
                        render.player_shadow.image=self.shadow_images[1]
                    self.direction=False
                    render.sprays[0].rect.right=self.rect.centerx-2
                    render.sprays[1].rect.left=self.rect.centerx+2
                elif self.x<5:
                    if self.direction!=None:
                        self.image=self.images[2]
                        if enable_shadows:
                            render.player_shadow.image=self.shadow_images[2]
                        self.direction=None
                        render.sprays[0].rect.right=self.rect.centerx-5
                        render.sprays[1].rect.left=self.rect.centerx+5
                elif self.x<12:
                    self.image=self.images[3]
                    if enable_shadows:
                        render.player_shadow.image=self.shadow_images[3]
                    self.direction=True
                    render.sprays[0].rect.right=self.rect.centerx-2
                    self.direction=True
                    render.sprays[0].rect.right=self.rect.centerx+2
                    render.sprays[1].rect.left=self.rect.centerx-2

        if pygame.time.get_ticks()-self.jettime>=16:
            self.jettime=pygame.time.get_ticks()
            # acerta os jatinhos
            # define grau de intensidade e ja acerta o volume do jato canal 3

            if y>0:
                n=0
                sound_engine.mixer.channel[3].set_volume(SFXVOL*0.3)
            elif y==0:
                n=1
                sound_engine.mixer.channel[3].set_volume(0.5*SFXVOL)
            elif y==-1:
                n=3
                sound_engine.mixer.channel[3].set_volume(0.6*SFXVOL)
            elif y==-2:
                n=5
                sound_engine.mixer.channel[3].set_volume(0.7*SFXVOL)
            elif y==-3:
                n=7
                sound_engine.mixer.channel[3].set_volume(0.8*SFXVOL)
            elif y==-4:
                n=9
                sound_engine.mixer.channel[3].set_volume(0.9*SFXVOL)
            else:
                n=11
                sound_engine.mixer.channel[3].set_volume(1*SFXVOL)

            # define um index n, do grau de jato, 11 mais forte, 0 fraco
            # se esta em um mivel novo,é automaticamente alterado, se nao randomiza
            # a cada 200ms
            if self.last_jet==n and pygame.time.get_ticks()-self.jet_status_time>=200:
                self.jet_status_time=pygame.time.get_ticks()
                if self.jet_status:
                    if n<=5:
                        a=random.randrange(9)+1
                        render.sprays[0].image=self.images_spray[a]
                        render.sprays[1].image=self.images_spray[a]
                        self.jet_status=False
                else:
                    render.sprays[0].image=self.images_spray[n]
                    render.sprays[1].image=self.images_spray[n]
                    self.jet_status=True
            else:
                render.sprays[0].image=self.images_spray[n]
                render.sprays[1].image=self.images_spray[n]
                self.jet_status=True
                self.last_jet=n

    def fire(self):
        #atira com as passivas
        for i in range(3):
            if self.weapon_magazine[10+i]!=None:
                self.weapon_magazine[10+i].fire(self.rect.center)


        #atira com a ativa
        if not self.has_no_weapons:
            return self.weapon_magazine[self.active_weapon].fire(self.rect.center)
        else:
            return None,None,None

    def unfire(self):
        if self.weapon_magazine[self.active_weapon]!=None:
            return self.weapon_magazine[self.active_weapon].unfire()

    def enter_battle(self):
        self.print('Entering battle')
        self.print('Initlizing back jets')
        # faz os jatos
        render.sprays.append(Object(self.images_spray[1],1000,1000,0,0))
        render.sprays.append(Object(self.images_spray[1],1000,1000,0,0))
        spraytop=self.rect.centery+38
        spray0right=self.rect.centerx-5
        spray1left=self.rect.centerx+5
        render.sprays[0].rect.top=spraytop
        render.sprays[1].rect.top=spraytop
        render.sprays[0].rect.right=spray0right
        render.sprays[1].rect.left=spray1left

        # faz a barrinha da vida
        self.print('Initlizing life bars')
        for i in range(100):
            a=(i+1)*8-4
            render.lines.append(line((1255,800-a),(1275,800-a),colors.RED,3))
        for i in range(100):
            a=(i+1)*8-4
            render.lines.append(line((5,800-a),(25,800-a),colors.YELLOW,3))

        # faz o overlay, que é as layers do shield
        for i in range(5):
            b=pygame.image.load('images/items/phase_shield_half.png')
            render.UI.append(Object(b,40+(40*i),-100,0,0))


        # inicializa TOOLS PARA armas
        self.line_n=len(render.lines)
        render.lines.append(line((0,0),(0,0),colors.WHITE,1))
        render.lines.append(line((0,0),(0,0),colors.WHITE,1))
        render.lines.append(line((0,0),(0,0),colors.WHITE,1))
        render.lines.append(line((0,0),(0,0),colors.WHITE,1))


        for i in [4,9]:
            if self.weapon_magazine[i]!=None:
                if i==4:
                    self.weapon_magazine[4].enter_battle(self.line_n)
                if i==9:
                    self.weapon_magazine[9].enter_battle(self.line_n,self)

        if self.active_weapon!=10:
            self.weapon_magazine[self.active_weapon].activate()

        self.update_bars()

    def update_bars(self):

        for i in range(100):
            if i<self.energy_module.current_hp:
                a=(i+1)*8-4
                render.lines[i+2].start=(1255,800-a)
                render.lines[i+2].end=(1275,800-a)
            else:
                render.lines[i+2].start=(1300,800)
                render.lines[i+2].end=(1300,800)

        for i in range(100):
            if i<(self.shield.current_hp):
                a=(i+1)*8-4
                render.lines[i+102].start=(5,800-a)
                render.lines[i+102].end=(25,800-a)
            else:
                render.lines[i+102].start=(1300,800)
                render.lines[i+102].end=(1300,800)


        for i in range(5):
            render.UI[i].rect.top=-100

        for i in range(self.shield.layers):
            render.UI[i].rect.top=5

    def take_damage(self,dmg,projectile_x):
        if self.shield.current_hp>0:
            self.shield.take_damage(dmg)
            self.shield_sound.play()
            self.shield_anim.play()
            self.update_bars()
        else:
            self.energy_module.take_damage(dmg)
            spawn_sprite(projectile_x,self.rect.centery-10,'small_explosion')
            play_sound('ship_hull')
            self.update_bars()
            if self.energy_module.current_hp<=0:
                self.dead=1
                return True

    def print(self,str):
        print(Fore.LIGHTRED_EX+'[SHIP] '+Fore.RESET+str)

    def blit(self,screen):
        screen.blit(self.image,self.rect)
        self.shield_anim.blit(screen,(self.rect.centerx-110,self.rect.centery-110))

    def colliderect(self,rect):
        if self.shield.current_hp>0:
            self.shield_rect.center=self.rect.center
            return self.shield_rect.colliderect(rect)
        else:
            return self.rect.colliderect(rect)

    def save(self,cursor):
        a='UPDATE ships SET'
        a+=' energylvl='+str(self.energy_module.current_hp/100)
        a+=' ,shieldlvl='+str(self.shield.current_hp/100)
        a+=' ,Weapon1='+str(self.active_weapon)
        a+=" ,Weapon0='"+self.get_weapons_string()+"'"
        a+=' ,shield_layers='+str(self.shield.layers)
        a+=" WHERE id="+str(self.index)
        print(a)
        cursor.execute(a)

    def get_weapons_string(self):
        a=''
        possibilidades=['0','1','2','3','4','5','6','7','8','9','a','b','c']
        for i in range(13):
            if self.weapon_magazine[i]!=None:
                a+=possibilidades[i]

        print(a)
        return a

#######################################
######### SHIPS INIMIGAS ##############
#######################################
# seletor de sprites dependendo do dano
def damage_taken_sprite_selector(source):
    if source.origin=='Machine GunL' or source.origin=='Machine GunR':
        a=random.randrange(4)
        if a<=1:
            return 'yellow_spark'
        elif a==2:
            return 'blue_spark'
        else:
            return 'red_spark'
    elif source.origin=='Air/Air Missle':
        return 'small_explosion'
    elif source.origin=='Laser Turret':
        return 'laser_turret_hit'
    # player
    elif source.origin=='Player':
        return 'medium_explosion'
    elif source.origin=='Twin Laser':
        return 'null'
    else:
        return 'null'

#-/> AS SHIPS ESTAO HARDCODED INDIVIDUALMENTE!!!!!!!!!!!!
class enemy_ship_0:
    def __init__(self,*args,**kwargs):  # tem q passar pos_list,e spawn_dist nos kwargs
        self.hp=1000
        self.cooldown=int((1/0.7)*1000)
        self.value=1000

        # lista de pontos de posicionamento
        self.pos_list=kwargs.get('pos_list')

        # lista de velocidades entre pontos
        self.speed_list,self.max_speed=get_speed_list(self.pos_list)

        # posicção inicial=0
        self.pos_n=0
        self.pos_max=len(self.pos_list)-2

        self.vx=self.speed_list[self.pos_n][0]
        self.vy=self.speed_list[self.pos_n][1]
        self.x=self.pos_list[0][0]
        self.y=self.pos_list[0][1]

        # definir weapon
        self.weapon=flak('Flak')
        self.offsetL=33
        self.offsetR=33

        # controle da engine principal
        self.alive=True
        self.was_killed=False
        self.spawn_distance=kwargs.get('spawn_dist')

        # definir imagem
        aux='images/ship/enemies/0.png'
        self.image=pygame.image.load(aux).convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.center=(self.x,self.y)

        aux='images/ship/0/jet_spray/spray40.png'
        self.jet=pygame.image.load(aux).convert_alpha()
        self.jet=pygame.transform.flip(self.jet,False,True)
        self.jet2=pygame.transform.smoothscale(self.jet,(20,33))
        self.jet=pygame.transform.smoothscale(self.jet,(20,40))
        self.jets=[]
        self.jets.append(Object(self.jet,0,0,0,0))
        self.jets.append(Object(self.jet,0,0,0,0))
        self.jets[0].rect.centerx=self.rect.centerx
        self.jets[1].rect.centerx=self.rect.centerx
        for i in self.jets:
            i.rect.bottom=self.rect.centery-22

        self.jet_time=pygame.time.get_ticks()
        self.jet_style=True

        # definir sombra
        if enable_shadows:
            aux='images/ship/enemies/shadows/0.png'
            self.shadow_image=pygame.image.load(aux).convert_alpha()
            self.shadow_rect=self.shadow_image.get_rect()
            self.shadow_rect.center=(-1000,-1000)
        self.time=0

    def fire(self):
        if pygame.time.get_ticks()-self.weapon.clock>=self.cooldown:
            self.weapon.clock=pygame.time.get_ticks()
            render.projectiles.append(
                Projectile(self.weapon.projectile_image,self.rect.centerx-self.offsetL,self.rect.centery,0,
                           self.weapon.projectile_speedV,'centered',damage=self.weapon.damage,friendly=False))
            render.projectiles.append(
                Projectile(self.weapon.projectile_image,self.rect.centerx+self.offsetR,self.rect.centery,0,
                           self.weapon.projectile_speedV,'centered',damage=self.weapon.damage,friendly=False))
            play_sound('flak')

    def update_rect(self):
        # move
        if check_point(self.pos_list[self.pos_n+1],self.rect.center,self.max_speed):
            if self.pos_n<self.pos_max:
                self.pos_n+=1
                self.vx=self.speed_list[self.pos_n][0]
                self.vy=self.speed_list[self.pos_n][1]

        self.x+=self.vx
        self.y+=self.vy
        self.rect.center=(self.x,self.y)

        # acerta os jatos
        self.jets[0].rect.centerx=self.rect.centerx-32
        self.jets[1].rect.centerx=self.rect.centerx+32
        self.jets[0].rect.centery=self.rect.centery-40
        self.jets[1].rect.centery=self.rect.centery-40

        if pygame.time.get_ticks()-self.jet_time>=100:
            self.jet_time=pygame.time.get_ticks()
            if self.jet_style:
                for i in self.jets:
                    i.image=self.jet
                    self.jet_style=False
            else:
                for i in self.jets:
                    i.image=self.jet2
                    self.jet_style=True

        # acerta as sombras
        if enable_shadows:
            self.shadow_rect.centerx=interpolate(self.rect.centerx,34,1246,-100,1380)
            self.shadow_rect.centery=interpolate(self.rect.centery,40,760,-80,880)

        if self.rect.top>=sresV or self.alive==False:
            return True

    def blit(self,screen):
        for i in self.jets:
            screen.blit(i.image,i.rect)
        screen.blit(self.image,self.rect)

    def blit_shadow(self,screen):
        screen.blit(self.shadow_image,self.shadow_rect)

    def take_damage(self,source):
        self.hp-=source.damage
        if source.pseudo:
            spawn_sprite(self.rect.centerx,self.rect.centery,damage_taken_sprite_selector(source))
        else:
            spawn_sprite(source.rect.centerx,source.rect.centery,damage_taken_sprite_selector(source))

        # se morreu...
        if self.hp<=0:  # faz toda a ceniunha
            self.alive=False
            self.was_killed=True
            spawn_sprite(self.rect.centerx,self.rect.centery,'medium_explosion')  # --tem q ser a medium
            play_sound('medium_explosion')
            return True


class enemy_ship_1:
    def __init__(self,*args,**kwargs):  # tem q passar pos_list,e spawn_dist nos kwargs
        self.hp=750
        self.cooldown=int((1/1)*1000)
        self.value=500

        # lista de pontos de posicionamento
        if 1:
            self.pos_list=kwargs.get('pos_list')

            # lista de velocidades entre pontos
            self.speed_list,self.max_speed=get_speed_list(self.pos_list)

            # posicção inicial=0
            self.pos_n=0
            self.pos_max=len(self.pos_list)-2

            self.vx=self.speed_list[self.pos_n][0]
            self.vy=self.speed_list[self.pos_n][1]
            self.x=self.pos_list[0][0]
            self.y=self.pos_list[0][1]

        # definir weapon
        self.weapon=flak('Flak')
        self.offsetH=+20

        # controle da engine principal
        self.alive=True
        self.was_killed=False
        self.spawn_distance=kwargs.get('spawn_dist')

        # definir imagem
        aux='images/ship/enemies/1.png'
        self.image=pygame.image.load(aux).convert_alpha()
        self.image=pygame.transform.smoothscale(self.image,(100,77))
        self.rect=self.image.get_rect()
        self.rect.center=(self.x,self.y)

        aux='images/ship/0/jet_spray/spray40.png'
        self.jet=pygame.image.load(aux).convert_alpha()
        self.jet=pygame.transform.flip(self.jet,False,True)
        self.jet2=pygame.transform.smoothscale(self.jet,(20,33))
        self.jet=pygame.transform.smoothscale(self.jet,(20,40))
        self.jets=[]
        self.jets.append(Object(self.jet,0,0,0,0))
        self.jets.append(Object(self.jet,0,0,0,0))
        self.jets[0].rect.centerx=self.rect.centerx+10
        self.jets[1].rect.centerx=self.rect.centerx+10
        for i in self.jets:
            i.rect.bottom=self.rect.centery-30  # ---> quanto o jato ta para tras do centro

        self.jet_time=pygame.time.get_ticks()
        self.jet_style=True

        # definir sombra
        if enable_shadows:
            aux='images/ship/enemies/shadows/1.png'
            self.shadow_image=pygame.image.load(aux).convert_alpha()
            self.shadow_image=pygame.transform.smoothscale(self.shadow_image,(100,77))
            self.shadow_rect=self.shadow_image.get_rect()
            self.shadow_rect.center=(-1000,-1000)
        self.time=0

    def fire(self):
        if pygame.time.get_ticks()-self.weapon.clock>=self.cooldown:
            self.weapon.clock=pygame.time.get_ticks()
            render.projectiles.append(
                Projectile(self.weapon.projectile_image,self.rect.centerx,self.rect.centery+self.offsetH,0,
                           self.weapon.projectile_speedV,'centered',damage=self.weapon.damage,friendly=False))
            play_sound('flak')

    def update_rect(self):
        # move
        if check_point(self.pos_list[self.pos_n+1],self.rect.center,self.max_speed):
            if self.pos_n<self.pos_max:
                self.pos_n+=1
                self.vx=self.speed_list[self.pos_n][0]
                self.vy=self.speed_list[self.pos_n][1]

        self.x+=self.vx
        self.y+=self.vy
        self.rect.center=(self.x,self.y)

        # acerta os jatos
        self.jets[0].rect.centerx=self.rect.centerx-32
        self.jets[1].rect.centerx=self.rect.centerx+32
        self.jets[0].rect.centery=self.rect.centery-40
        self.jets[1].rect.centery=self.rect.centery-40

        if pygame.time.get_ticks()-self.jet_time>=100:
            self.jet_time=pygame.time.get_ticks()
            if self.jet_style:
                for i in self.jets:
                    i.image=self.jet
                    self.jet_style=False
            else:
                for i in self.jets:
                    i.image=self.jet2
                    self.jet_style=True

        # acerta as sombras
        if enable_shadows:
            self.shadow_rect.centerx=interpolate(self.rect.centerx,34,1246,-100,1380)
            self.shadow_rect.centery=interpolate(self.rect.centery,40,760,-80,880)

        if self.rect.top>=sresV or self.alive==False:
            return True

    def blit(self,screen):
        for i in self.jets:
            screen.blit(i.image,i.rect)
        screen.blit(self.image,self.rect)

    def blit_shadow(self,screen):
        screen.blit(self.shadow_image,self.shadow_rect)

    def take_damage(self,source):
        self.hp-=source.damage
        spawn_sprite(self.rect.centerx,self.rect.centery,damage_taken_sprite_selector(source))

        # se morreu...
        if self.hp<=0:  # faz toda a ceniunha
            self.alive=False
            self.was_killed=True
            spawn_sprite(self.rect.centerx,self.rect.centery,'medium_explosion')  # --tem q ser a medium
            play_sound('medium_explosion')
            return True


#########################################
########### FUNÇOES AUXILIARES ##########
#########################################
def interpolate(value,fromLow,fromHigh,toLow,toHigh):
    # interpolação simples linear
    return ((toHigh-toLow)/(fromHigh-fromLow))*(value-fromLow)+toLow


def chk_sign(v):
    if v>0:
        return 1
    elif v<0:
        return -1
    else:
        return 0


def get_speed(start,end):
    # start tem 3 elementos o 3o eh o tempo
    x=end[0]-start[0]
    y=end[1]-start[1]
    t=start[2]/16

    if x!=0 and y!=0:
        a=(x/t,y/t)
    elif y==0 and x!=0:
        a=(x/t,0)
    elif x==0 and y!=0:
        a=(0,y/t)
    else:
        a=(0,0)
    return a


def get_speed_list(list):
    n=len(list)-1
    speed_list=[]
    max=0
    for i in range(n):
        start=(list[i][0],list[i][1],list[i][2])
        end=(list[i+1][0],list[i+1][1])
        speed_list.append(get_speed(start,end))

    for i in speed_list:
        if i[0]>max:
            max=i[0]
        if i[1]>max:
            max=i[1]

    return speed_list,max


def check_point(desired,current,tol):
    return abs(desired[0]-current[0])<=tol and abs(desired[1]-current[1])<=tol


def get_distance(p1,p2):
    x=abs(p1[0]-p2[0])
    y=abs(p1[1]-p2[1])
    y=y**2
    x=x**2
    d=int(math.sqrt(x+y))
    return d


def check_if_on_screen(rect):
    if rect.right>0 and rect.left<sresH and rect.top>-20 and rect.bottom<sresV+20:
        return True
    else:
        return False


def get_if_have(ship,cursor):
    if cursor==0:
        return ship.energy_module.current_hp
    elif cursor==1:
        return ship.shield.layers
    elif cursor==2:
        return ship.bombs
    elif cursor==3:
        return ship.weapon_magazine[10]!=None
    elif cursor==4:
        return ship.weapon_magazine[12]!=None
    elif cursor==5:
        return ship.weapon_magazine[11]!=None
    elif cursor==6:
        return ship.weapon_magazine[0]!=None
    elif cursor==7:
        return ship.weapon_magazine[1]!=None
    elif cursor==8:
        return ship.weapon_magazine[7]!=None
    elif cursor==9:
        return ship.weapon_magazine[2]!=None
    elif cursor==10:
        return ship.weapon_magazine[3]!=None
    elif cursor==11:
        return ship.weapon_magazine[5]!=None
    elif cursor==12:
        return ship.weapon_magazine[4]!=None
    elif cursor==13:
        return ship.weapon_magazine[6]!=None
    elif cursor==14:
        return ship.weapon_magazine[8]!=None
    elif cursor==15:
        return ship.weapon_magazine[9]!=None


def get_wpn_index_on_ship(cursor):
    if cursor==4:
        return 12
    elif cursor==5:
        return 11
    elif cursor==6:
        return 0
    elif cursor==7:
        return 1
    elif cursor==8:
        return 7
    elif cursor==9:
        return 2
    elif cursor==10:
        return 3
    elif cursor==11:
        return 5
    elif cursor==12:
        return 4
    elif cursor==13:
        return 6
    elif cursor==14:
        return 8
    elif cursor==15:
        return 9


def get_index(cursor):
    if cursor==3:
        return 10
    elif cursor==4:
        return 12
    elif cursor==5:
        return 11
    elif cursor==6:
        return 0
    elif cursor==7:
        return 1
    elif cursor==8:
        return 7
    elif cursor==9:
        return 2
    elif cursor==10:
        return 3
    elif cursor==11:
        return 5
    elif cursor==12:
        return 4
    elif cursor==13:
        return 6
    elif cursor==14:
        return 8
    elif cursor==15:
        return 9


def buy_weapon(player,cursor):
    #retorna -1 se n tem dinheiro
    #retorna -2 se jha tem aa arma
    if shop_magazine[cursor].cost>player.money:
        return -1
    else:
        if cursor==0:
            if player.ship.energy_module.current_hp<100:
                player.ship.energy_module.current_hp+=25
                if player.ship.energy_module.current_hp>100:
                    player.ship.energy_module.current_hp=100
                player.money-=shop_magazine[cursor].cost
                return 0
            else:
                return -2

        elif cursor==1:
            if player.ship.shield.layers<5:
                if player.ship.shield.layers==0:
                    player.ship.shield.layers+=1
                    player.ship.shield.current_hp=100
                else:
                    player.ship.shield.layers+=1
                if player.ship.shield.layers>5:
                    player.ship.shield.layers=5
                player.money-=shop_magazine[cursor].cost
                return 0
            else:
                return -2

        elif cursor==2:
            if player.ship.bombs<5:
                player.ship.bombs+=1
                if player.ship.bombs>5:
                    player.ship.bombs=5
                player.money-=shop_magazine[cursor].cost
                return 0
            else:
                return -2

        elif cursor==6:
            if get_if_have(player.ship,cursor):
                return -2
            else:
                player.ship.weapon_magazine[get_index(cursor)]=AA_missle('Air/Air Missle')
                player.money-=shop_magazine[cursor].cost
                return 0

        elif cursor==12:
            if get_if_have(player.ship,cursor):
                return -2
            else:
                player.ship.weapon_magazine[get_index(cursor)]=Laser_turret('Laser Turret')
                player.money-=shop_magazine[cursor].cost
                return 0

        elif cursor==15:
            if get_if_have(player.ship,cursor):
                return -2
            else:
                player.ship.weapon_magazine[get_index(cursor)]=Twin_Laser('Twin Laser')
                player.money-=shop_magazine[cursor].cost
                return 0
        else:
            return 0


def get_list_index(val,list):
    k=0
    for i in list:
        if i==val:
            return k
        k+=1
    return None


def sell_weapon(player,cursor,display):
    if cursor==0:
        if player.ship.energy_module.current_hp>=26:
            player.ship.energy_module.current_hp-=25
            player.money+=int(shop_magazine[cursor].cost/2)
            if player.ship.energy_module.current_hp<25:
                display.nones_items.append(cursor)
                return -1
            return 0

    elif cursor==1:
        if player.ship.shield.layers>0:
            if player.ship.shield.current_hp==100:
                player.ship.shield.layers-=1
                player.money+=int(shop_magazine[cursor].cost/2)
            if player.ship.shield.layers==0:
                display.nones_items.append(cursor)
                return -1
            return 0

    elif cursor==2:
        if player.ship.bombs>0:
            player.ship.bombs-=1
            player.money+=int(shop_magazine[cursor].cost/2)
            if player.ship.bombs==0:
                display.nones_items.append(cursor)
                return -1
            return 0

    elif cursor==3:
        return 0

    else:
        player.ship.weapon_magazine[get_wpn_index_on_ship(cursor)]=None
        player.money+=int(shop_magazine[cursor].cost/2)
        display.nones_items.append(cursor)
        return -1
