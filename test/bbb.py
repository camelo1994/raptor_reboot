import os



def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


class contador:
    def __init__(self):
        self.x=0
    def increment(self):
        self.x+=1


#o processo eh uma funcao como outra qualquer
que deve conter um loop e um controle


def a(flag):
    print('iniciando A')
    teste=ab()
    print(teste.x)
    print('incrementando')
    while flag:
        teste.increment()
        a,b=divmod(teste.x,10000)
        if b==0:
            print('x:'+str(teste.x))


    print('acabou')
    print(teste.x)