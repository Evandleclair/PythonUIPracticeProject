from playsound3 import playsound
import os, logging, random
from threading import Event, Thread
logger = logging.getLogger(__name__)
logging.basicConfig(filename='PythonRandomSoundLog.log', encoding='utf-8', level=logging.DEBUG)
class RepeatTimer():
    intervalMin = 0
    intervalMax = 0
    def __init__(self):
        logger.debug(f"playsound active")

    def run_after_interval(self, pFunc, *args):
        stopped = Event()
        print("starting thread")
        def loop():
            while not stopped.wait(random.randrange(int(self.intervalMin),int(self.intervalMax),1)):
                pFunc(*args)
                print(f"ran function{pFunc} with arguments {args}")
        th = Thread(target=loop)
        th.daemon = True
        th.start()
        return stopped.set
        
    def set_interval(self,pIntervalVal,pIntervalKey):
        if pIntervalKey=="min":
            self.intervalMin = pIntervalVal
        elif pIntervalKey=="max":
            self.intervalMax = pIntervalVal
        

class SoundPlayer():
    sound = None
    def __init__(self):
        logger.debug(f"playsound active")

    def play_sound_at_path(self, pSoundPath):
        if self.sound is None:
            self.sound = playsound(pSoundPath, block=False)
        elif not self.sound.is_alive():
            self.sound = playsound(pSoundPath, block=False)
        else:
            logger.debug("sound still playing. skipping execution")

    def stop_sound(self):
        if not self.sound is None:
            self.sound.stop()
   
