import pandas as pd
import numpy as np
from lidarcontroller.lidarsignal import lidarsignal
from lidarcontroller.lidarsignal import lidarsignal
import matplotlib.pyplot as plt

BIN_LONG_TRANCE = 4000
SHOTS_DELAY = 1000 # wait 10s = 300shots/30Hz
OFFSET_BINS = 10
THRESHOLD_METERS = 1000 # meters
LIDAR_FILE='./tr1_532par_500mV_20211001_1740_analog.txt'

data_csv = pd.read_csv(LIDAR_FILE,sep='\n',header=None)
lidar_data = np.array(data_csv[0])
lidar = lidarsignal()
lidar.loadSignal(lidar_data)
lidar.offsetCorrection(OFFSET_BINS)
lidar.rangeCorrection(THRESHOLD_METERS)

lidar.setSurfaceConditions(temperature=298,pressure=1023)
lidar.molecularProfile(wavelength=533,masl=10)
lidar.rayleighFit(3000,5000) # meters

fig,(ax1,ax2,ax3)=plt.subplots(3)
fig.suptitle('LiDAR SMN')
ax1.set(xlabel='height', ylabel='voltage (mV)')
ax2.set(xlabel='height', ylabel='mV x m^2')
ax1.grid()
ax2.grid()
ax1.plot(lidar.range,lidar.raw_signal)
ax2.plot(lidar.range,lidar.rc_signal)
ax3.plot(lidar.range,lidar.rc_signal,'g-',lidar.range,lidar.pr2_mol*lidar.adj_factor,'r-')

plt.show()