import threading
import time
from audioplayer import AudioPlayer
import os, logging, random
from threading import Event, Thread

logger = logging.getLogger(__name__)
logging.basicConfig(filename='PythonRandomSoundLog.log', encoding='utf-8', level=logging.DEBUG)

class RepeatTimer():
    intervalMin = 0
    intervalMax = 0
    def __init__(self):
        logger.debug(f"silence breaker active")

    def run_after_interval(self, pFunc, *args):
        stopped = Event()
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


    def __init__(self):
        logger.debug(f"playsound active")
        self.is_playing = False
        self.current_volume = 100
        self._stop_event = threading.Event()
        self._lock = threading.Lock()


    def _normalize_volume(self, p_volume):
        if isinstance(p_volume, float) and p_volume <= 1.0:
            val = int(round(p_volume * 100))
        else:
            val = int(round(p_volume))
        return max(0, min(100,val))

    def play_sound_at_path(self, pSoundPath, pVolume=None):
        with self._lock:
            if self.is_playing:
                return #end early
            self.is_playing = True
            self._stop_event.clear() #clear the stop flag

            if pVolume is not None:
                self.current_volume = self._normalize_volume(pVolume)

        threading.Thread(
            target=self._load_and_push, 
            args=(str(pSoundPath),), 
            daemon=True
        ).start()

    def _load_and_push(self, sound_path_str):
        player = None
        try:
            player = AudioPlayer(sound_path_str)
            player.play(block = False)
            last_vol =-1
            time.sleep(0.05) #buffer
            while not self._stop_event.is_set():
                if self.current_volume != last_vol:
                    player.volume = self.current_volume
                    last_vol = self.current_volume
                if self._has_finished(player):
                    break;
                time.sleep(0.05) #buffer
        except Exception as e:
            logger.error(f"Failed to load or play sound from {sound_path_str}: {e}")
        finally:
            if player is not None:
                try:
                    player.stop()
                    player.close()
                except Exception:
                    pass
            with self._lock:
                self.is_playing = False

    def _sound_is_playing(self):
        return self.is_playing


    def _has_finished(self,player):
        alias = getattr(player, "_alias", None)
        if alias:
            try:
                import ctypes
                buf = ctypes.create_unicode_buffer(64)
                ctypes.windll.winmm.mciSendStringW(f"status {alias} mode", buf, 64, 0)
                return buf.value.lower() != "playing"
            except Exception:
                pass
        if hasattr(player,"_process") and player._process is not None:
            return player._process.poll() is not None
        if hasattr(player,"_player") and hasattr(player._player, "isPlaying"):
            return player._player.isPlaying()

        return False


    def set_volume(self, pVolume):
        self.current_volume = self._normalize_volume(pVolume)

    def stop_sound(self):
        self._stop_event.set()