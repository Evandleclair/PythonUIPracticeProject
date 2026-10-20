
from PyQt5.QtWidgets import  QMainWindow,  QWidget, QLabel

from Windows.helpers import Color, QWidgetHelper, GridUIElement, DataHelpers, DirectoryHelper
from Logic.soundPlayer import SoundPlayer, RepeatTimer
import logging, os
logger = logging.getLogger(__name__)
# this class handles the main window, and is the "Central node" that calls all other necessary classes and modules. 
class MainWindow(QMainWindow):
    
    maxIntervalSeconds = 30 ##maximum interval between sound effects in seconds
    minIntervalSeconds = 5 ##minimum interval between sound effects in seconds

    minIntervalWidget = None
    maxIntervalwidget = None

    myDirectoryHelper = None
    myPlayer = None
    loopStarted = False #whether the program is active or not. 
    loopPaused = False 

    currentSoundDirectory=""
    defaultSoundDirectory=""

    quietChance = 25
    mediumChance = 25
    loudChance = 25
    specialChance = 25 
    volume = 100.0
    sourceFolder = "test"

    volSliderLabels = []

    chanceVariables = {
        0 : quietChance,
        1 : mediumChance,
        2 : loudChance,
        3 : specialChance
        }

    chanceDirectories = {
            0 : "q",
            1 : "m",
            2 : "l",
            3 : "s"
            }
    
    chanceSliders = {}

    chanceNames = {
        0 : "Quiet noise chance",
        1 : "Medium noise chance",
        2 : "Loud noise chance",
        3 : "Special noise chance"
        }
    
    def __init__(self):
        super().__init__()
        logging.basicConfig(filename='PythonRandomSoundLog.log', encoding='utf-8', level=logging.DEBUG)
        try:
            self.button_checked = True
            self.setWindowTitle("Python UI Practice")
            self.establish_directories()
            self.myPlayer = SoundPlayer()
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

    def button_pressed(self,pText):
        print(pText)

    def start_button_pressed(self):
        if (self.myDirectoryHelper.check_sound_folder_exists()):
           self.invoke_sound()
        else:
             QWidgetHelper.generate_and_show_alert("directory no exist")

    def stop_button_pressed(self):
        self.myPlayer.stop_sound()

    def establish_directories(self):
        self.myDirectoryHelper = DirectoryHelper()
        self.myDirectoryHelper.establish_core_directories(self.chanceDirectories)


    def volume_change(self,p):
        lower =0
        upper = 100
        val = lower if p < lower else upper if p > upper else p
        self.volume = val
        print(p)
        
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
            self.minIntervalSeconds = pIntervalValue
        elif pTypeFlag =="max":
            self.maxIntervalSeconds = pIntervalValue

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

    def generate_layout_objects(self):
        objectList = []

        objectList.append(GridUIElement(
            QWidgetHelper.generate_volume_section("volume", "100"),
            0,
            0,
        ))

        objectList.append(GridUIElement(
            QWidgetHelper.generate_dial(self.volume_change),
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

        self.minIntervalWidget = QWidgetHelper.generate_interval_spin(self.minIntervalSeconds,lambda val: self.interval_update("min", val))
        self.maxIntervalwidget = QWidgetHelper.generate_interval_spin(self.maxIntervalSeconds,lambda val: self.interval_update("max", val))
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
