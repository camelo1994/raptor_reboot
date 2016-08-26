import mouse_spots,colors,def_lib,render,sound_engine
import sqlite3,pygame,pyganim,random,colorama,copy
from render import *
from sound_engine import *
from colorama import Fore

data_db=None
data_db_cursor=None
items_db=None
items_db_cursor=None
sprites_dict={}
audio_dict={}

sresH=1280
sresV=800


#inicializacoes
def init(a,b):
    global data_db,items_db,data_db_cursor,items_db_cursor
    #connect to Database
    print('SQL: Connecting to SQL database: '+a)
    data_db=sqlite3.connect(a)
    data_db_cursor=data_db.cursor()
    print('SQL: Connecting to SQL database: '+b)
    items_db=sqlite3.connect(b)
    items_db_cursor=items_db.cursor()
    start_sprite_dict()
    start_audio_dict()


def start_sprite_dict():
    global sprites_dict
    #inicia um dicionario global de sprites
    print('Initializing sprites dictionary')

    #'small_explosion'
    spritelist=[]
    for i in range(14):
        aux='sprites/small_explosion/'+str(i)+'.png'
        spritelist.append((aux,100))
        sprites_dict['small_explosion']=pyganim.PygAnimation(spritelist)


def start_audio_dict():
    global audio_dict

    #inicia um dicionario global de soms
    print('Initializing audio dictionary')

    #barulho da arma flak - 'flak'
    aux='sounds/weapons/flak.ogg'
    aux=pygame.mixer.Sound(aux)
    aux.set_volume(0.3)
    audio_dict['flak']=aux

    #barulho da explosao media - 'medium_explosion'
    aux='sounds/medium_explosion.ogg'
    aux=pygame.mixer.Sound(aux)
    aux.set_volume(1)
    audio_dict['medium_explosion']=aux




#chamadas
def spawn_sprite(x,y,key,dx=0,dy=0):
    global sprites_dict
    if key in sprites_dict:
        n=len(render.sprites)
        render.sprites.append(Animation(sprites_dict.get(key),anim_rect(x,y,dx,dy,100,100)))
        render.sprites[n].animation.play()
    else:
        print('There is no sprite: '+key)


def play_sound(key):
    global audio_dict
    if key in audio_dict:
        n=sound_engine.mixer.find_channel()
        if n != None:
            sound_engine.mixer.channel[n].play(audio_dict.get(key))
    else:
        print('There is no audio: '+key)


def spawn(ID,posx):
    if ID==0:
        render.enemy_ships.append(enemy_ship_0(posx))


class text:#(str,ttf_file,size,color,cx,cy,abs?) none=center / 1=topleft / 2=topright
    def __init__(self,str,ttf_file,size,color,cx,cy,abs=None):
        #local defs
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

class line:#(start,end,color,width)
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


class Player:
    def __init__(self,aux):
        self.name=aux[1]
        self.callsign=aux[2]
        self.shipname=aux[3]
        self.imageindex=aux[4]
        self.shipindex=aux[5]

        self.ship=Ship(self.shipindex)
        #internal
        self.money=50000

        #pygame stuff
        picture_file_path='images/profiles/'+str(self.imageindex)+'.jpg'
        print('loading file: '+picture_file_path)
        self.image=pygame.image.load(picture_file_path)
        self.rect=self.image.get_rect()


class Cursor:
    def __init__(self,image):
        self.image=image
        #self.rect=image.get_rect()
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

            #atualiza os graficos do render
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


