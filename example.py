import licel_controller.settings
from licel_controller.interface import Controller
import time

# override settings
licel_controller.settings.HOST = "10.49.234.234"
licel_controller.settings.PORT = 2055

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
