import threading
import queue
import CBPlotter
import CBNode

plotQueue=queue.Queue()



CBPlotterThread=threading.Thread(target=CBPlotter.main,args=(plotQueue,))
CBPlotterThread.daemon =True
CBPlotterThread.start()

CBNodeThread=threading.Thread(target=CBNode.main,args=(plotQueue,))
CBNodeThread.daemon =True
CBNodeThread.start()