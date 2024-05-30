#! /usr/bin/env python
# encoding: utf-8

import netCDF4
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime


if __name__  == '__main__':

  NC = netCDF4.Dataset('liverpool_bay.nc')

  TIME = NC.variables['time']
  startdate = datetime.datetime(1999, 7, 5, 16, 30)
  stopdate  = datetime.datetime(1999, 7, 6, 17, 00)
  nstart = netCDF4.date2index( startdate, TIME, select='nearest')
  nstop  = netCDF4.date2index( stopdate , TIME, select='nearest')


  time    = TIME                   [nstart:nstop+1,...]
  h       = NC.variables['h'      ][nstart:nstop+1,...]
  u       = NC.variables['u'      ][nstart:nstop+1,...]
  u_obs   = NC.variables['u_obs'  ][nstart:nstop+1,...]
  v       = NC.variables['v'      ][nstart:nstop+1,...]
  v_obs   = NC.variables['v_obs'  ][nstart:nstop+1,...]
  eps     = NC.variables['eps'    ][nstart:nstop+1,...]
  eps_obs = NC.variables['eps_obs'][nstart:nstop+1,...]
  temp    = NC.variables['temp'   ][nstart:nstop+1,...]
  salt    = NC.variables['salt'   ][nstart:nstop+1,...]
  temp_obs_name = ''
  varname = 'tprof'
  if varname in NC.variables:
    temp_obs_name = varname
  varname = 'temp_obs'
  if varname in NC.variables:
    temp_obs_name = varname
  if temp_obs_name is not '':
    temp_obs = NC.variables[temp_obs_name][nstart:nstop+1,...]
  salt_obs_name = ''
  varname = 'sprof'
  if varname in NC.variables:
    salt_obs_name = varname
  varname = 'salt_obs'
  if varname in NC.variables:
    salt_obs_name = varname
  if salt_obs_name is not '':
    salt_obs = NC.variables[salt_obs_name][nstart:nstop+1,...]

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
  figsize=(figwidth,figwidth*golden_ratio) # golden_ratio portrait format
  fig, ax = plt.subplots(5, 2, sharex='all', sharey='all', squeeze=False, figsize=figsize)
  fig.autofmt_xdate()

  vmin = min( temp.min() , temp_obs.min() )
  vmax = max( temp.max() , temp_obs.max() )
  axes = ax[0,0]
  qm = axes.pcolormesh(datex2d,zx[...,j,i],temp_obs[1:-1,:,j,i],vmin=vmin,vmax=vmax)
  axes.set_ylabel('z [m]')
  axes = ax[0,1]
  qm = axes.pcolormesh(datex2d,zx[...,j,i],temp    [1:-1,:,j,i],vmin=vmin,vmax=vmax)
  cb = plt.colorbar(qm,ax=(ax[0,0],ax[0,1]))
  cb.set_label('temp [degC]')

  vmin = min( salt.min() , salt_obs.min() )
  vmax = max( salt.max() , salt_obs.max() )
  axes = ax[1,0]
  qm = axes.pcolormesh(datex2d,zx[...,j,i],salt_obs[1:-1,:,j,i],vmin=vmin,vmax=vmax)
  axes.set_ylabel('z [m]')
  axes = ax[1,1]
  qm = axes.pcolormesh(datex2d,zx[...,j,i],salt    [1:-1,:,j,i],vmin=vmin,vmax=vmax)
  cb = plt.colorbar(qm,ax=(ax[1,0],ax[1,1]))
  cb.set_label('salt')

  vmax = max( abs(u.min()) , abs(u_obs.min()) , abs(u.max()) , abs(u_obs.max()) )
  vmin = -vmax
  axes = ax[2,0]
  qm = axes.pcolormesh(datex2d,zx[...,j,i],u_obs[1:-1,:,j,i],cmap='seismic',vmin=vmin,vmax=vmax)
  axes.set_ylabel('z [m]')
  axes = ax[2,1]
  qm = axes.pcolormesh(datex2d,zx[...,j,i],u    [1:-1,:,j,i],cmap='seismic',vmin=vmin,vmax=vmax)
  cb = plt.colorbar(qm,ax=(ax[2,0],ax[2,1]))
  cb.set_label('u [m/s]')

  vmax = max( abs(v.min()) , abs(v_obs.min()) , abs(v.max()) , abs(v_obs.max()) )
  vmin = -vmax
  axes = ax[3,0]
  qm = axes.pcolormesh(datex2d,zx[...,j,i],v_obs[1:-1,:,j,i],cmap='seismic',vmin=vmin,vmax=vmax)
  axes.set_ylabel('z [m]')
  axes = ax[3,1]
  qm = axes.pcolormesh(datex2d,zx[...,j,i],v    [1:-1,:,j,i],cmap='seismic',vmin=vmin,vmax=vmax)
  cb = plt.colorbar(qm,ax=(ax[3,0],ax[3,1]))
  cb.set_label('v [m/s]')

  vmin = max( 1e-9 , min( eps.min() , eps_obs.min() ) )
  vmax = max( eps.max() , eps_obs.max() )
  axes = ax[4,0]
  qm = axes.pcolormesh(datex2d,zx[...,j,i],eps_obs[1:-1,:,j,i],cmap='hot_r',norm=mpl.colors.LogNorm(vmin=vmin,vmax=vmax))
  axes.set_ylabel('z [m]')
  axes = ax[4,1]
  qm = axes.pcolormesh(datex2d,zx[...,j,i],eps    [1:-1,:,j,i],cmap='hot_r',norm=mpl.colors.LogNorm(vmin=vmin,vmax=vmax))
  cb = plt.colorbar(qm,ax=(ax[4,0],ax[4,1]))
  cb.set_label('dissipation [m2/s3]')

  axes.set_ylim((zi.min(),zi.max()))
  ax[0,0].set_title('observation')
  ax[0,1].set_title('model'      )
  plt.draw()
  axes.xaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
  fig.savefig('liverpool_bay.png',dpi=300)
