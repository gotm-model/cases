#! /usr/bin/env python
# encoding: utf-8

import netCDF4
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec

if __name__  == '__main__':

  NC = netCDF4.Dataset('gotland.nc')

  TIME = NC.variables['time']
  time = TIME[:]
  h    = NC.variables['h'   ][:]
  temp = NC.variables['temp'][:]
  salt = NC.variables['salt'][:]

  no3_name = 'iow_ergom_t_no3'
  o2_name  = 'iow_ergom_t_o2'

  nax = 1
  if no3_name in NC.variables:
    no3 = NC.variables[no3_name][:]
    nax += 1
  if o2_name in NC.variables:
    o2 = NC.variables[o2_name][:]
    nax += 1
    
  N, K, J, I = temp.shape

  zi = np.insert(h, 0, 0.0, axis=1)
  zi = zi.cumsum(axis=1)
  # broadcasting does not work with "-=" !!!
  zi = zi - zi[0, -1, ...]

  i = j = 0

  zc = 0.5 * ( zi[:,:-1,...] + zi[:,1:,...] )

  time2d = np.expand_dims(time, 1)
  time2d = time2d.repeat(K, axis=1)
  date2d = netCDF4.netcdftime.utime(TIME.units).num2date(time2d)


  # temporal avg. positions
  timex = 0.5 * ( time[:-1     ] + time[1:     ] )
  zx    = 0.5 * ( zi  [:-1, ...] + zi  [1:, ...] )

  timex2d = np.expand_dims(timex, 1)
  timex2d = timex2d.repeat(K+1, axis=1)
  datex2d = netCDF4.netcdftime.utime(TIME.units).num2date(timex2d)

  golden_ratio = (1.+np.sqrt(5.))/2.
  figwidth=7.48 # 3.54 (Elsevier 2-columnwidth), 7.48 (Elsevier 1-columnwidth)
  figsize=(figwidth,figwidth/golden_ratio*nax/3) # golden_ratio landscape format
  fig, ax = plt.subplots(nax, 1, sharex='col', sharey='all', squeeze=False, figsize=figsize)
  fig.autofmt_xdate()

  axes = ax[0,0]
  qm = axes.pcolormesh(datex2d,zx[...,j,i],temp[1:-1,:,j,i])
  cb = plt.colorbar(qm,ax=axes)
  cb.locator = mpl.ticker.MaxNLocator(5)
  cb.update_ticks()
  cs = axes.contour(date2d,zc[...,j,i],salt[...,j,i],(8.,10.,12.),colors='k')
  cs.clabel(fmt='%1.f')
  axes.set_ylim((zi.min(),zi.max()))
  axes.set_ylabel('z [m]')
  cb.set_label('temp [degC]')

  nax = 1
  if no3_name in NC.variables:
    axes = ax[nax,0]
    qm = axes.pcolormesh(datex2d,zx[...,j,i],no3[1:-1,:,j,i])
    cb = plt.colorbar(qm,ax=axes,format='%.1e')
    cb.locator = mpl.ticker.MaxNLocator(5)
    cb.update_ticks()
    axes.set_ylim((zi.min(),zi.max()))
    axes.set_ylabel('z [m]')
    cb.set_label('no3 [mol/kg]')
    nax += 1
  if o2_name in NC.variables:
    axes = ax[nax,0]
    qm = axes.pcolormesh(datex2d,zx[...,j,i],o2[1:-1,:,j,i])
    cb = plt.colorbar(qm,ax=axes,format='%.1e')
    cb.locator = mpl.ticker.MaxNLocator(5)
    cb.update_ticks()
    axes.set_ylim((zi.min(),zi.max()))
    axes.set_ylabel('z [m]')
    cb.set_label('o2 [mol/kg]')
    nax += 1

  plt.tight_layout()
  fig.savefig('gotland.png',dpi=300)