class menu:#(settings_file,profiles_file,crosshair_file,bgm_file):
    def __init__(self,crosshair_file,bgm_file,bgm_file2,button_sound_file,button_select_file):
        self.print('Initializing menu...')

        #control variables
        self.status='loading'
        self.next_status=''
        self.in_menu=True
        self.changed=False
        self.ops=[]
        self.lastop=None
        self.op=None
        self.player_text_index=None
        self.button_sound_held=False
        self.selected=False

        #read saved data
        self.read_user_settings()
        self.player=self.read_player_profiles(self.profileindex)

        #start subsystems 
        self.print('Initalizing audio')
        self.button_sound=None
        self.select_sound=None
        self.start_sounds(button_sound_file,button_select_file)
        self.cursor=None
        self.start_cursor(crosshair_file)

        #music
        self.bgm=pygame.mixer.Sound(bgm_file)
        self.bgm2=pygame.mixer.Sound(bgm_file2)
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
        self.profileindex=self.settings[2]

    def read_player_profiles(self,i):

        data_db_cursor.execute('SELECT * FROM profiles')
        self.profile_list=data_db_cursor.fetchall()

        print('\t'+str(len(self.profile_list))+' Profiles detected')
        for n in self.profile_list:
            print('\t'+str(n))

        print('\n\tReading profile #'+str(i))
        aux=self.profile_list[i]

        return Player(aux)

    def save_data(self):
        self.print('Saving data')
        self.print('\t Global settings..')
        aux='UPDATE settings SET'+' bgm_volume='+str(self.bgm_volume)+','+'last_player='+str(self.profileindex)
        global data_db_cursor,data_db
        data_db_cursor.execute(aux)
        self.print('\tCommiting database')
        data_db.commit()

    def start_cursor(self,file):
        self.cursor=Cursor(pygame.image.load(file).convert_alpha())
        self.print('Cursor management started')

    def start_sounds(self,bsound,selsound):
        self.button_sound=pygame.mixer.Sound(bsound)
        self.select_sound=pygame.mixer.Sound(selsound)

    def bgm_toogle(self,bool=None):
        if bool==None:
            self.bgm=not self.bgm
        else:
            self.bgm=bool

    def sel_update(self):

        #verifica onde o mouse ta
        op=mouse_spots.check_selection(self.status,self.cursor.posX,self.cursor.posY)
        self.op=op
        #se estuver em cmia de um botao, fala pra ele ficar selecionado
        #se nao nao
        if op!=None:
            for i in range(len(render.buttons)):
                if i!=op:
                    render.buttons[i].swap_image(False)
                else:
                    render.buttons[i].swap_image(True)
        #se td estiver descelecionado eh td descelecionado
        else:
            for i in render.buttons:
                i.swap_image(False)
        #se tiver uma op diferente toca sonzinho
        if op!=self.lastop and op!=None:
            self.button_sound.play()
        #segura a ultia op pro p~óx ciclo
        self.lastop=op

        if (self.cursor.buttons)[0]==0:
            self.button_held=False

        if (self.cursor.buttons)[0]==1 and not self.button_held and op!=None:
            self.button_held=True
            action=mouse_spots.check_choice(self.status,op)
            #print(action)
            #para a??o interna:
            if action[0]=='$':
                #$-> troca de menu, ja se atualiza!
                if action[1]=='$':
                    self.swap(action[2:])
                    return action
                #%-> troca player selecionado
                elif action[1]=='%':
                    #print(action[2:])
                    self.swap_player(action[2:])
                #&-> salva os dados
                elif action[1]=='&':
                    self.save_user_profiles()
                    self.print('User data saved')
            else:

                return action

    def update(self,renderer):
        self.cursor.update(renderer)
        return self.sel_update()

    def swap_player(self,direction,revese=None):
        if direction=='+' and (self.profileindex+1)<=(len(self.profile_list)-1):
            self.profileindex+=1

            self.player=Player(self.profile_list[self.profileindex])
            self.print(
                '\tPlayer loaded: #'+str(self.profileindex)+' -> '+str(self.player.name+' '+str(self.player.callsign)))
            self.update_menu_profile_data()
            if self.selected:
                render.texts.pop()

        elif direction=='-' and (self.profileindex-1)>=0:
            self.profileindex-=1

            self.player=Player(self.profile_list[self.profileindex])
            self.print(
                '\tPlayer loaded: #'+str(self.profileindex)+' -> '+str(self.player.name)+' '+str(self.player.callsign))
            self.update_menu_profile_data()
            if self.selected:
                render.texts.pop()

        elif direction=='*':
            filepath='fonts/major_shift.ttf'
            self.print('loading file: '+filepath)
            render.texts.append(classes.text('player selected',filepath,24,colors.RED,970,700,1))
            self.selected=True
            self.lastprofile=self.profileindex


        elif direction=='**':
            self.profileindex=self.lastprofile
            self.player=Player(self.profile_list[self.profileindex])
            self.print(
                '\tPlayer loaded: #'+str(self.profileindex)+' -> '+str(self.player.name)+' '+str(self.player.callsign))
            self.update_menu_profile_data()
            self.swap('main')

    def update_menu_profile_data(self):
        render.objects[len(render.objects)-1].change_image(self.player.image)
        render.texts[self.player_text_index].update_text(self.player.name)
        render.texts[self.player_text_index+1].update_text(self.player.callsign)
        render.texts[self.player_text_index+2].update_text(self.player.shipname)

    def print(self,str):
        print(Fore.BLUE+'[MENU] '+Fore.RESET+str)


