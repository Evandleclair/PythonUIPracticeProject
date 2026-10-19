
from PyQt5.QtWidgets import QGridLayout, QMainWindow, QPushButton, QWidget, QLabel, QLayout

from Windows.helpers import Color, QWidgetHelper, GridUIElement, DataHelpers
import logging, datetime

# this class handles the main window, and is the "Central node" that calls all other necessary classes and modules. 
class MainWindow(QMainWindow):
    
    maxInterval = 30 ##maximum interval between sound effects
    loopStarted = False #whether the program is active or not. 
    loopPaused = False 
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
    
    chanceSliders = {}

    chanceNames = {
        0 : "Quiet noise chance",
        1 : "Medium noise chance",
        2 : "Loud noise chance",
        3 : "Special noise chance"
        }
    
    def __init__(self):
        super().__init__()
        logger = self.createLogger()
        try:
            self.button_checked = True
            self.setWindowTitle("Python UI Practice")

            objList = self.generateLayoutObjects()
            layout = QWidgetHelper.GenerateGridLayout(objList)
            layout.setContentsMargins(0,0,0,0)

            container = QWidget()
            container.setLayout(layout)

            # Set the central widget of the Window.
            self.setCentralWidget(container)
        except Exception as e:
            logger.error(f"Exception Occured: {e}")

    def button_pressed(self,pText):
        print(pText)

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

            while (totalChance>100):
                otherSliders = DataHelpers.exclude_key(self.chanceVariables,sliderId)

                if not otherSliders:
                    break

                max_other_key = max(otherSliders, key=otherSliders.get)
                self.chanceVariables[max_other_key] -= 1
             
                totalChance = DataHelpers.combine_values(self.chanceVariables)
                self.chanceSliders[max_other_key].setValue(self.chanceVariables[max_other_key]) #update slider with its new value
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

    def createLogger(self):
        returnLogger = logging.getLogger(__name__)
        logging.basicConfig(filename='PythonRandomSoundLog.log', encoding='utf-8', level=logging.DEBUG)
        now = datetime.datetime.now()
        returnLogger.debug('Logger spun up at {now}')
        return returnLogger

    def defineLabel(self,pText):
        self.label = QLabel(pText)

    def do_nothing(self):
        print("not implemented")

    def generateLayoutObjects(self):
        objectList = []

        objectList.append(GridUIElement(
            QWidgetHelper.GenerateVolumeSection("volume", "100"),
            0,
            0,
        ))

        objectList.append(GridUIElement(
            QWidgetHelper.GenerateDial(self.volume_change),
            0,
            1,
        ))
        

        objectList.append(GridUIElement(
            QWidgetHelper.GenerateButton("start", lambda: self.button_pressed("start")),
            1,
            0,
        ))

        objectList.append(GridUIElement(
            QWidgetHelper.GenerateButton("stop", lambda:  self.button_pressed("stop")),
            1,
            1,
        ))

        objectList.append(GridUIElement(
            QWidgetHelper.GenerateButton("reset", lambda:  self.button_pressed("reset")),
            1,
            2,
        ))

        objectList.append(GridUIElement(
            QWidgetHelper.GenerateVBoxLayout(self.createSliderStack()),
            0,
            3,

        ))

        return objectList

    
    def createSliderStack(self):
        sliderStack = []
       #sliderStack.append(QWidgetHelper.GenerateChanceSlider("",lambda: self.do_nothing()))

        for i in range(0, len(self.chanceVariables), 1):
            chanceSlider, volumeLabel, sliderWidget = QWidgetHelper.GenerateChanceSlider(
                self.chanceNames[i],
                self.chanceVariables[i], 
                lambda value, idx=i: self.chance_change(idx, value)
            )
            self.volSliderLabels.append(volumeLabel)
            sliderStack.append(chanceSlider)
            self.chanceSliders[i] = sliderWidget #store this so it can be referenced by other functions

        return sliderStack
