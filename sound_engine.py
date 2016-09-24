import threading,pygame,render

from colorama import Fore

mixer=None


class Mixer(threading.Thread):
    def __init__(self,bitrate,channels,buffersize):
        self.print('Initializing mixer...')
        threading.Thread.__init__(self)
        self.print('\tFreq:'+str(bitrate/1000)+'kHz - Ch'+str(channels)\
                   +' - Buffer: '+str(buffersize)+'bits\n')
        pygame.mixer.set_num_channels(channels)

        self.run_flag=True

        self.channel=[]
        for i in range(channels):
            self.channel.append(pygame.mixer.Channel(i))

    def print(self, str):
        print(Fore.YELLOW + '[MIXER] ' + Fore.RESET + str)

    def find_channel(self):
        n=0
        for i in self.channel:
            if not i.get_busy():
                return n
            n+=1
    def run(self):
        while self.run_flag:
            pass

        self.print('Finishing mixer thread')
        #pygame.mixer.quit()





