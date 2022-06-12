import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

LIDAR_FILE='./analog_500mV.txt'

data_csv = pd.read_csv(LIDAR_FILE,sep='\n',header=None)
data=pd.DataFrame(data_csv)

y = np.array(data[0])
#y=y[5:] # offset correction

x = np.arange(0, len(y), 1)

 

# LiDAR signal range correction since bin number 1000

yr = (y-np.mean(y[1000:]))*(x**2)
fig,(ax1,ax2)=plt.subplots(2)

fig.suptitle('LiDAR SMN')
ax1.set(xlabel='bins', ylabel='voltage (mV)')
ax2.set(xlabel='bins', ylabel='mV x m^2')
ax1.grid()
ax2.grid()
ax1.plot(x,y)
ax2.plot(x,yr)
plt.show()
