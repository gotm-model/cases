#! /usr/bin/env python
# encoding: utf-8

import netCDF4
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec

if __name__  == '__main__':

  NC = netCDF4.Dataset('nns_annual.nc')

  TIME = NC.variables['time']
  time = TIME[:]
  h    = NC.variables['h'   ][:]
  temp = NC.variables['temp'][:]

  nut_name = 'gotm_npzd_nut'
  phy_name = 'gotm_npzd_phy'
  zoo_name = 'gotm_npzd_zoo'
  det_name = 'gotm_npzd_det'

  nax = 1
  if nut_name in NC.variables:
    nut = NC.variables[nut_name][:]
    nax += 1
  if phy_name in NC.variables:
    phy = NC.variables[phy_name][:]
    nax += 1
  if zoo_name in NC.variables:
    zoo = NC.variables[zoo_name][:]
    nax += 1
  if det_name in NC.variables:
    det = NC.variables[det_name][:]
    nax += 1
    
  N, K, J, I = temp.shape

  zi = np.insert(h, 0, 0.0, axis=1)
  zi = zi.cumsum(axis=1)
  # broadcasting does not work with "-=" !!!
  zi = zi - zi[0, -1, ...]

  i = j = 0

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
  axes.set_ylim((zi.min(),zi.max()))
  axes.set_ylabel('z [m]')
  cb.set_label('temp [degC]')

  nax = 1
  if nut_name in NC.variables:
    axes = ax[nax,0]
    qm = axes.pcolormesh(datex2d,zx[...,j,i],nut[1:-1,:,j,i])
    cb = plt.colorbar(qm,ax=axes)
    cb.locator = mpl.ticker.MaxNLocator(5)
    cb.update_ticks()
    axes.set_ylim((zi.min(),zi.max()))
    axes.set_ylabel('z [m]')
    cb.set_label('nut [mmol/m3]')
    nax += 1
  if phy_name in NC.variables:
    axes = ax[nax,0]
    qm = axes.pcolormesh(datex2d,zx[...,j,i],phy[1:-1,:,j,i])
    cb = plt.colorbar(qm,ax=axes)
    cb.locator = mpl.ticker.MaxNLocator(5)
    cb.update_ticks()
    axes.set_ylim((zi.min(),zi.max()))
    axes.set_ylabel('z [m]')
    cb.set_label('phy [mmol/m3]')
    nax += 1
  if zoo_name in NC.variables:
    axes = ax[nax,0]
    qm = axes.pcolormesh(datex2d,zx[...,j,i],zoo[1:-1,:,j,i])
    cb = plt.colorbar(qm,ax=axes)
    cb.locator = mpl.ticker.MaxNLocator(5)
    cb.update_ticks()
    axes.set_ylim((zi.min(),zi.max()))
    axes.set_ylabel('z [m]')
    cb.set_label('zoo [mmol/m3]')
    nax += 1
  if det_name in NC.variables:
    axes = ax[nax,0]
    qm = axes.pcolormesh(datex2d,zx[...,j,i],det[1:-1,:,j,i])
    cb = plt.colorbar(qm,ax=axes)
    cb.locator = mpl.ticker.MaxNLocator(5)
    cb.update_ticks()
    axes.set_ylim((zi.min(),zi.max()))
    axes.set_ylabel('z [m]')
    cb.set_label('det [mmol/m3]')
    nax += 1

  plt.tight_layout()
  fig.savefig('nns_annual.png',dpi=300)
