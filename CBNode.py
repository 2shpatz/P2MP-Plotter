
import sys


def arrowReq(cir1,cir2,color):
    return 'arrow{CB%d,CB%d,%s}'%(cir1,cir2,color)
    

def main(plotQueue):
    try:
        toPlot=[None]*4
        toPlot[0]=arrowReq(1,2,'black')
        toPlot[1]=arrowReq(2,0,'black')
        toPlot[2]=arrowReq(4,3,'blue')
        toPlot[3]=arrowReq(3,1,'black')
        #toPlot[3]=arrowReq(1,2,'yellow')
        plotQueue.put(toPlot)
        print ('queue put applied')
    except:
        type, value, tb = sys.exc_info()
        print ('Error Type: '+str(type)+'\r\nError Value: '+str(value)+'\r\n')
        pass