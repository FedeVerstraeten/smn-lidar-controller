import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import constants
from scipy import integrate
from scipy.interpolate import interp1d

# Current surface atmospheric conditions
SURFACE_TEMP = 300 # [K] 27C
SURFACE_PRESS = 1024 # [hPa]

# load data
LIDAR_FILE='./US-StdA_DB_CEILAP.csv'
data_csv = pd.read_csv(LIDAR_FILE,sep=',',header=None)

index_AMSL = 2 # Height above mean sea level (AMSL)

height_lowres=np.array(data_csv[0][index_AMSL:])
temp_lowres=np.array(data_csv[1][index_AMSL:])
press_lowres=np.array(data_csv[2][index_AMSL:])

# Height high resolution
NUM_BINS=4096
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

# Plot
fig1,(ax_temp,ax_pres)=plt.subplots(2)

fig1.suptitle('LiDAR SMN')
ax_temp.set(xlabel='Height', ylabel='Temperature [K]')
ax_pres.set(xlabel='Height', ylabel='Pressure [hPa]')
ax_temp.grid()
ax_pres.grid()
ax_temp.plot(height_lowres,temp_lowres,'o',height_highres,temp_highres,'-')
ax_pres.plot(height_lowres,press_lowres,'o',height_highres,press_highres,'-')

# Plot PR2 Mol
fig2,ax_pr2=plt.subplots()
ax_pr2.set(xlabel='Height', ylabel='Pr2')
ax_pr2.grid()
ax_pr2.plot(height_highres,pr2_mol,'-')


plt.show()