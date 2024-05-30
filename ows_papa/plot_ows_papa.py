#! /usr/bin/env python
# encoding: utf-8

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec

if __name__  == '__main__':

  NC = netCDF4.Dataset('ows_papa.nc')

  TIME = NC.variables['time']
  time = TIME[:]
  h    = NC.variables['h'   ][:]
  temp = NC.variables['temp'][:]

  temp_obs_name = ''
  varname = 'tprof'
  if varname in NC.variables:
    temp_obs_name = varname
  varname = 'temp_obs'
  if varname in NC.variables:
    temp_obs_name = varname
  if temp_obs_name is not '':
    temp_obs = NC.variables[temp_obs_name][:]
    
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
  figsize=(figwidth,figwidth/golden_ratio) # golden_ratio landscape format
  fig, ax = plt.subplots(2, 1, sharex='col', sharey='all', squeeze=False, figsize=figsize)
  modAxes = ax[0,0]
  obsAxes = ax[1,0]

  fig.autofmt_xdate()

  vmin = min( temp.min() , temp_obs.min() )
  vmax = max( temp.max() , temp_obs.max() )

  qm = modAxes.pcolormesh(datex2d,zx[...,j,i],temp    [1:-1,:,j,i],vmin=vmin,vmax=vmax)
  qm = obsAxes.pcolormesh(datex2d,zx[...,j,i],temp_obs[1:-1,:,j,i],vmin=vmin,vmax=vmax)
  cb = plt.colorbar(qm,ax=ax.ravel().tolist())

  modAxes.set_ylim((zi.min(),zi.max()))
  modAxes.set_ylabel('z [m]')
  obsAxes.set_ylabel('z [m]')
  cb.set_label('temperature [degC]')

  modAxes.text(0.95,0.1,'model'      ,transform=modAxes.transAxes,va='bottom',ha='right',bbox={'edgecolor':'0.0','facecolor':'None','boxstyle':'round'})
  obsAxes.text(0.95,0.1,'observation',transform=obsAxes.transAxes,va='bottom',ha='right',bbox={'edgecolor':'0.0','facecolor':'None','boxstyle':'round'})

  fig.savefig('ows_papa.png',dpi=300)
