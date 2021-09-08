import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import constants
from scipy import integrate
from scipy.interpolate import interp1d

# Current surface atmospheric conditions
SURFACE_TEMP = 300 # [K] 27C
SURFACE_PRESS = 1024 # [hPa]

#----------
#  LiDAR
#----------
  
# load data
LIDAR_FILE='./analog_dia_20mV.txt'
data_csv = pd.read_csv(LIDAR_FILE,sep='\n',header=None)

lidar_signal = np.array(data_csv[0])
number_bins = len(data_csv[0])

lidar_bins = np.arange(0, number_bins, 1)


# LiDAR signal range correction since bin number 1000
BIN_RC_THRESHOLD=1000
height = np.arange(0, number_bins, 1)
lidar_bias = np.mean(lidar_signal[BIN_RC_THRESHOLD:])
lidar_rc = (lidar_signal - lidar_bias)*(height**2)

#----------
#  MODEL
#----------

# load data
MODEL_FILE='./US-StdA_DB_CEILAP.csv'
data_csv = pd.read_csv(MODEL_FILE,sep=',',header=None)

index_AMSL = 2 # Height above mean sea level (AMSL)

height_lowres=np.array(data_csv[0][index_AMSL:])
temp_lowres=np.array(data_csv[1][index_AMSL:])
press_lowres=np.array(data_csv[2][index_AMSL:])

# Height high resolution
# NUM_BINS=4096
NUM_BINS=4000
height_highres = np.linspace(height_lowres[index_AMSL], NUM_BINS*7.5, num=NUM_BINS, endpoint=True)
height_lowres[-1] = height_highres[-1]

# Interpolation Spline 1D
temp_spline = interp1d(height_lowres, temp_lowres, kind='cubic')
temp_highres = temp_spline(height_highres)

press_spline = interp1d(height_lowres, press_lowres, kind='cubic')
press_highres = press_spline(height_highres)

# Scaling the temperature and pressure profiles in the model
# with current surface conditions
temp_highres = SURFACE_TEMP * (temp_highres/temp_highres[0])
press_highres = SURFACE_PRESS * (press_highres/press_highres[0])

# alpha y beta
kboltz=constants.k
nmol = (100*press_highres)/(temp_highres*kboltz)
wave_length = 532 #nm
beta_mol = nmol * (550/wave_length)**4.09 * 5.45 * (10**-32)
alpha_mol = beta_mol * (8*np.pi/3)
cumtrapz = integrate.cumtrapz(alpha_mol, height_highres, initial=0)
tm2r_mol = np.exp(-2*cumtrapz)
pr2_mol = beta_mol*tm2r_mol


#----------
#   ECM
#----------
bin_init = int(1500/7.5) # 2500m / 7.5m
bin_fin = int(3750/7.5) # 3200m / 7.5m
# bin_init = 200
# bin_fin = 500

print(lidar_rc[bin_init])
print(lidar_rc[bin_fin+1])

mNum = np.dot(lidar_rc[bin_init:bin_fin+1],pr2_mol[bin_init:bin_fin+1])
mDen = np.dot(pr2_mol[bin_init:bin_fin+1],pr2_mol[bin_init:bin_fin+1])

m = mNum/mDen

print("ECM:",np.format_float_scientific(m))
# sig == lidar_rc
# sigmol == pr2_mol

# for ( i=fitParam.indxInicFit:fitParam.indxEndFit )
#       mNum = mNum + sig   (i)*sigMol(i) ;
#       mDen = mDen + sigMol(i)*sigMol(i) ;
#     endfor
#     m = mNum/mDen ;

#----------
#  PLOT
#----------
factor_adj=m

fig,ax_pr2=plt.subplots()
fig.suptitle('LiDAR SMN')
ax_pr2.set(xlabel='height', ylabel='meters')
ax_pr2.grid()
# ax_pr2.plot(height_highres,lidar_rc,'-',height_highres,pr2_mol*factor_adj,'-')
ax_pr2.plot(lidar_bins,lidar_rc,'-',lidar_bins,pr2_mol*factor_adj,'-')

xposition = [bin_init, bin_fin]
for xc in xposition:
  ax_pr2.axvline(x=xc, color='k', linestyle='--')

plt.show()