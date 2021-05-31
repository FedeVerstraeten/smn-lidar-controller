import licelcontroller.settings
from licelcontroller.interface import Controller
import time

# override settings
licelcontroller.settings.HOST = "10.49.234.234"
licelcontroller.settings.PORT = 2055

if __name__ == '__main__':
    c = Controller()
##    c.select(0,1,2,3)
    c.select(1)
    c.mstart()
##    c.mstop()
    c.run()
    time.sleep(1)
    c.mstop()
    c.data()
    c.run()
