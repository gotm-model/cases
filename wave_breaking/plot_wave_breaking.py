# written by Lars Umlauf (IOW)
# questions to gotm-users@googlegroups.com

# load required packages
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

# model parameters (have to correspond to content of your yaml file)
# surface forcing
us2      = 0.001              # surface friction velocity (squared)
z0       = 0.5                # surface roughness length

# k-omega model parameters (written to screen by GOTM)
alpha   = -2.529
L       = 0.25
cmu     = 0.5477

# GLS model (uncomment if you use gotm.gls.yaml)
#alpha   = -2.0
#L       = 0.2
#cmu     = 0.5477

file    = 'wave_breaking.nc'
data    = nc.Dataset(file)

# load variables from netCDF
z       = data.variables['z'][:, :, 0, 0]
zi      = data.variables['zi'][:, :, 0, 0]
t       = data.variables['time'][:]
u       = data.variables['u'][:, :, 0, 0]
k       = data.variables['tke'][:, :, 0, 0]
l       = data.variables['L'][:, :, 0, 0]
num     = data.variables['num'][:, :, 0, 0]

# plot all following profiles at this time index
NT      = t.size
iPlt    = NT-1

# water depth
H       = - zi[iPlt,0]

# theoretical profiles for TKE injection by breaking waves (see Umlauf and Burchard, 2003)
d       = np.abs(z[iPlt,:])
di      = np.abs(zi[iPlt,:])

K       = k[iPlt,-2] * (di[-2] + z0)**(-alpha)
U       = u[iPlt,-1] -  2*us2/(alpha*cmu*K**0.5*L)*(d[-1] + z0)**(-0.5*alpha)

u_th    = U + 2*us2/(alpha*cmu*K**0.5*L)*(d + z0 )**(-0.5*alpha)
k_th    = K*(di + z0 )**alpha
l_th    = L*(di + z0 )

zMin    = -3.


# plot vertical profiles at time index iPlt
fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(7, 10))
plt.subplots_adjust(hspace=0.5)

bprops = {'facecolor': 'white','edgecolor': 'none', 'pad': 2}     # text label box properties

ax1.plot(u[iPlt, :], z[iPlt, :], label='GOTM')
ax1.plot(u_th, z[iPlt, :], '--', label=r'$u=\frac{2 u_*^2}{\alpha c_\mu K^\frac{1}{2} L} (|z|+z0)^{-\frac{\alpha}{2}}$ + C')
ax1.set_xlabel('$u$ [m s$^{-1}$]',fontsize=14)
ax1.set_ylabel('z [m]',fontsize=14)
ax1.set_xlim([0, 1])
ax1.set_ylim([zMin, 0])
ax1.legend(loc='upper left')
ax1.text(0.97, 0.2, 'A',verticalalignment='top',horizontalalignment='right',
         transform=ax1.transAxes,fontsize=16,bbox=bprops)
ax1.tick_params(labelsize=14)


ax2.plot(k[iPlt, :], zi[iPlt, :], label='GOTM')
ax2.plot(k_th, zi[iPlt, :], '--', label = r'$k = K (|z| + z_0)^\alpha$')
ax2.set_xlabel(r'$k$ [m$^2$ s$^{-2}$]',fontsize=14)
ax2.set_ylabel('z [m]',fontsize=14)
ax2.set_ylim([zMin, 0])
ax2.legend(loc='center')
ax2.text(0.97, 0.2, 'B',verticalalignment='top',horizontalalignment='right',
         transform=ax2.transAxes,fontsize=16,bbox=bprops)
ax2.tick_params(labelsize=14)


ax3.plot(l[iPlt, :], zi[iPlt, :], label = 'GOTM')
ax3.plot(l_th, zi[iPlt, :],'--', label = r'$l = L (|z| + z_0)$')
ax3.set_xlabel(r'$l$ [m]',fontsize=14)
ax3.set_ylabel('z [m]',fontsize=14)
ax3.set_xlim([0,1.5])
ax3.set_ylim([zMin, 0])
ax3.legend(loc='lower left')
ax3.text(0.97, 0.2, 'C',verticalalignment='top',horizontalalignment='right',
         transform=ax3.transAxes,fontsize=16,bbox=bprops)
ax3.tick_params(labelsize=14)

plt.savefig('wave_breaking.png')
plt.show()

