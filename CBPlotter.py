import time
import queue

import os
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PlotterGUIFuncs import *
from CBPlotFunc import *

app = QApplication(sys.argv)
window = QDialog()


def main():
    global ui, objectPressed
    objectPressed=None
    # run GUI
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()


    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    ui.NodeMove_PB.clicked.connect(movePBAction)
    ui.NodeDel_PB.clicked.connect(deletePBAction)
    ui.actionRandomPlot.triggered.connect(startNewRandomPlot)
    ui.actionXmlPlot.triggered.connect(startNewRandomPlot)
    ui.Simulation_PB.clicked.connect(startCBNodeThreads)
    ui.StopSimulation_PB.clicked.connect(stopCBNodeThreads)
    ui.Freq_HS.valueChanged.connect(freqHSAction)
    ui.BW_HS.valueChanged.connect(BWHSAction)
    ui.NodeUpdate_PB.clicked.connect(updateNodePBAction)


    sys.exit(app.exec_())

def freqHSAction():
    try:
        startFreq=1000
        endFreq=3000
        tickCount=int(ui.Freq_HS.maximum())
        currentTick= int(ui.Freq_HS.value())
        textToSet=str(int((endFreq-startFreq)*(currentTick/tickCount)+startFreq))
        ui.NodeFreq_L.setText(textToSet)

    except:

        errorType, value, tb = sys.exc_info()
        print('(freqHSAction)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')

def BWHSAction():
    try:
        BWsList=[1.4,3,5,10,15,20]


        currentTick= int(ui.BW_HS.value())
        textToSet= str(BWsList[currentTick])
        ui.NodeBW_L.setText(textToSet)

    except:

        errorType, value, tb = sys.exc_info()
        print('(BWHSAction)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')

def deletePBAction():
    if objectPressed is not None:
        objectPressed.deleteCir(arrowsList)

def movePBAction():
    try:
        global mainCurrentMouse
        print('start movePBAction')
        if objectPressed is not None:
            ui.NodeMove_PB.setStyleSheet("background-color: green")
            mainCurrentMouse = plotWinObj.getMouse()
            objectPressed.moveCir(mainCurrentMouse, plotWinObj, arrowsList)
            printNodeParameters()
            objectPressed.selectNode()
        movePBClear()
    except:

        errorType, value, tb = sys.exc_info()
        print('(movePBAction)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')

def updateNodePBAction():
    try:
        global objectPressed
        if objectPressed is not None:

            objectPressed.listToDisplay[10] = objectPressed.txPower = ui.NodeTXP_LE.text()
            objectPressed.listToDisplay[8] = objectPressed.freq = ui.NodeFreq_L.text()
            objectPressed.listToDisplay[9] = objectPressed.BW = ui.NodeBW_L.text()
            objectPressed.listToDisplay[1] = objectPressed.CID = ui.NodeCID_LE.text()

            objectPressed.updateListToDisplay()
            printNodeParameters()

    except:

        errorType, value, tb = sys.exc_info()
        print('(updateNodePBAction)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')

def movePBClear():
    print('start movePBClear')
    global mainCurrentMouse
    ui.NodeMove_PB.setStyleSheet("background-color: light gray")


def printNodeParameters():
    objectPressed.updateListToDisplay()
    objectPressed.listToDisplay[13]=str(int(objectPressed.cirCenter.getX())-borderSpaceX)+','+str(int(objectPressed.cirCenter.getY())-borderSpaceY)
    text = "Node Name: {0}\nNode CID: {1}\nTree No.: {2}\nTree Rate: {3}\nRN CID: {4}\nNext Hop CID: {5}\nState: {6}\nType: {7}\nFrequency: {8} [MHz]\nBandwidth: {9} [MHz]\nTx Power: {10}\nC. Nodes: {11}\nC. CPEs: {12}\nCoordinates: {13}\n"
    #ui.Node_TE.setText(ui.Node_TE.toPlainText() + objectPressed.textToDisplay)
    ui.Node_TE.setText(text.format(*objectPressed.listToDisplay))
    ui.NodeFreq_L.setText(objectPressed.listToDisplay[8])
    ui.NodeBW_L.setText(objectPressed.listToDisplay[9])
    ui.NodeTXP_LE.setText(objectPressed.listToDisplay[10])
    ui.NodeCID_LE.setText(objectPressed.listToDisplay[1])



