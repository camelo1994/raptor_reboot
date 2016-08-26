import render
from render import *
'''
nas definicoes, apos o return #op significa operação
#action significa ação no menu

1o char

$->ação interna do menu
%-> ação externa

'''





def check_selection(status,x,y):

    for i in range(len(render.buttons)):
        if render.buttons[i].rect.collidepoint(x,y):
            return i      
     
def check_choice(status,op):

    if status=='main':
        if op==0:
            return('$$hangar')
        elif op==1:
            return('$$profile')
        elif op==2:
            return('$$'+status)
        elif op==3:
            return('$$quit')
  
    if status=='profile':
        if op==0:
            return('$%*')#*-> select player
        elif op==1:
            return('$%**')#*cancel     
        elif op==2:
            return('$%-')
        elif op==3:
            return('$%+')

    if status=='hangar':
        if op==0:
            return('$$main')
        elif op==1:
            return('$$supply')     
        elif op==2:
            return('$$ship')
        elif op==3:
            return('$$mission')
        elif op==4:
            return('$%save')

            