from playsound3 import playsound
import os, logging
from threading import Timer
logger = logging.getLogger(__name__)
logging.basicConfig(filename='PythonRandomSoundLog.log', encoding='utf-8', level=logging.DEBUG)
class RepeatTimer(Timer):
        
    def run(self,event):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

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
        self.sound.stop()
   
