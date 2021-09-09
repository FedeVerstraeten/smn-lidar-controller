import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import constants
from scipy import integrate
from scipy.interpolate import interp1d

def smooth(y, box_pts):
  box = np.ones(box_pts)/box_pts
  y_smooth = np.convolve(y, box, mode='same')
  return y_smooth

#-------------
#  Parameters
#-------------

# LiDAR 
OFFSET_BINS = 10
BIN_RC_THRESHOLD=1000
wave_length = 532 #nm

# Current surface atmospheric conditions (Av.Dorrego SMN)
SURFACE_TEMP = 300 # [K] 27C
SURFACE_PRESS = 1024 # [hPa]
MASL = 10.0 # meters above sea level (AMSL)

#----------
#  LiDAR
#----------
  
# load data
LIDAR_FILE ='./analog_500mV.txt'
data_csv = pd.read_csv(LIDAR_FILE,sep='\n',header=None)

lidar_signal = np.array(data_csv[0])

# offset correction
lidar_signal=lidar_signal[OFFSET_BINS:]

number_bins = len(lidar_signal)

lidar_bins = np.arange(0, number_bins, 1)


# LiDAR signal range correction since bin number 1000
height = np.arange(0, number_bins, 1)
lidar_bias = np.mean(lidar_signal[BIN_RC_THRESHOLD:])
lidar_rc = (lidar_signal - lidar_bias)*(height**2)

lidar_rc = smooth(lidar_rc,5) # smooth noise
#----------
#  MODEL
#----------

# load data
MODEL_FILE='./US-StdA_DB_CEILAP.csv'
data_csv = pd.read_csv(MODEL_FILE,sep=',',header=None)

height_lowres=np.array(data_csv[0])
temp_lowres=np.array(data_csv[1])
press_lowres=np.array(data_csv[2])

# Height high resolution
# NUM_BINS=4096
# NUM_BINS=1144
height_highres = np.linspace(height_lowres[0], number_bins*7.5, num=number_bins, endpoint=True)
# height_highres = np.arange(height_lowres[index_MASL], number_bins*7.5, 7.5,)
# height_lowres[-1] = height_highres[-1]

index_MASL = (np.abs(height_highres - MASL)).argmin() # Height above mean sea level (AMSL)

# Interpolation Spline 1D
temp_spline = interp1d(height_lowres, temp_lowres, kind='cubic')
temp_highres = temp_spline(height_highres)

press_spline = interp1d(height_lowres, press_lowres, kind='cubic')
press_highres = press_spline(height_highres)

# Scaling the temperature and pressure profiles in the model
# with current surface conditions
temp_highres = SURFACE_TEMP * (temp_highres/temp_highres[index_MASL])
press_highres = SURFACE_PRESS * (press_highres/press_highres[index_MASL])

# atm molecular concentration 
kboltz=constants.k
nmol = (100*press_highres[index_MASL:])/(temp_highres[index_MASL:]*kboltz) 

# alpha y beta
beta_mol = nmol * (550/wave_length)**4.09 * 5.45 * (10**-32)
alpha_mol = beta_mol * (8*np.pi/3)

range_lidar = height_highres[:-index_MASL]
cumtrapz = integrate.cumtrapz(alpha_mol, range_lidar, initial=0)
tm2r_mol = np.exp(-2*cumtrapz)
pr2_mol = beta_mol*tm2r_mol


#----------
#  Min ECM
#----------
bin_init = int(5000/7.5) # 2500m / 7.5m
bin_fin = int(8000/7.5) # 3200m / 7.5m


print(lidar_rc[bin_init])
print(lidar_rc[bin_fin+1])

# sig == lidar_rc
# sigmol == pr2_mol
mNum = np.dot(lidar_rc[bin_init:bin_fin+1],pr2_mol[bin_init:bin_fin+1])
mDen = np.dot(pr2_mol[bin_init:bin_fin+1],pr2_mol[bin_init:bin_fin+1])
m = mNum/mDen

print("Min ECM:",np.format_float_scientific(m))


#----------
#  PLOT
#----------
factor_adj=m

fig,ax_pr2=plt.subplots()
fig.suptitle('LiDAR SMN')
ax_pr2.set(xlabel='height', ylabel='meters')
ax_pr2.grid()
# ax_pr2.plot(lidar_bins*7.5,lidar_rc,'-',height_highres,pr2_mol*factor_adj,'-')
# ax_pr2.plot(lidar_bins*7.5,lidar_rc,'-',lidar_bins[:len(height_highres)]*7.5,pr2_mol*factor_adj,'-')
ax_pr2.plot(lidar_bins*7.5,lidar_rc,'g-',range_lidar,pr2_mol*factor_adj,'r-')

#xposition = [bin_init, bin_fin]
xposition = [5000, 8000] # meters

for xc in xposition:
  ax_pr2.axvline(x=xc, color='k', linestyle='--')

plt.show()