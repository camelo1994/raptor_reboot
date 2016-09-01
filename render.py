import threading,time,pygame,colors,os,classes,colorama
from colorama import Fore

#se tiver #$ na frente eh pq usa in-game
objects=[]#$
texts=[]#$
lines=[]#$
cursors=[]
buttons=[]
projectiles=[]#$
sprays=[]#$
sprites=[]#$
shield_UI=[]#$-sao as barras laterais
hp_UI=[]#$-barra lateral
enemy_ships=[]#sao as naves inimgas e elas se blitam
shadows=[]


background=None
player=None
player_shadow=None


def update_list(list,spritelist=False,flaga=None,flagb=None):
    #se for sprites spritelist tem q ser true!!!, pra limpoar o sprite tb
    global sprites
    n=0
    will_remove=False
    to_remove=[]
    for i in list:
        if i.update_rect():
            to_remove.append(n)
            will_remove=True
        n+=1
    if will_remove:
        flaga=False
        flagb=False
        n=0
        for i in to_remove:
            list.pop(int(i-n))
            n+=1
        flaga=True
        flagb=True


class Blit:
    def __init__(self):
        self._objects=True
        self._texts=True
        self._lines=True
        self._buttons=True
        self._cursors=True
        self._projectiles=True
        self._sprites=True


class render_thread_class(threading.Thread):
    def __init__(self,sresH,sresV,windowname,crosshair_file,fps,enable_shadows):
        #from classes import menu
        self.print('Initializing render thread...')
        threading.Thread.__init__(self)
        self.print('Booting screen...')

        #startwindow
        os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d"%(100,100)  #-> USE IF WINDOWED
        flags=pygame.HWACCEL
        flags|= pygame.HWSURFACE
        self.screen=pygame.display.set_mode((sresH,sresV),flags,16)#-> WINDOW STYLE, add kvarg=FULLSCREEN/NOFRAME
        pygame.display.set_caption(windowname)

        #start cursor
        self.cursorObj=classes.Object(pygame.image.load(crosshair_file),sresH/2,sresV/2,0,0)

        #startclock
        self.Clocktime=0
        self.fpscounterclock=0
        self.desired_fps=fps
        self.fps=0
        self.fps_show=0
        if self.fps!=0:
            self.frametime=(1//self.desired_fps)*1000
            self.print('Frametime: '+str(self.frametime))
            self.print('Max FPS: '+str(fps))
        else:
            self.frametime=0
            self.print('Frametime set to 0, running max fps')


        #flags
        self.run_flag=True
        self.show_cursor=True
        self.show_player=False
        self.blit_flags=Blit()
        self.background=False
        self.enable_shadows=enable_shadows

        #debug
        debug_filepath='fonts/AndikaNewBasic-R.ttf'
        self.print(' loading file: '+debug_filepath)
        debug_text_str='debug'
        self.debug_text=classes.text(debug_text_str,debug_filepath,12,colors.WHITE,40,750,1)

    def clear_control(self):
        self.print('Clearing render list')
        global objects,texts,lines,buttons,projectiles,sprays,sprites,sprites_pos,shield_UI,hp_UI,enemy_ships

        objects=[]
        texts=[]
        lines=[]
        buttons=[]
        projectiles=[]
        sprays=[]
        sprites=[]
        sprites_pos=[]
        shield_UI=[]
        hp_UI=[]
        enemy_ships=[]

    def print(self,str):
        print(Fore.GREEN+'[RENDER] '+Fore.RESET+str)

    def run(self):
        self.print('Starting render thread...')
        self.print('Objects -> Projectiles->Texts -> Lines -> Buttons\n')

        while self.run_flag:
            if pygame.time.get_ticks()-self.Clocktime>=self.frametime:
                self.Clocktime=pygame.time.get_ticks()

                #printa o fundo
                if self.background:
                    background.blit(self.screen)
                else:
                    self.screen.fill(colors.BLACK)

                #prita objetos estaticos soltos
                for i in objects:
                    self.screen.blit(i.image,i.rect)

                if self.enable_shadows:
                    if self.show_player:
                        self.screen.blit(player_shadow.image,player_shadow.rect)

                #printa os projeteis - tem seu proprio blit()
                for i in projectiles:
                    i.blit(self.screen)

                #printa naves inimigas - elas tem q ter seu proprio blit()
                for i in enemy_ships:
                    if i.alive:
                        i.blit(self.screen)

                #printa o player - tem seu proprio blit()
                if self.show_player:
                    #é o sproy da nave
                    for i in sprays:
                        self.screen.blit(i.image,i.rect)
                    player.blit(self.screen)

                #printa sprites avulsos - possuem seu proprio blit -  classe Animation()
                for i in sprites:
                    i.blit(self.screen)
                #printa linhas
                for i in lines:
                    pygame.draw.line(self.screen,i.color,i.start,i.end,i.width)
                for i in buttons:
                    self.screen.blit(i.image,i.rect)
                #printa textos
                for i in texts:
                    self.screen.blit(i.text,i.rect)


                #prints debug text
                self.screen.blit(self.debug_text.text,self.debug_text.rect)

                #blits teh cursor
                if self.show_cursor:
                    self.screen.blit(self.cursorObj.image,self.cursorObj.rect)


                pygame.display.update()
                self.fps+=1

                #self control de fps
                if (pygame.time.get_ticks()-self.fpscounterclock)>500:
                    self.fpscounterclock=pygame.time.get_ticks()
                    self.fps_show=self.fps*2
                    self.fps=0
                    if self.desired_fps != 0:
                        if self.fps_show>self.desired_fps+10:
                            if self.frametime<25:
                                self.frametime+=1
                        elif self.fps_show<self.desired_fps-3:
                            if self.frametime>1:
                                self.frametime-=1


        self.print('Finishing render thread.')


class updater_thread_class(threading.Thread):#NAO IMPLEMENTADO -DEU RUIM
    def __init__(self,bg):
        self.print('Initalizing updater thread ...')
        threading.Thread.__init__(self)
        self.run_flag=True
        self.enable=False
        self.clock=pygame.time.get_ticks()
        self.time=10
        self.bg=bg

    def play(self):
        self.print('Resuming...')
        self.enable=True

    def pause(self):
        self.print('Pausing...')
        self.enable=False

    def print(self,str):
        print(Fore.LIGHTBLUE_EX+'[POS-UPDTR] '+Fore.RESET+str)

    def run(self):
        self.print('Starting with pause state')
        while self.run_flag:
            if self.enable:
                if pygame.time.get_ticks()-self.clock>=self.time:
                    self.clock=pygame.time.get_ticks()
                    update_list(projectiles)
                    update_list(sprites)
                    update_list(enemy_ships)
            else:
                pygame.time.wait(500)

        pygame.time.wait(100)






        self.print('Finishing updater thread.')
