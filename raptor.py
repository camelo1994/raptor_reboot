import os,sys,random,time,threading,sqlite3,colorama
import sound_engine,classes

from def_lib import *
from render import *
from sound_engine import *

colorama.init()
print('\n\n\n\n\nImporting pygame library...')
import pygame
from pygame.locals import *

print('Importing pyganim library...')
import pyganim

#deve-se pre incializar esta merda! pq se nao fica com lag de entrada
pygame.mixer.pre_init(22050,8,2,32)


print('Initializing pygame')
pygame.init()
print('\t pygame.font')
pygame.font.init()
pygame.display.init()
pygame.mixer.init()
sound_engine.mixer=sound_engine.Mixer(22050,8,32)


#CONSTANTS
sresH=1280
sresV=800
fps=100
#CONTROL
debug=True
op=0
kappa=0
a=0
main_engine_fps=0
main_engine_fps_show=0
main_engine_fps_clock=pygame.time.get_ticks()
clock=pygame.time.get_ticks()
if 1:
    #loading crosshair file, and starting the renderer thread
    crosshair_file='images/cursor/crosshair.png'
    pygame.mouse.set_visible(False)
    print('loading file: '+crosshair_file)
    if fps!=0:
        fps=int((1/fps)*1000)
    #initializes renderer
    renderer=render.render_thread_class(sresH,sresV,'Raptor',crosshair_file,fps)
    renderer.start()

    #printing loading screen
    file='images/menu/falido e falencia.png'
    aux=pygame.image.load(file).convert_alpha()
    render.objects.append(classes.Object(aux,430,100,0,0))

    #loading everything from the user and starting the menu
    data_db_file='sql/data.db'
    items_db_file='sql/items.db'
    classes.init(data_db_file,items_db_file)

    bgm_file='bgm/raptor11.ogg'
    bgm_file2='bgm/raptor09.ogg'
    button_sound_file='sounds/menu/button-21.ogg'
    button_select_file='sounds/menu/button-22.ogg'

    menu=classes.menu(crosshair_file,bgm_file,\
                      bgm_file2,button_sound_file,button_select_file)
    renderer.clear_control()

    # aqui tem que ter uma tela se for a primeira vez

    #if menu.lastplayer == -1:
    #se nao houver jogadores criar um.. to do
    #else:
    #   print('lindao!!!!!!')



