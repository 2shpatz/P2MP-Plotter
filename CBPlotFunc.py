from graphics import *
import re
import xml.etree.ElementTree as ET
from random import randrange, randint
import threading
import queue

from math import log10
# import CBNode

from math import sqrt

borderSpaceX = 30
borderSpaceY = 15


class PlotPopup:
    def __init__(self, winHeight, winWidth, title):
        self.winHeight = winHeight
        self.winWidth = winWidth
        self.winObj = GraphWin(title, winWidth, winHeight)

    def Close(self):
        self.winObj.close()


class PlotWindow:

    def __init__(self, winHeight, winWidth, title, tiks, borders):
        self.winHeight = winHeight
        self.winWidth = winWidth
        self.winObj = GraphWin(title, winWidth + borderSpaceX, winHeight + borderSpaceY)
        self.plotQueue = queue.Queue()

        # borders
        if borders:
            self.windowLines = [Line(Point(borderSpaceX, borderSpaceY), Point(borderSpaceX, winHeight + borderSpaceY)),
                                Line(Point(borderSpaceX, borderSpaceY), Point(winWidth + borderSpaceX, borderSpaceY))]
            # Line(Point(borderSpaceX,winHeight), Point(winWidth,winHeight)),
            # Line(Point(winWidth,borderSpaceY), Point(winWidth,winHeight))]
            for line in self.windowLines:
                line.draw(self.winObj)

        if tiks:

            for ind in range(0, winWidth + 1, 50):
                tikText = Text(Point(ind + borderSpaceX, 8), ind)
                tikText.setSize(8)
                tikText.draw(self.winObj)

            for ind in range(0, winHeight + 1, 50):
                tikText = Text(Point(15, ind + borderSpaceY), ind)
                tikText.setSize(8)
                tikText.draw(self.winObj)

    def Close(self):
        self.winObj.close()


class PlotArrow:

    def __init__(self, cir1cen, cir2cen, textToDisplay, lineColor, lineWidth):

        self.cir1cen = cir1cen
        self.cir2cen = cir2cen
        self.setArrowPts()
        self.textToDisplay = textToDisplay

        self.lineColor = lineColor
        self.lineWidth = lineWidth
        # self.Pt1=None
        # self.Pt2=None
        self.arrowTextObj = None
        self.isDrawn = 0
        self.arrowObj = Line(self.Pt1, self.Pt2)

        self.setObjPar()

    def setArrowPts(self):
        try:
            if self.cir1cen.getX() <= self.cir2cen.getX():
                Pt1x = self.cir1cen.getX() + 15
                Pt2x = self.cir2cen.getX() - 15
            else:
                Pt1x = self.cir1cen.getX() - 15
                Pt2x = self.cir2cen.getX() + 15

            if self.cir1cen.getY() <= self.cir2cen.getY():
                Pt1y = self.cir1cen.getY() + 15
                Pt2y = self.cir2cen.getY() - 15
            else:
                Pt1y = self.cir1cen.getY() - 15
                Pt2y = self.cir2cen.getY() + 15

            self.Pt1 = Point(Pt1x, Pt1y)
            self.Pt2 = Point(Pt2x, Pt2y)
        except:
            errorType, value, tb = sys.exc_info()
            print('(setArrowPts)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')

    def setObjPar(self):
        try:
            self.arrowObj.setArrow('last')

            if self.textToDisplay is not None:
                xPos = self.cir1cen.getX() + (self.cir2cen.getX() - self.cir1cen.getX()) / 2
                yPos = (self.cir2cen.getY() + (self.cir2cen.getY() - self.cir1cen.getY()) / 2) - 10
                self.arrowTextObj = Text(Point(xPos, yPos), self.textToDisplay)

            if self.lineWidth is not None:

                self.arrowObj.setWidth(self.lineWidth)
            else:
                self.arrowObj.setWidth(2)

            if self.lineColor is not None:
                self.arrowObj.setOutline(self.lineColor)

        except:
            errorType, value, tb = sys.exc_info()
            print('(setObjPar)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')

    def setArrowColor(self, lineColor):
        try:
            self.lineColor = lineColor
            self.arrowObj.setOutline(lineColor)
        except:
            errorType, value, tb = sys.exc_info()
            print('(setArrowColor)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')

    def setArrowText(self,text):
        try:
            self.textToDisplay = text
            #xPos = self.cir1cen.getX() + (self.cir2cen.getX() - self.cir1cen.getX()) / 2
            #yPos = (self.cir2cen.getY() + (self.cir2cen.getY() - self.cir1cen.getY()) / 2) - 10
            xPos = (self.cir1cen.getX() + self.cir2cen.getX())/2
            yPos = (self.cir1cen.getY() + self.cir2cen.getY())/2

            self.arrowTextObj = Text(Point(xPos, yPos), self.textToDisplay)
            self.arrowTextObj.setSize(7)
            self.arrowTextObj.setTextColor('blue')

        except:
            errorType, value, tb = sys.exc_info()
            print('(setArrowText)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')

    def drawArrow(self, win):
        try:

            if self.isDrawn:
                self.arrowObj.undraw()
                if self.textToDisplay is not None:
                    self.arrowTextObj.undraw()
            self.arrowObj.draw(win)
            self.isDrawn = 1
            if self.textToDisplay is not None:
                self.arrowTextObj.draw(win)


        except:
            errorType, value, tb = sys.exc_info()
            print('(drawArrow)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')

    def hideArrow(self):
        try:
            self.arrowObj.undraw()
            self.isDrawn = 0
            if self.textToDisplay is not None:
                self.arrowTextObj.undraw()
        except:
            errorType, value, tb = sys.exc_info()
            print('(hideArrow)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')


