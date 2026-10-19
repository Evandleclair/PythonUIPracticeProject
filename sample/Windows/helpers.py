from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget, QPushButton,QDial, QSlider, QLabel, QVBoxLayout, QHBoxLayout, QSlider,QLayout,QGridLayout, QDialog 
from PyQt5.QtCore import Qt

class Color(QWidget):
    def __init__(self, pColor):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(pColor))
        self.setPalette(palette)

class QWidgetHelper():
    @staticmethod
    def GenerateButton(pText,pEvent):
        returnWidget = QPushButton(pText)
        returnWidget.clicked.connect(pEvent)
        return returnWidget

    @staticmethod
    def GenerateButton(pText,pEvent):
        returnWidget = QPushButton(pText)
        returnWidget.clicked.connect(pEvent)
        return returnWidget
    
    @staticmethod
    def GenerateSlider(pEvent,pInitialValue, pMin, pMax):
        returnWidget = QSlider(Qt.Horizontal)
        returnWidget.sliderMoved.connect(pEvent)
        returnWidget.setMinimum(pMin)
        returnWidget.setMaximum(pMax)
        returnWidget.setValue(pInitialValue)
        return returnWidget

    @staticmethod
    def GenerateLabel(pText):
        returnWidget = QLabel(pText)
        return returnWidget

    @staticmethod
    def VolumeLabel(pText):
        returnWidget = QLabel(pText)
        return returnWidget

    @staticmethod
    def GenerateVolumeSection(pLabelText, pVolumeVariable):
        widgetList = []
        widgetList.append(QWidgetHelper.GenerateLabel(pLabelText))
        widgetList.append(QWidgetHelper.VolumeLabel(pVolumeVariable))
        returnWidget = QWidgetHelper.GenerateVBoxLayout(widgetList)
        return returnWidget

    @staticmethod
    def GenerateChanceSlider(pLabelText, pInitialValue, pEvent):
        widgetList=[]
        textLabel = QWidgetHelper.GenerateLabel(pLabelText)
        volNumberLabel = QWidgetHelper.GenerateLabel("0")
        sliderWidget = QWidgetHelper.GenerateSlider(pEvent,pInitialValue,0,100)
        widgetList.append(textLabel)
        widgetList.append(sliderWidget)
        widgetList.append(volNumberLabel)
        returnWidget = QWidgetHelper.GenerateHBoxLayout(widgetList)
        return returnWidget, volNumberLabel, sliderWidget
    
    @staticmethod 
    def GenerateHBoxLayout(widgets =[],*args):
        returnWidget = QHBoxLayout()
        for widget in widgets:
            if isinstance(widget, QWidget):
                returnWidget.addWidget(widget)
            elif isinstance(widget, QLayout):
                returnWidget.addLayout(widget)      
        return returnWidget

    @staticmethod 
    def GenerateVBoxLayout(widgets =[], *args):
        returnWidget = QVBoxLayout()
        for widget in widgets:
            if isinstance(widget, QWidget):
                returnWidget.addWidget(widget)
            elif isinstance(widget, QLayout):
                returnWidget.addLayout(widget)      
        return returnWidget

    @staticmethod
    def GenerateGridLayout(pObjectList=[], *args):
        retLayout = QGridLayout()
        for obj in pObjectList:
            if isinstance(obj.element, QWidget):
                retLayout.addWidget(obj.element,obj.row,obj.col)
            elif isinstance(obj.element, QLayout):
                retLayout.addLayout(obj.element,obj.row,obj.col)      
                
        return retLayout

    @staticmethod
    def GenerateDial(pVolumeEvent):
        returnWidget = QDial()
        returnWidget.setRange(0,100)
        returnWidget.setSingleStep(1)
        returnWidget.sliderMoved.connect(pVolumeEvent)
        return returnWidget

class DataHelpers():
    def exclude_key(pDictionary, pKeysToExclude):
       if not isinstance(pKeysToExclude, (list, set, tuple, dict)):
        pKeysToExclude = {pKeysToExclude}
        return {x: pDictionary[x] for x in pDictionary if x not in pKeysToExclude}

    def combine_values(pDictionary):
        returnValue = 0
        for key, value in pDictionary.items():
            returnValue += value
        return returnValue

class GridUIElement():
    def __init__(self, pElement, pRow, pCol):
        self.element = pElement
        self.row = pRow
        self.col = pCol
