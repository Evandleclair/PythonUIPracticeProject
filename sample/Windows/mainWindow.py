
from PyQt5.QtWidgets import QGridLayout, QMainWindow, QPushButton, QWidget, QLabel, QLayout

from Windows.helpers import Color, QWidgetHelper, GridUIElement
import logging, datetime
# this class handles the main window, and is the "Central node" that calls all other necessary classes and modules. 
class MainWindow(QMainWindow):
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
        except:
            logger.error('and error occured. Logging will be more verbose in future versions')

    def button_pressed(self,pText):
        print(pText)

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
            QWidgetHelper.GenerateDial(lambda: self.do_nothing),
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
       sliderStack.append(QWidgetHelper.GenerateChanceSlider("Loud chance",lambda: self.do_nothing()))
       sliderStack.append(QWidgetHelper.GenerateChanceSlider("Normal volume chance",lambda: self.do_nothing()))
       sliderStack.append(QWidgetHelper.GenerateChanceSlider("Quiet volume chance",lambda: self.do_nothing()))
       sliderStack.append(QWidgetHelper.GenerateChanceSlider("Special noise chance",lambda: self.do_nothing()))
       return sliderStack
