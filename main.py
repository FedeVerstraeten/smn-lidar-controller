from lidarcontroller.licelcontroller import licelcontroller
from lidarcontroller import licelsettings
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
  
  # basic settings
  BIN_LONG_TRANCE = 4000
  SHOTS_DELAY = 10000 # wait 10s = 300shots/30Hz

  # initialization
  lc = licelcontroller()
  lc.openConnection('10.49.234.234',2055)
  tr=0 #first TR
  lc.selectTR(tr)
  lc.setInputRange(licelsettings.MILLIVOLT500)
  # lc.setThresholdMode(licelsettings.THRESHOLD_LOW) #Is this necessary?
  # lc.setDiscriminatorLevel(8) # can be set between 0 and 63
  
 
  # start the acquisition
  lc.clearMemory()
  lc.startAcquisition()
  lc.msDelay(SHOTS_DELAY)
  lc.stopAcquisition() 
  #lc.waitForReady(100) # wait till it returns to the idle state

  ## get the shotnumber 
  if lc.getStatus() == 0:
    if (lc.shots_number > 1):
      cycles = lc.shots_number - 2 # WHY??!

  # read from the TR triggered mem A
  data_lsw = lc.getDatasets(tr,"LSW",BIN_LONG_TRANCE+1,"A")
  data_msw = lc.getDatasets(tr,"MSW",BIN_LONG_TRANCE+1,"A")
  
  # combine, normalize an scale data to mV
  data_accu,data_clip = lc.combineAnalogDatasets(data_lsw, data_msw)
  data_phys = lc.normalizeData(data_accu,cycles)
  data_mv = lc.scaleAnalogData(data_phys,licelsettings.MILLIVOLT500) 
  
  # DUMP THE DATA INTO A FILE
  with open('analog.txt', 'w') as file: # or analog.dat 'wb'
    np.savetxt(file,data_mv,delimiter=',')


  # Plot
  t = np.arange(0, len(data_mv), 1)
  fig, ax = plt.subplots()
  ax.plot(t, data_mv)
  ax.set(xlabel='bins', ylabel='voltage (mV)',title='SMN LICEL')
  ax.grid()
  fig.savefig("test.png")
  plt.show()

  lc.closeClonnection()