print('\n\nStarting main loop:')
menu.swap('main')
while 1:
    #rotinas independentes de troca de menu(executam uma só vez)
    if menu.changed:
        #primeiro finaliza os arquivos do menu anterior

        if menu.last_status=='main':
            print('Leaving main menu...')
            if menu.next_status=='hangar':
                sound_engine.mixer.channel[0].fadeout(500)
                sound_engine.mixer.channel[1].play(menu.bgm2,fade_ms=500)

        elif menu.last_status=='profile':
            print('Leaving profile menu...')

        elif menu.last_status=='hangar':
            print('Leaving '+menu.last_status+' menu...')
            if menu.next_status=='main':
                sound_engine.mixer.channel[1].fadeout(500)
                sound_engine.mixer.channel[0].play(menu.bgm,fade_ms=500)
            elif menu.next_status=='mission':
                sound_engine.mixer.channel[1].fadeout(500)

        elif menu.last_status=='supply':
            print('Leaving '+menu.last_status+' menu...')

        elif menu.last_status=='ship':
            print('Leaving '+menu.last_status+' menu...')

        elif menu.last_status=='mission':
            print('Leaving '+menu.last_status+' menu...')
            menu.cursor.diff_mode()
            renderer.show_cursor=True
            renderer.background=False
            if menu.next_status=='hangar':
                sound_engine.mixer.channel[1].play(menu.bgm2,fade_ms=500)
                sound_engine.mixer.channel[2].fadeout(500)
                sound_engine.mixer.channel[3].stop()

                #pygame.mouse.set_visible(True)

        #então realiza a inicialização do novo menu
        if menu.next_status=='quit':
            print('Flaging renderer')
            renderer.run_flag=False
            print('Flaging sound engine')
            sound_engine.mixer.run_flag=False

            menu.save_data()
            print('Wiping memory...')
            print('Ready to quit...')

            sys.exit()
        if menu.next_status=='main':
            print('Generating main menu...')
            renderer.clear_control()

            #objetos
            file='images/menu/background.png'#fundo
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,0,0,0,0))

            file='images/menu/menu.png'#fundo
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,700,100,0,0))

            file='images/menu/logo.png'
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,150,70,0,0))

            file='images/menu/menu_profile_square.png'#moldura
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,715,150,0,0))

            file='images/menu/menu_statistics.png'#texto das estatisticas
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,930,170,0,0))

            render.objects.append(classes.Object(menu.player.image,727,163,0,0))#foto do player atual

            #textos
            filepath='fonts/major_shift.ttf'
            #print('loading file: ' + filepath)
            render.texts.append(classes.text(menu.player.name,filepath,24,colors.WHITE,930,190,1))#nome
            render.texts.append(classes.text(menu.player.callsign,filepath,24,colors.WHITE,930,245,1))#callsign
            render.texts.append(classes.text(menu.player.shipname,filepath,24,colors.WHITE,930,300,1))#shipname
            filepath='fonts/AndikaNewBasic-BI.ttf'
            #print('loading file: '+ filepath)
            render.texts.append(classes.text('Selected profile',filepath,30,colors.RED1,800,110,1))#elementos do menu

            #carrega os botoes
            k=480
            for i in ['a','b','c','d']:
                patha='dev_menu/buttons/'+menu.next_status+'/button_'+i+'0.png'
                pathb='dev_menu/buttons/'+menu.next_status+'/button_'+i+'1.png'
                render.buttons.append(classes.MenuButton(patha,pathb,100,k))
                k+=30

            #linhas
            render.lines.append(classes.line((600,450),(600,700),colors.RED,3))

            menu.update(renderer)
        if menu.next_status=='profile':
            print('Generating profiles menu...')
            renderer.clear_control()
            #controle pra nao dar merda
            menu.lastprofile=menu.profileindex
            menu.lastplayer=menu.player

            #objetos
            file='images/menu/menu.png'#fundo
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,700,100,0,0))

            file='images/menu/menu_profile_square.png'#molduras
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,715,150,0,0))

            file='images/menu/menu_statistics.png'#texto das estatisticas
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,930,170,0,0))

            render.objects.append(classes.Object(menu.player.image,727,163,0,0))#foto do player atual

            #botoes
            #menu
            k=480
            for i in ['a','b']:
                patha='dev_menu/buttons/'+menu.next_status+'/button_'+i+'0.png'
                pathb='dev_menu/buttons/'+menu.next_status+'/button_'+i+'1.png'
                render.buttons.append(classes.MenuButton(patha,pathb,100,k))
                k+=30

                #setinhas

            i='c'
            patha='dev_menu/buttons/'+menu.next_status+'/button_'+i+'0.png'
            pathb='dev_menu/buttons/'+menu.next_status+'/button_'+i+'1.png'
            render.buttons.append(classes.MenuButton(patha,pathb,640,365,'centered'))

            i='d'
            patha='dev_menu/buttons/'+menu.next_status+'/button_'+i+'0.png'
            pathb='dev_menu/buttons/'+menu.next_status+'/button_'+i+'1.png'
            render.buttons.append(classes.MenuButton(patha,pathb,1170,365,'centered'))

            #textos
            filepath='fonts/Capture_it.ttf'
            #print('loading file: ' + filepath)
            render.texts.append(classes.text('RAPTOR',filepath,70,colors.WHITE,300,100))#título
            render.texts.append(classes.text('Call of the Birl',filepath,40,colors.RED,300,180))#subtítulo

            filepath='fonts/major_shift.ttf'
            #print('loading file: ' + filepath)
            render.texts.append(classes.text(menu.player.name,filepath,24,colors.WHITE,930,190,1))#nome
            menu.player_text_index=len(render.texts)-1
            render.texts.append(classes.text(menu.player.callsign,filepath,24,colors.WHITE,930,245,1))#callsign
            render.texts.append(classes.text(menu.player.shipname,filepath,24,colors.WHITE,930,300,1))#shipname
            filepath='fonts/AndikaNewBasic-BI.ttf'
            #print('loading file: '+ filepath)
            render.texts.append(classes.text('Selected profile',filepath,30,colors.RED1,800,110,1))#elementos do menu

            #linhas
            render.lines.append(classes.line((600,450),(600,700),colors.RED,3))

            menu.update(renderer)
        if menu.next_status=='hangar':
            print('Generating hangar menu...')
            renderer.clear_control()

            #fundo + timer da lmapada piscante
            patha='dev_menu/hangar/hangar1.png'
            pathb='dev_menu/hangar/hangar2.png'
            render.objects.append(classes.MenuButton(patha,pathb,0,0,abs))
            light_interval=500
            light_timer=pygame.time.get_ticks()

            filepath='fonts/Capture_it.ttf'
            render.texts.append(classes.text('aaaaaa',filepath,50,colors.RED,sresH/2,780))

            #botoes
            patha='dev_menu/buttons/hangar/exit.png'
            render.buttons.append(classes.MenuButton(patha,patha,(sresH/2)-300,sresV-80,abs))

            patha='dev_menu/buttons/hangar/supply.png'
            render.buttons.append(classes.MenuButton(patha,patha,740,470,abs))

            patha='dev_menu/buttons/hangar/my_ship.png'
            render.buttons.append(classes.MenuButton(patha,patha,0,sresV-675,abs))

            patha='dev_menu/buttons/hangar/mission.png'
            render.buttons.append(classes.MenuButton(patha,patha,195,460,abs))

            patha='dev_menu/buttons/hangar/save.png'
            render.buttons.append(classes.MenuButton(patha,patha,680,140,abs))
        if menu.next_status=='supply':
            print('Generating supply menu...')
            renderer.clear_control()

            #objetos
            file='dev_menu/supply_room/supply room.png'#background
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,0,0,0,0))
        if menu.next_status=='ship':
            print('Generating ship menu...')
            renderer.clear_control()
            filepath='fonts/Capture_it.ttf'
            render.texts.append(classes.text('SHIP MENU',filepath,70,colors.WHITE,sresH/2,sresV/2))
        if menu.next_status=='mission':
            print('Generating mission menu...')
            renderer.clear_control()
            #entra no modo diferencial
            menu.cursor.diff_mode()
            #esconde o cursor
            renderer.show_cursor=False

            #define canal 2 - bgm
            wave_bgm_file='bgm/raptor02.ogg'
            wave_sound=pygame.mixer.Sound(wave_bgm_file)
            wave_sound.set_volume(0.3)
            sound_engine.mixer.channel[2].play(wave_sound,loops=-1)
            #define canal 3 - barulho do vento
            jet_sound_file='sounds/jet_interior.ogg'
            jet_sound=pygame.mixer.Sound(jet_sound_file)
            jet_sound.set_volume(0.5)
            sound_engine.mixer.channel[3].play(jet_sound,loops=-1)

            desired_pos=[]
            desired_pos.append(sresH/2)
            desired_pos.append(100)

            #fundo
            file='images/background.png'#fundo
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.background=classes.Object(aux,0,0,0,0)
            renderer.background=True

            render.player=menu.player.ship
            renderer.show_player=True

            render.objects.append(menu.player.ship.weapon[0])

            #linhas
            render.lines.append(classes.line((1250,0),(1250,800),colors.WHITE,1))
            render.lines.append(classes.line((30,0),(30,800),colors.WHITE,1))

             #avisa pra nave q vai entrar em batalha
            menu.player.ship.enter_battle()

            kappa=pygame.time.get_ticks()


        menu.done_loading()#informa ao menu,que Load/Unloads foram realizados


    #rotinas cíclicas    
    else:

        while menu.status=='main':
            for event in pygame.event.get():
                if event.type==QUIT:
                    menu.swap('quit')
                if event.type==KEYDOWN:
                    if event.key==K_p:
                        menu.cursor.diff_mode()
                    elif event.key==K_F2:
                        menu.swap('profile')

            keys=pygame.key.get_pressed()
            if keys[K_q] and keys[K_LALT]:
                menu.swap('quit')

            #atualiza o menu
            menu.update(renderer)

            #debug_text
            renderer.debug_text.update_text('Mouse: X,Y('+str(menu.cursor.posX)\
                                            +','+str(menu.cursor.posY)+')'\
                                            +' dX,dY('+str(menu.cursor.posdX)\
                                            +','+str(menu.cursor.posdY)+')'\
                                            +'m1,m2,m3'+str(menu.cursor.buttons),colors.BLUE1)

        while menu.status=='profile':
            for event in pygame.event.get():
                if event.type==QUIT:
                    menu.swap('quit')
                if event.type==KEYDOWN:
                    if event.key==K_p:
                        menu.cursor.diff_mode()
                    elif event.key==K_F1:
                        menu.swap('main')
                    elif event.key==K_r:
                        menu.swap_player('+')
                    elif event.key==K_e:
                        menu.swap_player('-')
                    elif event.key==K_w:
                        menu.swap_player('*')
                    elif event.key==K_q:
                        menu.swap_player('**')

            keys=pygame.key.get_pressed()
            if keys[K_q]&keys[K_LALT]:
                menu.swap('quit')

            #atualiza o menu
            menu.update(renderer)

            #debugs
            renderer.debug_text.update_text('Mouse: X,Y('+str(menu.cursor.posX)+','+str(menu.cursor.posY)+')'\
                                            +' dX,dY('+str(menu.cursor.posdX)+','+str(menu.cursor.posdY)+')'\
                                            +'m1,m2,m3'+str(menu.cursor.buttons),colors.BLUE1)

        while menu.status=='hangar':
            for event in pygame.event.get():
                if event.type==QUIT:
                    menu.swap('quit')
                if event.type==KEYDOWN:
                    if event.key==K_p:
                        menu.cursor.diff_mode()
                    elif event.key==K_F1:
                        menu.swap('main')

            keys=pygame.key.get_pressed()
            if keys[K_q]&keys[K_LALT]:
                menu.swap('quit')

            #lampada flickerando no hangar
            if (pygame.time.get_ticks()-light_timer)>=light_interval:
                light_timer=pygame.time.get_ticks()
                light_interval=random.randrange(150)+50
                render.objects[0].swap_image()


                #atualiza o menu
            menu.update(renderer)

            if menu.op!=None:
                if menu.op==0:
                    render.texts[0].update_text('RETURN TO MAIN MENU')
                elif menu.op==1:
                    render.texts[0].update_text('SUPPLY ROOM')
                elif menu.op==2:
                    render.texts[0].update_text('MY SHIP')
                elif menu.op==3:
                    render.texts[0].update_text('MISSION MENU')
                elif menu.op==4:
                    render.texts[0].update_text('SAVE PROFILE')
            else:
                render.texts[0].update_text('')

            #debugs
            renderer.debug_text.update_text('Mouse: X,Y('+str(menu.cursor.posX)+','+str(menu.cursor.posY)+')'\
                                            +' dX,dY('+str(menu.cursor.posdX)+','+str(menu.cursor.posdY)+')'\
                                            +'m1,m2,m3'+str(menu.cursor.buttons)\
                                            +'op('+str(menu.op)+')',colors.BLACK)

        while menu.status=='supply':
            for event in pygame.event.get():
                if event.type==QUIT:
                    menu.swap('quit')
                if event.type==KEYDOWN:
                    if event.key==K_p:
                        menu.cursor.diff_mode()
                    elif event.key==K_F1:
                        menu.swap('hangar')

            #atualiza o menu
            menu.update(renderer)

            #debug_text
            renderer.debug_text.update_text('Mouse: X,Y('+str(menu.cursor.posX)\
                                            +','+str(menu.cursor.posY)+')'\
                                            +' dX,dY('+str(menu.cursor.posdX)\
                                            +','+str(menu.cursor.posdY)+')'\
                                            +'m1,m2,m3'+str(menu.cursor.buttons),colors.BLACK)

        while menu.status=='ship':
            for event in pygame.event.get():
                if event.type==QUIT:
                    menu.swap('quit')
                if event.type==KEYDOWN:
                    if event.key==K_p:
                        menu.cursor.diff_mode()
                    elif event.key==K_F1:
                        menu.swap('hangar')

        while menu.status=='mission':
            for event in pygame.event.get():
                if event.type==QUIT:
                    menu.swap('quit')
                if event.type==KEYDOWN:
                    if event.key==K_p:
                        menu.cursor.diff_mode()
                    if event.key==K_F1:
                        menu.swap('hangar')
                    if event.key==K_F3:
                        classes.spawn_sprite(100,100,'small_explosion')
                    if event.key==K_F4:
                        classes.spawn_sprite(100,100,'small_explosion',5,5)
                    if event.key==K_F2:
                        render.player.take_damage(1)
                    if event.key==K_F5:
                        classes.spawn(0,random.randrange(200,1000))
                    if event.key==K_F12:
                        render.player.shield.current_hp+=10
                    if event.key==K_F11:
                        render.player.energy_module.current_hp+=10
                    if event.key==K_F8:
                        render.enemy_ships[1].fire()
                    if event.key==K_F9:
                        render.enemy_ships[2].fire()
            #atualiza o menu
            menu.update(renderer)

            #move a nave
            #verifica posição desejada para ver se cabe na tela
            if desired_pos[0]+menu.cursor.posdX<sresH-34 and desired_pos[0]+menu.cursor.posdX>34:
                desired_pos[0]+=menu.cursor.posdX
            if desired_pos[1]+menu.cursor.posdY>40 and desired_pos[1]+menu.cursor.posdY<sresV-40:
                desired_pos[1]+=menu.cursor.posdY
            #move a nave    
            render.player.move(desired_pos)

            #atualiza tudo
            if pygame.time.get_ticks()-clock>=16:
                clock=pygame.time.get_ticks()

                #posicoes
                render.update_list(render.projectiles)
                render.update_list(render.sprites)
                render.update_list(render.enemy_ships)

                #verica colisoes com projeteis
                for i in render.projectiles:
                    #se o projetil ainda for valido
                    if i.valid:
                    #se o tiro nao for amigavel eu tomo dano
                        if not i.friendly:
                            if render.player.colliderect(i.rect):
                                render.player.take_damage(i.damage)
                                i.valid=False
                        #se algum inimigo tomou dano:
                        else:
                            for a in render.enemy_ships:
                                if a.rect.colliderect(i.rect):
                                    a.take_damage(i.damage)
                                    i.valid=False


            #atira se tiver com wm1 apertado
            if menu.cursor.buttons[0]:
                render.player.fire()


            for i in render.enemy_ships:
                i.fire()

            main_engine_fps+=1

            if pygame.time.get_ticks()-main_engine_fps_clock >=1000:
                main_engine_fps_clock=pygame.time.get_ticks()
                main_engine_fps_show=main_engine_fps
                main_engine_fps=0


                #debug_text
            renderer.debug_text.update_text('Mouse: X,Y('+str(menu.cursor.posX)\
                                            +'  '+str(menu.cursor.posY)+')'\
                                            +'  dX,dY('+str(menu.cursor.posdX)\
                                            +'  '+str(menu.cursor.posdY)+')'\
                                            +'  m1,m2,m3'+str(menu.cursor.buttons)\
                                            +'  desiredpos('+str(desired_pos)+')'\
                                            +'   nProj:'+str(len(render.projectiles))\
                                            +'   nAnimPos:'+str(len(render.sprites_pos))\
                                            +'   nAnim:'+str(len(render.sprites))\
                                            +'   nEnemy:'+str(len(render.enemy_ships))\
                                            +'   HP:'+str(menu.player.ship.energy_module.current_hp)\
                                            +'   shield:'+str(menu.player.ship.shield.current_hp)\
                                            +'   time:'+str(pygame.time.get_ticks())\
                                            +'   MainFPS:'+str(main_engine_fps_show)\
                                            +'   RenderFPS:'+str(renderer.fps_show),colors.WHITE)