class Object:#(image,PosH,PosV,speedH,speedV):
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
        if 'friendly' in kwargs:
            self.friendly=kwargs.get('friendly')
        else:
            self.friendly=False
        self.valid=True

    def check_out(self):
        if self.rect.bottom<=-100 or self.rect.top>=900 or self.valid==False:
            return True


class MenuButton(Object):#(imagefileA,imagefileB,PosH,PosV,mode=None):
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


#SPRITEEEEEEESSSSSSSSSSSSS
class anim_rect:
    def __init__(self,x,y,dx,dy,h,w):
        self.dx=dx
        self.dy=dy
        self.pos=[x,y]
        self.h=h
        self.w=w

    def update_rect(self):
        self.pos[0]+=self.dx
        self.pos[1]+=self.dy
        if self.pos[0]>sresH+100 or self.pos[0]+self.w<-100 or self.pos[1]<-100 or self.pos[1]-self.h>sresV+100:
            return True


class Animation:
    def __init__(self,animation,rect,loop=False):
        self.animation=animation
        self.rect=rect
        self.loop=loop
        if loop==False:
            self.animation._loop=False

    def blit(self,screen):
        self.animation.blit(screen,(self.rect.pos[0],self.rect.pos[1]))

    def update_rect(self):
        if self.rect.update_rect():# or (not self.loop and self.animation.state=='stopped'):
            return True
        elif self.loop==False:
            if self.animation.state=='stopped':
                return True


#SHIP -STUFF



#define uma classe weapon genérica, define projectile e fire tem q ser providas
#pelas respectivasd subclasses
class Weapon:
    def __init__(self,name):
        global items_db_cursor
        #read data
        items_db_cursor.execute('SELECT * FROM weapons WHERE name="'+name+'"')
        self.data=items_db_cursor.fetchall()[0]
        self.name=name
        self.damage=self.data[2]

        #pygame stuff
        #image-self
        file='images/weapons/'+str(self.data[1])+'.png'
        print(file)
        self.image=pygame.image.load(file).convert_alpha()
        self.image=pygame.transform.scale(self.image,(50,50))

        self.rect=self.image.get_rect()
        self.rect.center=(sresH-60,28)
        #projectile
        self.projectile=None
        self.define_projectile()

        #clock
        self.clock=pygame.time.get_ticks()


