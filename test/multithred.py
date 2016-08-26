from multiprocessing import Process, Manager, Pipe
import threading
import time,os

def f(l,pipe):
    print('loop de soma PID:'+str(os.getpid()))
    print('loop de soma PID parental(em teoria o programa principal):'+str(os.getppid()))
    flag=True
    while flag:
        l[1]+=1
        if pipe.poll():#verifica se tem informação nova no cano
            flag=pipe.recv()#recenbe dados do cano - volta pra linha 35
    print('end')

class thread(threading.Thread):
    def __init__(self,c0):
        threading.Thread.__init__(self)
        self.flag=True
        self.l=Manager().list()
        self.l.append(0)
        self.l.append(1)
        self.l.append('ss')
        self.c0=c0#salva o final do cano

    def run(self):
        self.p=Process(target=f,args=(self.l,self.c0,))#inicia um processo em loop com o cano -vai pra linha 5
        self.p.start()
        self.p.join()

if __name__ == '__main__':
    p0,c0=Pipe(True)#cria um cano de comunicação inter-processos
    p0.send(True)#envia True para o cano

    t=thread(c0)#inicia a thread -  vai pra linha 24
    t.start()

    #enquanto td akilo tava acontecendo, o progr principal le de 1 em 1 segundo
    #qnd o valor estorar 100000 ele manda falso pro cano
    print('prog principal PID:'+str(os.getpid()))
    print('prog principal PID parental(em teoria o proprio explorer.exe):'+str(os.getppid()))
    a=True
    while a:
        print(t.l)
        time.sleep(1)
        if t.l[1]>100000:
            p0.send(False)
            a=False
        elif t.l[1]>=50000:#depois de 50000 fica adicinonando uim termo kappa
            t.l.append('kappa')
        #else:
         #   p0.send(True)
    print(t.l)





