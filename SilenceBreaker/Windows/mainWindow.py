
from PyQt5.QtWidgets import  QMainWindow,  QWidget, QLabel

from Windows.helpers import Color, QWidgetHelper, GridUIElement, DataHelpers, DirectoryHelper
from Logic.soundPlayer import SoundPlayer, RepeatTimer
import logging, os
logger = logging.getLogger(__name__)
# this class handles the main window, and is the "Central node" that calls all other necessary classes and modules. 
class MainWindow(QMainWindow):
    
    maxIntervalSeconds = None
    minIntervalSeconds = 5 ##minimum interval between sound effects in seconds

    minIntervalWidget = None
    maxIntervalwidget = None

    myDirectoryHelper = None
    myPlayer = None
    myTimer = None
    myIntervalTimer = None
    myConfig = {}
 
    stopEvent = None

    loopStarted = False #whether the program is active or not. 
    loopPaused = False 

    triedLoadConfig = False #error flag on config load. 
    resetConfigEvent = None

    currentSoundDirectory=""
    defaultSoundDirectory=""
    defaultLogFileName=""

    quietChance = 25
    mediumChance = 25
    loudChance = 25
    specialChance = 25 
    volume = 0.0
    volumeLabel = None
    sourceFolder = "test"

    volSliderLabels = []

    chanceVariables = {
        0 : quietChance,
        1 : mediumChance,
        2 : loudChance,
        3 : specialChance
        }
    
    elementsToLock = [] #UI elements that should be marked "read only" when the loop is ongoing
    chanceDirectories = {}
    
    chanceSliders = {}

    chanceNames = {}
    
    def __init__(self, pConfig, pDirectoryHelper, pResetEvent):
        super().__init__()
       
        try:
            self.load_config(pConfig)
            logging.basicConfig(filename=self.defaultLogFileName, encoding='utf-8', level=logging.DEBUG)
        except Exception as e:
            print(f'Error {e} occured on initial launch of program')
        try:
            #now that the logger is loaded, we can use that for our exceptions instead. 
            self.setWindowTitle("Python UI Practice")
            self.establish_directories(pDirectoryHelper)
            self.myPlayer = SoundPlayer()
            self.myTimer = RepeatTimer()
            self.resetConfigEvent=pResetEvent
            self.define_unique_elements() #generate widget items that need to be referred to directly by this controller.
            objList = self.generate_layout_objects()
            layout = QWidgetHelper.GenerateGridLayout(objList)
            layout.setContentsMargins(0,0,0,0)

            container = QWidget()
            container.setLayout(layout)

            # Set the central widget of the Window.
            self.setCentralWidget(container)
        except Exception as e:
            QWidgetHelper.generate_and_show_alert(e)
            logger.error(f"Exception Occured: {e}")

    def load_config(self,pConfig):
        try:
            chance_dirs_raw = pConfig.get("chanceDirectories", [])
            self.chanceDirectories = {i: val for i, val in enumerate(chance_dirs_raw)}
            
            chance_names_raw = pConfig.get("chanceNames", [])
            self.chanceNames = {i: val for i, val in enumerate(chance_names_raw)}
            
            # Use .get() with safe fallbacks so variables will not end up as a None
            default_settings = pConfig.get("defaultSettings", {})
            self.volume = default_settings.get("defaultVolume", 50)
            self.minIntervalSeconds = default_settings.get("defaultMinInterval", 5)
            self.maxIntervalSeconds = default_settings.get("defaultMaxInterval", 15)
            self.defaultLogFileName = default_settings.get("defaultLogFileName", "SilenceBreaker.log")
            
            self.myConfig = pConfig  # Store config reference for later export
        except Exception as e:
            if self.triedLoadConfig == False:
                 QWidgetHelper.generate_and_show_alert(f"Config load error: {e}")
                 self.resetConfigEvent()
                 self.triedLoadConfig=True
            else:
                strMessage = f"Failed to load valid config even after config reset. Please contact the developer. The following exception was raised: {e}"
                QWidgetHelper.generate_and_show_alert(strMessage)
                self.close() #if we cannot load config, do not continue

    def export_config(self):
        self.myConfig["chanceDirectories"] = self.chanceDirectories
        self.myConfig["chanceNames"] = self.chanceNames

        if "defaultSettings" not in self.myConfig:
            self.myConfig["defaultSettings"] = {}

        self.myConfig["defaultSettings"]["defaultVolume"] = self.volume
        self.myConfig["defaultSettings"]["defaultMinInterval"] = self.minIntervalSeconds
        self.myConfig["defaultSettings"]["defaultMaxInterval"] = self.maxIntervalSeconds
        self.myConfig["defaultSettings"]["defaultLogFileName"] = self.defaultLogFileName
        return self.myConfig
    
    def button_pressed(self,pText):
        print(pText)

    def start_button_pressed(self):
        if (self.myDirectoryHelper.check_sound_folder_exists()):
           self.start_timer()
        else:
             QWidgetHelper.generate_and_show_alert("directory no exist")

    def stop_button_pressed(self):
        self.myPlayer.stop_sound()
        self.stopEvent()

    def establish_directories(self, pDirectoryHelper):
        self.myDirectoryHelper = pDirectoryHelper
        self.myDirectoryHelper.establish_core_sound_directories(self.chanceDirectories)
        

    def start_timer(self):
        self.myTimer.set_interval(self.minIntervalSeconds,"min")
        self.myTimer.set_interval(self.maxIntervalSeconds,"max")
        self.stopEvent = self.myTimer.run_after_interval(lambda: self.invoke_sound())

    def volume_change(self,p):
        lower =0
        upper = 100
        val = lower if p < lower else upper if p > upper else p
        self.volume = val
        self.volumeLabel.setText(str(val))

    def get_config_values(self):
        return 
    
    def chance_change(self,sliderId,p):
        try:
            self.chanceVariables[sliderId]=p #update changed slider to new value
            totalChance = DataHelpers.combine_values(self.chanceVariables)
            otherSliders = DataHelpers.exclude_key(self.chanceVariables,sliderId)

            if not otherSliders:
                return
            
            while (totalChance>100):
                max_other_key = max(otherSliders, key=otherSliders.get)
                self.chanceVariables[max_other_key] -= 1
                totalChance = DataHelpers.combine_values(self.chanceVariables)
                self.chanceSliders[max_other_key].setValue(self.chanceVariables[max_other_key]) #update slider with its new value
         
            while (totalChance<100):
                min_other_key = min(otherSliders, key=otherSliders.get)
                self.chanceVariables[min_other_key] += 1
                totalChance = DataHelpers.combine_values(self.chanceVariables)
                self.chanceSliders[min_other_key].setValue(self.chanceVariables[min_other_key]) #update slider with its new value

            self.update_volume_labels #once all calculation is done, update the labels.
        except Exception as e:
                self.logger.error(f"Exception Occured: {e}")
          
    def update_volume_labels(self):
        for id, label in self.volSliderLabels.items():
            num = self.chanceVariables[id]
            label.setText(num)
            print(num)


    def the_button_was_released(self):
        self.button_checked = self.button.isChecked();
        print(self.button_checked)

    def interval_update(self, pTypeFlag, pIntervalValue):
        if pTypeFlag == "min":
            if (pIntervalValue>=self.maxIntervalSeconds-1):
                pIntervalValue = self.maxIntervalSeconds-1
                self.minIntervalWidget.setValue(pIntervalValue)
            self.minIntervalSeconds = pIntervalValue
        elif pTypeFlag =="max":
            if (pIntervalValue<=self.minIntervalSeconds+1):
                pIntervalValue = self.minIntervalSeconds+1
                self.maxIntervalwidget.setValue(pIntervalValue)
            self.maxIntervalSeconds = pIntervalValue
        self.myTimer.set_interval(pIntervalValue,pTypeFlag)

    def invoke_sound(self):
        activeSubfolder = self.chanceDirectories[DataHelpers.pick_random(self.chanceVariables)]
        print(activeSubfolder)
        randomSoundFile = self.myDirectoryHelper.get_random_file(activeSubfolder)
        print(f"playing {randomSoundFile}")
        self.myPlayer.play_sound_at_path(randomSoundFile)


    def defineLabel(self,pText):
        self.label = QLabel(pText)

    def do_nothing(self):
        print("not implemented")

    def define_unique_elements(self):
        self.minIntervalWidget = QWidgetHelper.generate_interval_spin(self.minIntervalSeconds,lambda val: self.interval_update("min", val))
        self.maxIntervalwidget = QWidgetHelper.generate_interval_spin(self.maxIntervalSeconds,lambda val: self.interval_update("max", val))
        self.volumeLabel =  QWidgetHelper.GenerateLabel(str(self.volume))

    def generate_layout_objects(self):
        objectList = []
        objectList.append(GridUIElement(
            QWidgetHelper.generate_volume_section(self.volumeLabel, str(self.volume)),
            0,
            0,
        ))

        objectList.append(GridUIElement(
            QWidgetHelper.generate_dial(self.volume_change, self.volume),
            0,
            1,
        ))
        

        objectList.append(GridUIElement(
            QWidgetHelper.generate_button("start", lambda: self.start_button_pressed()),
            1,
            0,
        ))

        objectList.append(GridUIElement(
            QWidgetHelper.generate_button("stop", lambda:  self.stop_button_pressed()),
            1,
            1,
        ))

        objectList.append(GridUIElement(
            QWidgetHelper.generate_button("reset", lambda:  self.button_pressed("reset")),
            1,
            2,
        ))

        objectList.append(GridUIElement(
            QWidgetHelper.generate_vbox_layout(self.create_slider_stack()),
            0,
            3,

        ))

        objectList.append(GridUIElement(
            QWidgetHelper.generate_interval_section(self.minIntervalWidget,self.maxIntervalwidget),
            1,
            3,
        ))

        return objectList

    
    def create_slider_stack(self):
        sliderStack = []

        for i in range(0, len(self.chanceVariables), 1):
            chanceSlider, volumeLabel, sliderWidget = QWidgetHelper.generate_chance_slider(
                self.chanceNames[i],
                self.chanceVariables[i], 
                lambda value, idx=i: self.chance_change(idx, value)
            )
            self.volSliderLabels.append(volumeLabel)
            sliderStack.append(chanceSlider)
            self.chanceSliders[i] = sliderWidget #store this so it can be referenced by other functions

        return sliderStack