def startNewRandomPlot():
    plotKind = 'Random'
    startNewPlot(plotKind)

def startNewPlot(plotKind):
    path = os.path.dirname(os.path.realpath(__file__))

    winWidth = 1200
    winHeight = 800
    win = PlotWindow(winHeight, winWidth, 'plot', 1, 1)
    global plotWinObj, CBsList, arrowsList, objectPressed, mainCurrentMouse
    plotWinObj = win.winObj
    phase = 0
    plotCounter = 0
    objectPressed = None
    while 1:

        try:
            if phase == 0:
                # initEntry = PlotEntry(500, 200, 5, '0: Import xml 1: random 2: manually', 1, plotWinObj)
                PlotCircle.stopThreadTrigger.clear()

                if plotKind == 'Random':
                    initRandomMess=PlotEntry(500, 700,0, False, 'Before pressing "Apply" select the initial parameters for the nodes (Frequency, BW and Tx Power)\nunder the "Node Parameters" pane','red',0,plotWinObj)
                    initRandomEntry = PlotEntry(500, 200, 5, True, 'Select number of units','black', 1, plotWinObj)
                    apply = 0
                    while not apply:
                        currentMouse = plotWinObj.getMouse()
                        apply = initRandomEntry.applyRectObj.rectPress(currentMouse)

                    placeOption = initRandomEntry.GetText()
                    #print(placeOption)
                    initRandomEntry.hideEntry()
                    initRandomMess.hideEntry()
                    freq = ui.NodeFreq_L.text()
                    BW = ui.NodeBW_L.text()
                    txPower = ui.NodeTXP_LE.text()
                    CBsList, arrowsList = randomInitCBs(win.plotQueue, winWidth, winHeight, placeOption, freq, BW, txPower)
                    drawCircles(plotWinObj)
                    phase = 1

                # apply = 0
                # while not apply:
                #     currentMouse = plotWinObj.getMouse()
                #
                #     apply = initEntry.applyRectObj.rectPress(currentMouse)
                #
                #     if apply:
                #         placeOption = initEntry.GetText()
                #         print(placeOption)

                        # if placeOption == '0':
                        #     initEntry.hideEntry()
                        #     CBsList, arrowsList = importInitCBs(win.plotQueue, path + '/init_conf.xml')
                        #
                        #     drawCircles(plotWinObj)
                        #     phase = 1
                        #     break
                        #
                        # elif placeOption == '1':
                        #     initEntry.hideEntry()
                        #     CBsList, arrowsList = randomInitCBs(win.plotQueue, winWidth, winHeight)
                        #
                        #     drawCircles(plotWinObj)
                        #     phase = 1
                        #     break
                        #
                        # else:
                        #     apply = 0
                        #

            elif phase == 1:  # collect queue data
                try:

                    if not win.plotQueue.empty():

                        toPlot = win.plotQueue.get()
                        calculateTreesRatesAndDeclareTreeRN()
                        plotCounter += 1
                        # if plotCounter >= len(CBsList):
                        #     plotCounter = 0
                        #     calculateTreesRatesAndDeclareTreeRN()
                        print('queue item received')

                        for task in toPlot:
                            taskExecuter(task, arrowsList, plotWinObj)


                except:

                    type, value, tb = sys.exc_info()
                    print('Error Type: ' + str(type) + '\r\nError Value: ' + str(value) + '\r\n')
                    pass

                mainCurrentMouse = plotWinObj.checkMouse()

                if mainCurrentMouse is not None:

                    objectPressed = checkObjectPress(mainCurrentMouse, CBsList, objectPressed)

                    if objectPressed is not None:
                        ui.Node_TE.setText('')
                        printNodeParameters()
                    else:
                        ui.Node_TE.setText('')

            time.sleep(0.1)
        except:

            type, value, tb = sys.exc_info()
            print('Error Type: ' + str(type) + '\r\nError Value: ' + str(value) + '\r\n')
            if str(value).find('closed window'):

                break

            else:
                print('Error Type: ' + str(type) + '\r\nError Value: ' + str(value) + '\r\n')
                raise

    print('Bye bye')
    win.Close()


main()