#weapons do player
class AA_missle(Weapon):
    def define_projectile(self):
        self.projectile_image=pygame.image.load('images/projectiles/aa_missle.png').convert_alpha()
        self.projectile_image=pygame.transform.scale(self.projectile_image,(8,20))
        self.projectile_speedV=-12
        self.cooldown=self.data[3]

        #audio
        aux='sounds/weapons/aa_missle.ogg'
        self.fire_sound=pygame.mixer.Sound(aux)
        self.fire_sound.set_volume(0.4)

        self.missle_spritelist=[]
        for i in range(4):
            aux='sprites/missle_jet/'+str(i+1)+'.png'
            self.missle_spritelist.append((aux,25))
        self.anim=pyganim.PygAnimation(self.missle_spritelist)

    def fire(self,pos):
        # verifica se pode atirar
        if pygame.time.get_ticks()-self.clock>=self.cooldown:
            self.clock=pygame.time.get_ticks()
            #poe os 2 projeteis
            render.projectiles.append(
                Projectile(self.projectile_image,pos[0]+20,pos[1],0,self.projectile_speedV,friendly=True,
                           damage=self.damage))
            render.projectiles.append(
                Projectile(self.projectile_image,pos[0]-20,pos[1],0,self.projectile_speedV,friendly=True,
                           damage=self.damage))
            n=len(render.sprites)

            #poe os dois sprites de foguinho
            render.sprites.append(
                Animation(self.anim,anim_rect(pos[0]+18-5,pos[1]+20,0,self.projectile_speedV,20,50),True))
            render.sprites[n].animation.play()
            render.sprites.append(
                Animation(self.anim,anim_rect(pos[0]-18-5,pos[1]+20,0,self.projectile_speedV,20,50),True))
            render.sprites[n+1].animation.play()

            #toca barulinho
            sound_engine.mixer.channel[4].play(self.fire_sound)


class Machine_gun(Weapon):
    def define_projectile(self):
        self.projectile_image=pygame.image.load('images/projectiles/mg.png').convert_alpha()
        self.projectile_image=pygame.transform.scale(self.projectile_image,(4,4))
        self.projectile_image_inv=pygame.transform.flip(self.projectile_image,True,False)
        self.projectile_speedV=-50
        self.proj_style_left=False
        self.proj_style_right=True
        self.cooldown=self.data[3]

        # audio
        aux='sounds/weapons/mg.ogg'
        self.fire_sound=pygame.mixer.Sound(aux)
        self.fire_sound.set_volume(0.5)

    def fire(self,pos):
        # verifica se pode atirar
        if pygame.time.get_ticks()-self.clock>=self.cooldown:
            self.clock=pygame.time.get_ticks()
            # poe os 2 projeteis
            a=random.randrange(11)
            b=random.randrange(11)
            if a>5:
                render.projectiles.append(
                    Projectile(self.projectile_image_inv,pos[0]+15,pos[1],0,self.projectile_speedV,damage=self.damage,
                               friendly=True))
            else:
                render.projectiles.append(
                    Projectile(self.projectile_image,pos[0]+15,pos[1],0,self.projectile_speedV,damage=self.damage,
                               friendly=True))
            if b>5:
                render.projectiles.append(
                    Projectile(self.projectile_image_inv,pos[0]-15,pos[1],0,self.projectile_speedV,damage=self.damage,
                               friendly=True))
            else:
                render.projectiles.append(
                    Projectile(self.projectile_image,pos[0]-15,pos[1],0,self.projectile_speedV,damage=self.damage,
                               friendly=True))

            # toca barulinho
            sound_engine.mixer.channel[5].play(self.fire_sound)


#weapons dos inimigos
class flak():
    def __init__(self,name):
        global items_db_cursor
        #read data
        items_db_cursor.execute('SELECT * FROM enemy_weapons WHERE name="'+name+'"')
        self.data=items_db_cursor.fetchall()[0]

        self.name=name
        self.damage=self.data[2]

        self.projectile=None
        self.define_projectile()

        #clock
        self.clock=pygame.time.get_ticks()

    def define_projectile(self):
        aux='images/projectiles/'+str(self.data[3])+'.png'
        self.projectile_image=pygame.image.load(aux).convert_alpha()
        self.projectile_speedV=self.data[2]
        self.cooldown=int((1/self.data[1])*1000)

        aux='sounds/weapons/'+str(self.data[3])+'.ogg'
        self.fire_sound=pygame.mixer.Sound(aux)
        self.fire_sound.set_volume(0.4)


