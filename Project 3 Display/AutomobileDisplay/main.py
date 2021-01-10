import threading
import ControlWindow
import Display

class myThread(threading.Thread):
    def __init__(self, method, info):
        threading.Thread.__init__(self)
        self.method = method
        self.info = info
    def run(self):
        print("start of :",self.info)
        self.method()
        

def main():
    #Create Threads
   thread1 = myThread(ControlWindow.controlWindow,"Control-Window for Properties of the Car")
   thread2 = myThread(Display.display,"Display of Driver")
   #Start Threads
   thread1.start()
   thread2.start()

if __name__ == "__main__":
    main()