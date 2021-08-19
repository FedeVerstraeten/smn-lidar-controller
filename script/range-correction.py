import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

LIDAR_FILE='analog.txt'

data_csv = pd.read_csv(LIDAR_FILE,sep='\n',header=None)
data=pd.DataFrame(data_csv)

y = np.array(data[0])
x = np.arange(0, len(y), 1)

# LiDAR signal range correction since bin number 1000

yr = (y-np.mean(y[1000:]))*(x**2)
plt.plot(x,yr)
plt.show()