#items
class Shield:
    def __init__(self,name,perc):
        global items_db_cursor
        #read data
        items_db_cursor.execute('SELECT * FROM items WHERE name="'+name+'"')
        self.data=items_db_cursor.fetchall()[0]
        print(self.data)

        self.name=name
        self.hp=self.data[2]
        self.current_hp=int(self.hp*perc)
        self.multiplier=self.data[3]

        #pygame stuff
        file='images/items/'+str(self.data[1])+'.png'
        self.image=pygame.image.load(file).convert_alpha()
        self.rect=self.image.get_rect()

    def take_damage(self,dmg):
        #reduz a vida
        self.current_hp-=dmg
        if self.current_hp<0:
            self.current_hp=0


class Energy_module:
    def __init__(self,name,perc):
        global items_db_cursor
        #read data
        items_db_cursor.execute('SELECT * FROM items WHERE name="'+name+'"')
        self.data=items_db_cursor.fetchall()[0]
        print(self.data)

        self.name=name
        self.hp=self.data[2]
        self.current_hp=int(self.hp*perc)
        self.multiplier=self.data[3]

        #pygame stuff
        file='images/items/'+str(self.data[1])+'.png'
        self.image=pygame.image.load(file).convert_alpha()
        self.rect=self.image.get_rect()

    def take_damage(self,dmg):
        self.current_hp-=dmg
        if self.current_hp<0:
            self.current_hp=0