class PlotRect:

    def __init__(self, Pt1, Pt2, textToDisplay, lineColor, lineWidth, BGColor):

        self.Pt1 = Pt1
        self.Pt2 = Pt2
        self.textToDisplay = textToDisplay
        #self.textColor = textColor
        if textToDisplay is not None:
            xPos = Pt1.getX() + (Pt2.getX() - Pt1.getX()) / 2
            yPos = Pt2.getY() - 10
            self.RectTextObj = Text(Point(xPos, yPos), textToDisplay)
            #self.RectTextObj.setTextColor(textColor)


        self.rectObj = Rectangle(self.Pt1, self.Pt2)

        if lineWidth is not None:
            self.rectObj.setWidth(lineWidth)

        if BGColor is not None:
            self.rectObj.setFill(BGColor)

        if lineColor is not None:
            self.rectObj.setOutline(lineColor)

    def drawRect(self, win):
        self.rectObj.draw(win)
        if self.textToDisplay is not None:
            self.RectTextObj.draw(win)

    def hideRect(self):
        self.rectObj.undraw()
        if self.textToDisplay is not None:
            self.RectTextObj.undraw()

    def rectPress(self, pt):
        try:

            if pt.getX() in range(int(self.Pt1.getX()), int(self.Pt2.getX())) and pt.getY() in range(
                    int(self.Pt1.getY()), int(self.Pt2.getY())):

                print('rect pressed')
                return 1
            else:
                return 0

        except:
            errorType, value, tb = sys.exc_info()
            print('(rectPress)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
            pass


class PlotEntry:

    def __init__(self, xPos, yPos, chars, frame, textToDisplay, textColor, addApply, winObj):

        self.xPos = xPos
        self.yPos = yPos
        self.chars = chars
        self.addApply = addApply
        self.textColor = textColor
        self.textToDisplay = textToDisplay
        if textToDisplay is not None:

            self.textObj = Text(Point(xPos, yPos - 25), textToDisplay)
            self.textObj.setTextColor(textColor)
            self.entryRectObjP1 = Point(xPos - len(textToDisplay) * 5, self.yPos - 40)
            self.entryRectObjP2 = Point(xPos + len(textToDisplay) * 5, yPos + 80)
            if frame:
                self.entryRectObj = PlotRect(self.entryRectObjP1, self.entryRectObjP2, None, None, None, None)
        if chars:
            self.entryObj = Entry(Point(xPos, yPos + 20), chars)
        else:
            self.entryObj = Text(Point(xPos, yPos + 20), '')

        if addApply:
            self.applyRectObjP1 = Point(self.entryRectObjP2.getX() - 50, self.entryRectObjP2.getY() - 35)
            self.applyRectObjP2 = Point(self.entryRectObjP2.getX() - 5, self.entryRectObjP2.getY() - 5)
            self.applyRectObj = PlotRect(self.applyRectObjP1, self.applyRectObjP2, 'Apply', None, None, None)
            # self.applyRectObjText=Text(self.applyRectObj.getCenter(),'Apply')
        self.drawEntry(winObj)


    def GetText(self):
        return self.entryObj.getText()

    def drawEntry(self, win):

        self.entryObj.draw(win)
        if self.chars:
            self.entryRectObj.drawRect(win)
        if self.textToDisplay:
            self.textObj.draw(win)
        if self.addApply:
            self.applyRectObj.drawRect(win)
            # self.applyRectObjText.draw(win)

    def hideEntry(self):

        self.entryObj.undraw()
        self.textObj.undraw()
        try:
            self.entryRectObj.hideRect()
        except:
            pass
        if self.addApply:
            self.applyRectObj.hideRect()
            # self.applyRectObjText.undraw()


class PlotCircle:
    CIDList = [None]
    RSRPConnectionTH = -100
    stopThreadTrigger = threading.Event()

    def __init__(self, plotQueue, cirInd, center, radius, textToDisplay, lineColor, BGColor, innerCirColor, BW,
                 freq, txPower, CID):
        try:
            self.plotQueue = plotQueue
            self.ind = cirInd
            PlotCircle.CIDList.append(None)

            # graphics
            self.radius = radius
            self.lineColor = lineColor
            self.BGColor = BGColor
            self.innerCirColor = innerCirColor
            self.arrowColor = 'cyan'

            self.cirCenter = Point(int(center[center.find('[') + 1:center.find(',')]) + borderSpaceX,
                                   int(center[center.find(',') + 1:center.find(']')]) + borderSpaceY)

            self.textToDisplay = textToDisplay

            self.createCirObj()
            self.setCirObjPar()
            self.nodeSelected = False

            # RF Parameters
            self.txPower=txPower
            self.BW = BW
            self.freq = freq

            if (CID is None) or (CID in PlotCircle.CIDList):
                CID = randint(100, 999)
                while CID in PlotCircle.CIDList:
                    CID = randint(100, 999)
                self.CID = CID
            else:
                self.CID = CID

            PlotCircle.CIDList[self.ind] = self.CID

            self.mode = 'Client'  # client / root
            self.state = 'off'
            self.RNObj = None
            self.noOfCpe = 0
            self.startupTime = randint(0, 5)
            self.RNCID = self.CID
            self.noOfConnectedNodes = 0
            self.noOfNodesInTree = 1
            self.treeNo = self.ind  # ID (index) of the node's tree
            self.nodeRate = self.noOfConnectedNodes * 1000 + self.CID
            self.treeRate = None
            self.nextHopNode = None
            self.listOfConnNodes = [None]
            self.nextHopNodeFound = 0
            self.inboundConnection = False
            self.updateListToDisplay()

            self.CBNodeThread = None


        except:

            errorType, value, tb = sys.exc_info()
            print('(PlotCircle)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
            raise

    def updateListToDisplay(self):
        try:
            if self.nextHopNode is None:
                nextHopCID = 'n/a'
            else:
                nextHopCID = str(self.nextHopNode.CID)
            self.listToDisplay = [self.textToDisplay, str(self.CID), str(self.treeNo), str(self.treeRate), str(self.RNCID), nextHopCID, self.state, self.mode,
                                                                                                                          self.freq, self.BW, self.txPower,
                                                                                                                                             str(self.noOfConnectedNodes), str(self.noOfCpe),
                                  str(int(self.cirCenter.getX()) - borderSpaceX) + ',' + str(
                                      int(self.cirCenter.getY()) - borderSpaceY)]

        except:

            errorType, value, tb = sys.exc_info()
            print('(updateListToDisplay)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')

    def declareTreeRootNode(self, nodeObj):  # used after tree is created
        try:
            tempOwnTreeRate = findNoOfNodesInTree(nodeObj) * 1000 + int(self.CID)
            if nodeObj.treeRate is None:
                if self.nodeRate > nodeObj.nodeRate:

                    self.mode = 'root'
                    nodeObj.mode = 'client'
                    nodeObj.RNObj = self.RNObj = self
                    nodeObj.treeRate = self.nodeRate = tempOwnTreeRate
                    nodeObj.treeNo = self.treeNo = self.ind

                else:
                    self.mode = 'client'
                    nodeObj.mode = 'root'
                    self.RNObj = nodeObj.RNObj
                    nodeObj.treeRate = self.nodeRate = findNoOfNodesInTree(nodeObj) * 1000 + nodeObj.CID
                    nodeObj.treeNo = self.treeNo = nodeObj.ind


            else:

                if tempOwnTreeRate > nodeObj.treeRate:
                    self.mode = 'root'
                    nodeObj.mode = 'client'
                    nodeObj.RNObj = self.RNObj = self
                    nodeObj.treeRate = self.nodeRate = tempOwnTreeRate
                    nodeObj.treeNo = self.treeNo = self.ind

        except:

            errorType, value, tb = sys.exc_info()
            print('(declareTreeRootNode)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')

    def createCirObj(self):

        self.cirObj = Circle(self.cirCenter, self.radius)
        self.innerCirObj = Circle(self.cirCenter, 3)

    def setCirObjPar(self):

        self.cirObj.setWidth(3)
        self.innerCirObj.setWidth(6)
        if self.textToDisplay is not None:
            xPos = self.cirCenter.getX()
            yPos = self.cirCenter.getY() + self.radius + 10
            self.cirTextObj = Text(Point(xPos, yPos), self.textToDisplay)
            self.cirTextObj.setSize(9)
            self.cirTextObj.setStyle('bold')
        if self.BGColor is not None:
            self.cirObj.setFill(self.BGColor)

        if self.lineColor is not None:
            self.cirObj.setOutline(self.lineColor)

        if self.innerCirColor is not None:
            self.innerCirObj.setOutline(self.innerCirColor)

    def getCirCenter(self):

        return self.cirObj.getCenter()

    def moveCir(self, pt, winObj, arrowsList):
        try:

            self.hideCir()
            self.cirCenter = pt
            self.createCirObj()
            # self.cirObj=Circle(self.cirCenter,self.radius)
            self.setCirObjPar()
            for arrowInd in range(0, len(arrowsList)):

                arrowsList[self.ind][arrowInd].arrowObj.undraw()
                arrowsList[arrowInd][self.ind].arrowObj.undraw()

                arrowsList[self.ind][arrowInd].cir1cen = self.cirCenter
                arrowsList[self.ind][arrowInd].setArrowPts()
                arrowsList[self.ind][arrowInd].arrowObj = Line(arrowsList[self.ind][arrowInd].Pt1,
                                                               arrowsList[self.ind][arrowInd].Pt2)
                arrowsList[self.ind][arrowInd].setObjPar()

                arrowsList[arrowInd][self.ind].cir2cen = self.cirCenter
                arrowsList[arrowInd][self.ind].setArrowPts()
                arrowsList[arrowInd][self.ind].arrowObj = Line(arrowsList[arrowInd][self.ind].Pt1,
                                                               arrowsList[arrowInd][self.ind].Pt2)
                arrowsList[arrowInd][self.ind].setObjPar()

                if arrowsList[self.ind][arrowInd].isDrawn:
                    arrowsList[self.ind][arrowInd].drawArrow(winObj)

                if arrowsList[arrowInd][self.ind].isDrawn:
                    arrowsList[arrowInd][self.ind].drawArrow(winObj)

            self.drawCir(winObj)
            updateScanMatrix(self,arrowsList)
            self.plotQueueClear()
        except:
            errorType, value, tb = sys.exc_info()
            print('(moveCir)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
            pass

    def plotQueueClear(self):
        try:
            while not self.plotQueue.empty():
                self.plotQueue.get()
        except:
            errorType, value, tb = sys.exc_info()
            print('(moveCir)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
            pass

    def selectNode(self):
        try:
            self.nodeSelected = True
            self.innerCirObj.setOutline("blue")
            self.cirObj.setOutline("blue")
        except:
            errorType, value, tb = sys.exc_info()
            print('(selectNode)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
            pass

    def drawCir(self, win):
        try:
            self.cirObj.draw(win)
            self.innerCirObj.draw(win)
            if self.textToDisplay is not None:
                self.cirTextObj.draw(win)
        except:
            errorType, value, tb = sys.exc_info()
            print('(drawCir)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
            pass

    def hideCir(self):
        try:
            self.cirObj.undraw()
            self.innerCirObj.undraw()
            if self.textToDisplay is not None:
                self.cirTextObj.undraw()
        except:
            errorType, value, tb = sys.exc_info()
            print('(hideCir)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
            pass

    def deleteCir(self, arrowsList):
        try:
            self.hideCir()
            self.cirCenter = Point(-1, -1)
            for arrowInd in range(0, len(arrowsList)):
                arrowsList[self.ind][arrowInd].hideArrow()
                arrowsList[arrowInd][self.ind].hideArrow()
        except:
            errorType, value, tb = sys.exc_info()
            print('(deleteCir)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
            pass

    def changeState(self, newState):
        try:
            optionalStates = ['off', 'seeking', 'connected', 'tree_connected']
            if newState in optionalStates:
                self.state = newState
                self.dyeState()
        except:
            errorType, value, tb = sys.exc_info()
            print('(changeState)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
            pass

    def dyeState(self):
        try:
            if self.state == 'off':
                self.cirObj.setOutline("black")

            elif self.state == 'seeking':
                self.cirObj.setOutline("orange")
                self.arrowColor = 'cyan'
            elif self.state == 'connected' or self.state == 'tree_connected':
                self.cirObj.setOutline("green")
                if self.nextHopNode is not None:
                    if -70 > scanMatrix[self.ind][self.nextHopNode.ind] >= -90:
                        self.arrowColor = 'lime green'
                    elif 0 > scanMatrix[self.ind][self.nextHopNode.ind] >= -70:
                        self.arrowColor = 'dark green'
                    else:
                        self.arrowColor = 'red'
            if self.mode == 'root':
                self.cirObj.setFill('cyan')
            else:
                self.cirObj.setFill('SystemWindow')

        except:
            errorType, value, tb = sys.exc_info()
            print('(dyeState)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
            pass
    ####################################CBNode##########################################
    ####################################CBNode##########################################
    ####################################CBNode##########################################

    def findBestNode(self):  # next version should include next best options
        try:
            self.treeNo = -1
            bestNodeOption = None
            bestSnrNodeOption = None

            treeFound = 0
            nodeFound = 0
            if self.nextHopNode is not None:
                bestNodeOption = bestSnrNodeOption = self.nextHopNode

            for ind in range(len(cirList)):
                if ind == self.ind:
                    continue


                # if self.nextHopNode is not None and ( self.nextHopNode.treeNo == cirList[ind].treeNo or self.nextHopNode.treeRate > cirList[ind].treeRate):
                if self.nextHopNode is not None and self.nextHopNode.treeRate > cirList[ind].treeRate:

                    continue

                if bestNodeOption is None:
                    bestNodeOption = bestSnrNodeOption = cirList[ind]

                if 0 > scanMatrix[self.ind][ind] > self.RSRPConnectionTH:

                    nodeFound = 1
                    if scanMatrix[self.ind][ind] > scanMatrix[self.ind][bestSnrNodeOption.ind]:
                        bestSnrNodeOption = cirList[ind]

                    if cirList[ind].treeRate is None and cirList[ind] is not None:
                        #cirList[ind].treeRate = findNoOfNodesInTree(cirList[ind]) * 1000 + int(self.CID)
                        tempTreeRate = findNoOfNodesInTree(cirList[ind]) * 1000 + int(self.CID)
                    if bestNodeOption.treeRate is None:
                        # bestNodeOption.treeRate = findNoOfNodesInTree(bestNodeOption) * 1000 + int(bestNodeOption.CID)
                        tempBestNodeTreeRate = findNoOfNodesInTree(bestNodeOption) * 1000 + int(bestNodeOption.CID)
                    if self.nextHopNode is not None:
                        if cirList[ind].treeNo == bestNodeOption.treeNo:
                            treeFound = 1
                            if scanMatrix[self.ind][ind] > scanMatrix[self.ind][bestNodeOption.ind]:
                                bestNodeOption = cirList[ind]
                                # self.inboundConnection = True
                            # if self.nextHopNode.treeNo == bestNodeOption.treeNo:
                            #     if cirList[ind].nextHopNode == self:
                            #     # if self.inboundConnection:
                            #
                            #         bestNodeOption = self.nextHopNode
                            #     else:
                            #         bestNodeOption = bestSnrNodeOption
                    #     if tempTreeRate > tempBestNodeTreeRate:
                    #         bestNodeOption = cirList[ind]
                    # # else:
                    #     if cirList[ind].treeRate > bestSnrNodeOption.treeRate:
                        elif cirList[ind].treeRate > self.nextHopNode.treeRate:
                            treeFound = 1
                            bestNodeOption = cirList[ind]

            if not nodeFound:
                replay = None

            elif treeFound:



                if bestNodeOption != cirList[self.ind]:



                    replay = bestNodeOption

                else:
                    replay = None
            else:
                if bestSnrNodeOption != cirList[self.ind]:


                    replay = bestSnrNodeOption

                else:
                    replay = None

            print('for CB %d bestNodeOption= %d and bestSnrNodeOption= %d' % (
            self.ind, bestNodeOption.ind, bestSnrNodeOption.ind))

            if replay is not None:
                if self.nextHopNode is None:
                    self.nextHopNode = replay
                    self.declareTreeRootNode(replay)

                    # if treeFound:
                    #
                    #
                    #
                    #     # if self.treeNo == bestNodeOption.treeNo:
                    #     #
                    #     #     if bestSnrNodeOption.nextHopNode.CID == self.CID:
                    #     #
                    #     #         bestNodeOption = self.nextHopNode
                    #     #     else:
                    #     #         bestNodeOption = bestSnrNodeOption
                    #     self.nextHopNode = replay
                    #
                    # else:
                    #     self.nextHopNode = bestSnrNodeOption

                else:


                    if bestSnrNodeOption.treeNo == bestNodeOption.treeNo:
                        if self.treeNo == bestNodeOption.treeNo:
                            self.inboundConnection = True
                        if bestSnrNodeOption.nextHopNode.CID != self.CID:
                            self.nextHopNode = bestSnrNodeOption

                        elif bestNodeOption.nextHopNode.CID != self.CID:
                            self.nextHopNode = bestNodeOption

                    else:
                        self.nextHopNode = replay

                    if self.nextHopNode.listOfConnNodes[0] is None:
                        self.nextHopNode.listOfConnNodes[0] = replay
                    elif replay not in self.nextHopNode.listOfConnNodes:
                        self.nextHopNode.listOfConnNodes.append(replay)
                    #self.nextHopNode.noOfConnectedNodes = len(self.nextHopNode.listOfConnNodes)
            # else:
            #     self.nextHopNode = None
            # return replay

        except:
            errorType, value, tb = sys.exc_info()
            print('(findBestNode) Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
            pass

    def CBNode(self):
        try:


            while not PlotCircle.stopThreadTrigger.wait(1):
                toPlot = [None]
                if not self.nodeSelected:
                    self.dyeState()
                # else:
                #     continue
                self.noOfConnectedNodes = len(self.listOfConnNodes)

                if not self.nextHopNodeFound:
                    self.changeState('seeking')
                    time.sleep(1)
                    if self.nextHopNode is None:
                        self.findBestNode()
                        if self.nextHopNode is not None:
                            self.treeNo = self.nextHopNode.treeNo
                    if self.nextHopNode is not None and not self.nextHopNodeFound:
                        self.changeState('tree_connected')
                        toPlot[0] = arrowReq(self.ind, self.nextHopNode.ind, self.arrowColor, 1)
                        self.nextHopNodeFound = 1

                else:
                    ###############
                    # if self.nextHopNode is not None:
                    #     tempRNCID = self.RNCID
                    #     for cir in cirList:
                    #         if cir.RNCID != tempRNCID:
                    #             break
                    #     if tempRNCID == self.RNCID:
                    #         continue
                    ###############
                    self.nodeRate = self.noOfConnectedNodes * 1000 + self.CID
                    if not self.inboundConnection:

                        self.findBestNode()
                    if self.nextHopNode is not None:
                        self.treeNo = self.nextHopNode.treeNo
                    if self.nextHopNode is not None:
                        toPlot[0] = arrowReq(self.ind, self.nextHopNode.ind, self.arrowColor, 1)
                    #self.declareTreeRootNode(self.RNObj)
                    time.sleep(3)


                #
                # else:
                #     if self.treeNo is None:

                # toPlot[0] = arrowReq(1, 2, 'black')
                # toPlot[1] = arrowReq(2, 0, 'black')
                # toPlot[2] = arrowReq(4, 3, 'blue')
                # toPlot[3] = arrowReq(3, 1, 'black')
                # toPlot[3]=arrowReq(1,2,'yellow')
                if toPlot[0] is not None:
                    self.plotQueue.put(toPlot)
                    print('queue put applied')
                time.sleep(1)
        except:
            errorType, value, tb = sys.exc_info()
            print('(CBNode) Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
            pass

    ##############################################################################


def arrowReq(cir1, cir2, color, enableText):
    return 'arrow{CB%d,CB%d,%s,%s}' % (cir1, cir2, color, enableText)


def drawCircles(win):
    for ind in range(0, len(cirList)):
        cirList[ind].drawCir(win)


def importInitCBs(plotQueue, xmlFile):
    global cirList

    tree = ET.parse(xmlFile)
    root = tree.getroot()
    numberOfCBs = len(root)
    cirList = [None] * numberOfCBs
    for cirInd in range(0, numberOfCBs):

        cen = str(root[cirInd][0].text)
        rad = int(str(root[cirInd][1].text))
        lineColor = str(root[cirInd][2].text)
        BGcolor = str(root[cirInd][3].text)
        textToDisplay = str(root[cirInd][4].text)

        if lineColor == 'None':
            lineColor = None

        if BGcolor == 'None':
            BGcolor = None

        cirList[cirInd] = PlotCircle(plotQueue, cirInd, cen, rad, textToDisplay, lineColor, BGcolor, 'green', '5', '2100',
                                     '26', None)
    arrowsList = createArrowsList()
    createScanMatrix(numberOfCBs,arrowsList)


    # startCBNodeThreads()

    return cirList, arrowsList


def randomInitCBs(plotQueue, winWidth, winHeight, numberOfUnits, freq, BW, txPower):
    try:
        global cirList

        numberOfCBs = int(numberOfUnits)
        cirList = [None] * numberOfCBs

        # xPos = randrange(100, winWidth - 100)
        # yPos = randrange(100, winHeight - 100)
        # cirInd = 0

        for cirInd in range(0, numberOfCBs):
            xPos = randrange(100, winWidth)
            yPos = randrange(100, winHeight)
            cirList[cirInd] = PlotCircle(plotQueue, cirInd, '[%d,%d]' % (xPos, yPos), 20, 'P2MP' + str(cirInd), 'black',
                                         None, 'green', BW, freq, txPower, None)


        arrowsList = createArrowsList()
        createScanMatrix(numberOfCBs,arrowsList)
        # startCBNodeThreads()
        return cirList, arrowsList
    except:
        errorType, value, tb = sys.exc_info()
        print('(randomInitCBs)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
        raise


def createArrowsList():
    try:
        numberOfCBs = len(cirList)
        arrowsList = [[0 for x in range(numberOfCBs)] for x in range(numberOfCBs)]
        for cirInd1 in range(0, numberOfCBs):
            for cirInd2 in range(0, numberOfCBs):
                arrowsList[cirInd1][cirInd2] = PlotArrow(cirList[cirInd1].getCirCenter(),
                                                         cirList[cirInd2].getCirCenter(), None, None, None)

        return arrowsList

    except:
        errorType, value, tb = sys.exc_info()
        print('(createArrowsList)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')


def twoPtDis(pt0, pt1):
    try:
        return sqrt((pt0.getX() - pt1.getX()) ** 2 + (pt0.getY() - pt1.getY()) ** 2)

    except:
        errorType, value, tb = sys.exc_info()
        print('(twoPtDis)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')


def snrCalculator(distance, freq, txPower, BW):
    try:

        ############# pass lose calculation - Winner module ###########
        # freq in GHz, txPower in dBm, BW in MHz
        # 3m < d < 100m 1m < h < 2.5m
        # LOS
        A = 18.7
        B = 46.8
        C = 20
        X = 0
        passLoss = A * log10(distance) + B + C * log10(float(freq) / 5) + X
        ################################################################

        RSSI = int(txPower)-passLoss
        RSRP = RSSI - 10 * log10(12 * 5 * float(BW))

        return round(RSRP)
    except:
        errorType, value, tb = sys.exc_info()
        print('(snrCalculator) Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')


def createScanMatrix(numberOfCBs,arrowsList):
    try:
        # scanMatrix[modem][eNB]

        global scanMatrix
        scanMatrix = [[None] * numberOfCBs for i in range(numberOfCBs)]
        for ind1 in range(numberOfCBs):
            for ind2 in range(numberOfCBs):
                twoNodesDistance = twoPtDis(cirList[ind1].getCirCenter(), cirList[ind2].getCirCenter())

                scanMatrix[ind1][ind2] = snrCalculator(twoNodesDistance, float(cirList[ind2].freq)*0.001, cirList[ind2].txPower, cirList[ind2].BW)


                arrowsList[ind1][ind2].setArrowText("Dis=%d\nRSRP=%s"%(int(twoNodesDistance),str(scanMatrix[ind1][ind2])))

        print(scanMatrix)
    except:
        errorType, value, tb = sys.exc_info()
        print('(createScanMatrix)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')


def updateScanMatrix(NodeObj,arrowsList):  # used when one of the Nodes changes location or the environment has been changed
    try:
        print('start updateScanMatrix')
        global scanMatrix
        for Node in cirList:
            if NodeObj != Node:
                twoNodesDistance = twoPtDis(NodeObj.getCirCenter(), Node.getCirCenter())
                scanMatrix[Node.ind][NodeObj.ind] = snrCalculator(twoNodesDistance,float(cirList[NodeObj.ind].freq)*0.001, cirList[NodeObj.ind].txPower, cirList[NodeObj.ind].BW)
                arrowsList[Node.ind][NodeObj.ind].setArrowText("Dis=%d\nRSRP=%s"%(int(twoNodesDistance),str(scanMatrix[Node.ind][NodeObj.ind])))

        for Node in cirList:
            if NodeObj != Node:
                twoNodesDistance = twoPtDis(Node.getCirCenter(), NodeObj.getCirCenter())
                scanMatrix[NodeObj.ind][Node.ind] = snrCalculator(twoNodesDistance,float(cirList[NodeObj.ind].freq)*0.001, cirList[NodeObj.ind].txPower, cirList[NodeObj.ind].BW)
                arrowsList[NodeObj.ind][Node.ind].setArrowText("Dis=%d\nRSRP=%s"%(int(twoNodesDistance),str(scanMatrix[NodeObj.ind][Node.ind])))

    except:
        errorType, value, tb = sys.exc_info()
        print('(updateScanMatrix)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')


def startCBNodeThreads():
    try:
        if cirList is not None:
            for node in cirList:
                node.CBNodeThread = threading.Thread(target=node.CBNode, args=())
                node.CBNodeThread.daemon = True
                node.CBNodeThread.start()



    except:

        errorType, value, tb = sys.exc_info()
        print('(startCBNodeThreads)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
        pass


def stopCBNodeThreads():

    try:
        PlotCircle.stopThreadTrigger.set()
        if cirList is not None:
            for node in cirList:
                node.CBNodeThread.join()

    except:

        errorType, value, tb = sys.exc_info()
        print('(startCBNodeThreads)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
        raise

def taskExecuter(task, arrowsList, winObj):
    try:
        # task pattern: plot_task{arg1;arg2;...;}

        taskerrorType = task[:task.find('{')]
        # =re.search(r'(.*?)({(.*?),(.*?),(.*?)}),task, re.M|re.I)

        taskContent = task[task.find('{'):task.find('}') + 1]
        print(taskContent)

        if taskerrorType == 'arrow':
            regex = re.search(r'{CB(.*?),CB(.*?),(.*?),(.*?)}', taskContent, re.M | re.I)

            ind1 = int(regex.group(1))
            ind2 = int(regex.group(2))
            color = regex.group(3)
            textEnable = regex.group(4)
            if textEnable == '1':
                arrowsList[ind1][ind2].arrowTextObj.undraw()
                arrowsList[ind1][ind2].arrowTextObj.draw(winObj)
            else:
                arrowsList[ind1][ind2].arrowTextObj.undraw()
            # ind1=int(task[task.find('cir1=CB')+7:task.find(';',task.find('cir1='))])
            # ind2=int(task[task.find('cir2=CB')+7:task.find(';',task.find('cir2='))])
            # color=task[task.find('color=')+6:task.find(';',task.find('color='))]
            for Ind3 in range(len(arrowsList)):
                arrowsList[ind1][Ind3].hideArrow()
            arrowsList[ind1][ind2].setArrowColor(color)

            arrowsList[ind1][ind2].drawArrow(winObj)

    except:
        errorType, value, tb = sys.exc_info()
        print('(taskExecuter)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')


def checkObjectPress(currentMouse, CBsList, currentSelected):
    try:
        print('start checkObjectPress')

        if currentSelected is not None:
            currentSelected.nodeSelected = False
            currentSelected.innerCirObj.setOutline(currentSelected.innerCirColor)
            # currentSelected.cirObj.setOutline(currentSelected.lineColor)
            currentSelected.dyeState()
        for CB in CBsList:

            if (CB.cirCenter.getX() - 3) <= currentMouse.getX() <= (CB.cirCenter.getX() + 3) and (
                    CB.cirCenter.getY() - 3) <= currentMouse.getY() <= (CB.cirCenter.getY() + 3):
                if currentSelected is not None:
                    CB.nodeSelected = True
                CB.innerCirObj.setOutline("blue")
                CB.cirObj.setOutline("blue")
                return CB

        return None
    except:

        errorType, value, tb = sys.exc_info()
        print('(checkObjectPress)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
        pass

def calculateTreesRatesAndDeclareTreeRN():
    try:
        print('Start calculateTreesRatesAndDeclareTreeRN')
        noOfTrees = 0
        treesList = [cirList[0].treeNo]
        treeRNList = [cirList[0]]
        numberOfCBs = len(cirList)
        for ind in range(numberOfCBs):
            cirList[ind].noOfConnectedNodes = len(cirList[ind].listOfConnNodes)
            if cirList[ind].treeNo not in treesList:
                treesList.append(cirList[ind].treeNo)

                treeRNList.append(cirList[ind])
            else:
                tempTreeInd = treesList.index(cirList[ind].treeNo)

            if cirList[ind].noOfConnectedNodes > treeRNList[tempTreeInd].noOfConnectedNodes:
                treeRNList[tempTreeInd] = cirList[ind]

        for Node in treeRNList:
            Node.treeRate = findNoOfNodesInTree(Node) * 1000 + Node.CID
            Node.mode = 'root'

        for ind in range(numberOfCBs):


            tempTreeInd = treesList.index(cirList[ind].treeNo)
            if cirList[ind].CID != treeRNList[tempTreeInd].CID:
                cirList[ind].treeNo = treeRNList[tempTreeInd].treeNo
                cirList[ind].RNode = treeRNList[tempTreeInd]
                cirList[ind].RNCID = treeRNList[tempTreeInd].CID
                cirList[ind].treeRate = treeRNList[tempTreeInd].treeRate
                cirList[ind].mode = 'client'

    except:

        errorType, value, tb = sys.exc_info()
        print('(calculateTreesRatesAndDeclareTreeRN)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
        pass

def findNoOfNodesInTree(nodeObj):

    try:
        counter = 0

        for node in cirList:
            if node.treeNo == nodeObj.treeNo:
                counter += 1

        nodeObj.noOfNodesInTree = counter
        return counter

    except:

        errorType, value, tb = sys.exc_info()
        print('(findNoOfNodesInTree)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
        pass
# def queueCliReq(CLIEntry, cliWinObj, plotWinObj, cirList, arrowsList):
#     try:
#         CliApply = 0
#         # CliCurrentMouse=cliWinObj.getMouse()
#
#         cliReq = CLIEntry.GetText()
#
#         print(cliReq)
#
#         Req = cliReq[:cliReq.find('(')].lower()
#
#         if Req == 'movecb':
#             args = [int(s) for s in cliReq[cliReq.find('(') + 1:cliReq.find(')')].split(',') if s.isdigit()]
#             # print(args)
#             args[1] = args[1] + borderSpaceX
#             args[2] = args[2] + borderSpaceY
#             cirList[args[0]].moveCir(Point(args[1], args[2]), plotWinObj, arrowsList)
#
#     except:
#         errorType, value, tb = sys.exc_info()
#         print('(queueCliReq)Error errorType: ' + str(errorType) + '\r\nError Value: ' + str(value) + '\r\n')
#
#
# def crateCli():
#     CLIWin = PlotWindow(150, 250, 'CLI', 0, 0)
#     CLIEntry = PlotEntry(125, 50, 20, 'Enter CLI request', 1, CLIWin.winObj)
#
#     return CLIWin.winObj, CLIEntry
#
