#!/usr/bin/env python

# This script converts the NEMO asics-MED test case into gotm input format
# the NEMO test case is here
#https://forge.nemo-ocean.eu/nemo/nemo/-/blob/branch_5.0/cfgs/C1D/EXP_ASICS/namelist_cfg?ref_type=heads
# and the forcing files are here
# https://gws-access.jasmin.ac.uk/public/nemo/sette_inputs/r5.0.0/C1D_v5.0.1.tar.gz


import numpy as np
import matplotlib.pyplot as plt
from scipy.io import netcdf_file
from datetime import datetime, timedelta

plt.ion()

file1 = 'forc_ASICS_y2013.nc'
file2 = 'init_ASICS_m01d15.nc'
file3 = 'profils_Lion_2013_0115_0325_L75.nc'

flag_forcing = 1 #0: no forcing, 1: use all forcins

f1 = netcdf_file(file1,'r')
taux2 = f1.variables['TAUX2'][:].copy().squeeze()
tauy2 = f1.variables['TAUY2'][:].copy().squeeze()
fnet2 = f1.variables['FNET2'][:].copy().squeeze()
fsol2 = f1.variables['FSOL2'][:].copy().squeeze()
emp2  = f1.variables['EMP2' ][:].copy().squeeze()
f1.close()

n_rec = len(taux2)

# adjust EMP unit to m/s, and add minus sign (GOTM needs net precips)
# TODO: DOUBLE CHECK HERE:
# GOTM SHOULD ACCEPT PRECIP WITH UNITS M/S

# in theory, NEMO should be kg/m2/s but there is a mistake (see Mail by
# G. Samson) and it seems that EMP2 is already in m/s

precip = -1000*emp2

# adjust solar heat flux to have only positive values
fsol2 = np.where(fsol2>0., fsol2, 0.)

# remove solar from fnet2
qturb = fnet2 - fsol2


if flag_forcing == 0:
  taux2 *= 0.
  tauy2 *= 0.
  fnet2 *= 0.
  fsol2 *= 0.
  qturb *= 0.
  precip *= 0.

t0 = datetime.fromisoformat('2013-01-01 00:00:00')
dt = timedelta(hours=1)

date_list = [t0 + nr*dt for nr in range(n_rec)]

with open('meteo_asics.dat', 'w') as fout:
  for i in range(0,n_rec):
    fout.write(f'{date_list[i]} \t {taux2[i]:.7f} \t  {tauy2[i]:.7f} \t  {qturb[i]:.7f} \t  {fsol2[i]:.7f} \t  {precip[i]:.7e} \n')



# ---------- Read initial conditions ------------

f2 = netcdf_file(file2,'r')
temp0 = f2.variables['votemper'][:].copy().squeeze()
salt0 = f2.variables['vosaline'][:].copy().squeeze()
zt    = f2.variables['deptht'][:].copy().squeeze()
f2.close()

# read full time series to correct salinity issue
f3 = netcdf_file(file3,'r')
temp = f3.variables['votemper'][:].copy().squeeze()
salt = f3.variables['vosaline'][:].copy().squeeze()
f3.close()

si_z = len(zt)

dz = np.zeros(si_z)
zi = np.zeros(si_z)

dz[0] = 2*zt[0]
zi[0] = 2*zt[0]

for iz in range(1,si_z):
  dz[iz] = 2*(zt[iz] - zi[iz-1])
  zi[iz] = zi[iz-1] + dz[iz]

# do not keep bottom layers
izmax = 56
dz_gotm = np.abs(dz[:izmax])
temp_gotm = temp0[:izmax]
salt_gotm = salt0[:izmax]

si_z_gotm = len(dz_gotm)



# trying to correct the "anomaly" near idx_z = 48
# assume the proile at idx_time=65 should be perfectly mixed

salt_ref = salt[65,:izmax]
temp_ref = temp[65,:izmax]
# assume upper sensors are accurate
salt_ref = salt_ref - salt_ref[0]

# remove anomaly
salt_gotm = salt_gotm - salt_ref

with open('grid_z.dat', 'w') as fout:
  fout.write(f'{si_z_gotm}\n')
  for i in range(0,si_z_gotm):
    fout.write(f'{dz_gotm[i]} \t {temp_gotm[i]} \t  {salt_gotm[i]} \n')



with open('init_ts_asics.dat', 'w') as fout:
  fout.write(f'2013/01/15 00:00:00  {si_z_gotm} 3 \n')
  for i in range(0,si_z_gotm):
    fout.write(f'{-zt[i]} \t {temp_gotm[i]} \t  {salt_gotm[i]} \n')

print(f'depth= {np.sum(dz_gotm)}')