class Ship:
    def __init__(self,index):
        global items_db_cursor,data_db_cursor
        data_db_cursor.execute('SELECT * FROM ships WHERE ID='+str(index))
        shipdata=data_db_cursor.fetchall()[0]
        #define self data
        print('Defining ship: ')
        print(shipdata)

        self.energy_percent=shipdata[7]
        self.shield_percent=shipdata[8]

        self.energy_module=Energy_module(shipdata[1],self.energy_percent)
        self.shield=Shield(shipdata[2],self.shield_percent)

        self.skin=shipdata[3]

        self.weapon=[]
        for i in range(3):
            self.weapon.append(None)

        if shipdata[4]=='Air/Air Missle':
            self.weapon[0]=AA_missle(shipdata[4])
        if shipdata[5]=='Machine Gun':
            self.weapon[1]=Machine_gun(shipdata[5])

        #control
        self.movetime=pygame.time.get_ticks()
        self.jettime=pygame.time.get_ticks()
        self.jet_status_time=pygame.time.get_ticks()
        self.direction=None
        self.last_jet=0
        self.jet_status=False

        #lista com 5 images de inclina??o 0->4
        print('\t loading ship images...')
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

        #assume a posi??o central como padrao
        self.image=self.images[2]
        self.rect=self.image.get_rect()
        self.rect.center=(640,750)
        print('\timages-OK')

        #carrega os sprites
        #todos tem 8px de largura
        #só serao colocados no render qnd entrar em batalha
        print('\t loading jet sprays...')
        imagespath='images/ship/'+str(self.skin)+'/jet_spray/'
        self.images_spray=[]
        aux=imagespath+'spray10.png'
        self.images_spray.append(pygame.image.load(aux).convert_alpha())

        for i in range(11):
            aux=imagespath+'spray'+str(20+(i*2))+'.png'
            self.images_spray.append(pygame.image.load(aux).convert_alpha())

        #audio para tomar dano

        aux='sounds/ship/shield.ogg'
        self.shield_sound=pygame.mixer.Sound(aux)
        self.shield_sound.set_volume(1)

    def move(self,p):
        x=p[0]-self.rect.centerx
        y=p[1]-self.rect.centery
        if pygame.time.get_ticks()-self.movetime>=25:
            self.movetime=pygame.time.get_ticks()

            #anda a nave
            self.rect.move_ip(x,y)

            #anda os jatinhos
            render.sprays[0].rect.move_ip(x,y)
            render.sprays[1].rect.move_ip(x,y)

            #acerta graficos da nave   
            if self.direction==None or (self.direction==True and x<0) or (
                    self.direction==False and x>0) or pygame.time.get_ticks()-self.keep_pos>=500:
                self.keep_pos=pygame.time.get_ticks()

                #inclina??o
                if x<-9:
                    self.image=self.images[0]
                    self.direction=False
                    render.sprays[0].rect.right=self.rect.centerx+2
                    render.sprays[1].rect.left=self.rect.centerx-2

                elif x<-5:
                    self.image=self.images[1]
                    self.direction=False
                    render.sprays[0].rect.right=self.rect.centerx-2
                    render.sprays[1].rect.left=self.rect.centerx+2

                elif x<5:
                    if self.direction!=None:
                        self.image=self.images[2]
                        self.direction=None
                        render.sprays[0].rect.right=self.rect.centerx-5
                        render.sprays[1].rect.left=self.rect.centerx+5
                elif x<12:
                    self.image=self.images[3]
                    self.direction=True
                    render.sprays[0].rect.right=self.rect.centerx-2
                    render.sprays[1].rect.left=self.rect.centerx+2

                else:
                    self.image=self.images[4]
                    self.direction=True
                    render.sprays[0].rect.right=self.rect.centerx+2
                    render.sprays[1].rect.left=self.rect.centerx-2

        if pygame.time.get_ticks()-self.jettime>=16:
            self.jettime=pygame.time.get_ticks()
            #acerta os jatinhos
            #define grau de intensidade e ja acerta o volume do jato canal 3

            if y>0:
                n=0
                sound_engine.mixer.channel[3].set_volume(0.3)
            elif y==0:
                n=1
                sound_engine.mixer.channel[3].set_volume(0.5)
            elif y==-1:
                n=3
                sound_engine.mixer.channel[3].set_volume(0.6)
            elif y==-2:
                n=5
                sound_engine.mixer.channel[3].set_volume(0.7)
            elif y==-3:
                n=7
                sound_engine.mixer.channel[3].set_volume(0.8)
            elif y==-4:
                n=9
                sound_engine.mixer.channel[3].set_volume(0.9)
            else:
                n=11
                sound_engine.mixer.channel[3].set_volume(1)

            #define um index n, do grau de jato, 11 mais forte, 0 fraco
            #se esta em um mivel novo,é automaticamente alterado, se nao randomiza
            #a cada 200ms

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
        self.weapon[0].fire(self.rect.center)
        self.weapon[1].fire(self.rect.center)

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

        #faz a barrinha da vida
        self.print('Initlizing life bars')
        for i in range(100):
            a=(i+1)*8-4
            render.lines.append(line((1255,800-a),(1275,800-a),colors.RED,3))
        for i in range(100):
            a=(i+1)*8-4
            render.lines.append(line((5,800-a),(25,800-a),colors.YELLOW,3))

        self.update_bars()

    def update_bars(self):
        self.print('Shield/HP Bar:'+str(self.energy_module.current_hp)+'% '+str(self.shield.current_hp)+'%')

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

    def take_damage(self,dmg):
        if self.shield.current_hp>0:
            self.shield.take_damage(dmg)
            self.shield_sound.play()
        else:
            self.energy_module.take_damage(dmg)
        self.update_bars()

    def print(self,str):
        print(Fore.LIGHTRED_EX+'[SHIP] '+Fore.RESET+str)


#ships inimigas



class enemy_ship_0():
    def __init__(self,posx):
        global data_db_cursor
        #read data
        data_db_cursor.execute('SELECT * FROM enemies WHERE ID=0')
        self.data=data_db_cursor.fetchall()[0]

        self.hp=self.data[1]
        self.cooldown=int((1/self.data[2])*1000)
        self.speed=1#1*self.data[3]

        #definir weapon
        self.weapon=flak(self.data[4])
        self.offsetL=self.data[5]
        self.offsetR=self.data[6]

        self.alive=True

        #definir imagem
        aux='images/ship/enemies/0.png'
        self.image=pygame.image.load(aux).convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.center=(posx,100)

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
        self.rect=self.rect.move(0,self.speed)
        if self.rect.bottom<=-100 or self.alive==False:
            return True

    def take_damage(self,dmg):
        self.hp-=dmg
        if self.hp<=0:
            self.alive=False
            spawn_sprite(self.rect.left,self.rect.top,'small_explosion')#--tem q ser a medium
            play_sound('medium_explosion')
            return True
