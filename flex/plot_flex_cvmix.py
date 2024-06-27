import os
import numpy as np
import xarray as xr
from scipy.io import netcdf_file
import matplotlib.pyplot as plt

# define a function to load data into xarray.DataArray
def load_data(filename, **kwargs):
    # load z and zi
    with netcdf_file(filename, 'r', mmap=False) as ncfile:
        nc_z  = ncfile.variables['z']
        nc_zi = ncfile.variables['zi']
        z = xr.DataArray(
                nc_z[0,:,0,0],
                dims=('z'),
                coords={'z': nc_z[0,:,0,0]},
                attrs={'long_name': nc_z.long_name.decode(), 'units': nc_z.units.decode()}
                )
        zi = xr.DataArray(
                nc_zi[0,:,0,0],
                dims=('zi'),
                coords={'zi': nc_zi[0,:,0,0]},
                attrs={'long_name': nc_zi.long_name.decode(), 'units': nc_zi.units.decode()}
                )
    # load other variables
    out = xr.load_dataset(
            filename,
            drop_variables=['z', 'zi'],
            **kwargs,
            )
    out = out.assign_coords({
        'z': z,
        'zi': zi,
        })
    out = out.assign_coords({
        'z_2d': (('time', 'z'), nc_z[:,:,0,0]),
        'zi_2d': (('time', 'zi'), nc_zi[:,:,0,0]),
        })
    for var in out.data_vars:
        if 'z' in out.data_vars[var].dims:
            out.data_vars[var].assign_coords({'z':z})
        elif 'zi' in out.data_vars[var].dims:
            out.data_vars[var].assign_coords({'zi':zi})
    # return a reorderd view
    return out.transpose('z', 'zi', 'time', 'lon', 'lat')

# read the data
filename1 = os.path.join('flex.nc')
filename2 = os.path.join('flex_cvmix.nc')
ds_gotm1 = load_data(filename1)
ds_gotm2 = load_data(filename2)


# plot temperature profile
fig, axarr = plt.subplots(3, sharex='col')
fig.set_size_inches([8,6])

ax = axarr[0]
levels = np.linspace(6.0,9.6,37)
ds_gotm1.data_vars['temp_obs'].plot(ax=ax, levels=levels, add_colorbar=False)

ax = axarr[1]
im =ds_gotm1.data_vars['temp'].plot(ax=ax, levels=levels, add_colorbar=False)

ax = axarr[2]
ds_gotm2.data_vars['temp'].plot(ax=ax, levels=levels, add_colorbar=False)

labels = ['(a) Observation', '(b) $k$-$\epsilon$', '(c) CVMix']

for i, ax in enumerate(axarr):
    ax.set_title('')
    ax.set_xlabel('')
    ax.set_ylabel('$z$ [m]')
    ax.text(0.03, 0.05, labels[i], transform=ax.transAxes, color='w', fontsize=11, va='bottom')

plt.subplots_adjust(top=0.97, bottom=0.1, right=0.86, left=0.1, hspace=0.1, wspace=0.1)
label_str = '$T$ [$^\circ$C]'
cax = plt.axes([0.8, 0.28, 0.1, 0.5])
cax.set_visible(False)
cb = plt.colorbar(im, ax=cax)
cb.formatter.set_powerlimits((-2, 2))
cb.update_ticks()
cb.set_label(label_str)

fig.savefig('flex_temp.png', dpi=300)


# plot velocity profile
fig, axarr = plt.subplots(2, sharex='col')
fig.set_size_inches([8,4])

levels = np.linspace(-0.6, 0.6, 41)
ax = axarr[0]
im =ds_gotm1.data_vars['u'].plot(ax=ax, levels=levels, add_colorbar=False)

ax = axarr[1]
ds_gotm2.data_vars['u'].plot(ax=ax, levels=levels, add_colorbar=False)

labels = ['(a) $k$-$\epsilon$', '(b) CVMix']

for i, ax in enumerate(axarr):
    ax.set_title('')
    ax.set_xlabel('')
    ax.set_ylabel('$z$ [m]')
    ax.text(0.03, 0.05, labels[i], transform=ax.transAxes, color='k', fontsize=11, va='bottom')

plt.subplots_adjust(top=0.97, bottom=0.1, right=0.86, left=0.1, hspace=0.1, wspace=0.1)
label_str = '$u$ [m s$^{-1}$]'
cax = plt.axes([0.8, 0.28, 0.1, 0.5])
cax.set_visible(False)
cb = plt.colorbar(im, ax=cax)
cb.formatter.set_powerlimits((-2, 2))
cb.update_ticks()
cb.set_label(label_str)

fig.savefig('flex_u.png', dpi=300)


fig, axarr = plt.subplots(2, sharex='col')
fig.set_size_inches([8,4])

levels = np.linspace(-1, 1, 41)
ax = axarr[0]
im =ds_gotm1.data_vars['v'].plot(ax=ax, levels=levels, add_colorbar=False)

ax = axarr[1]
ds_gotm2.data_vars['v'].plot(ax=ax, levels=levels, add_colorbar=False)

labels = ['(a) $k$-$\epsilon$', '(b) CVMix']

for i, ax in enumerate(axarr):
    ax.set_title('')
    ax.set_xlabel('')
    ax.set_ylabel('$z$ [m]')
    ax.text(0.03, 0.05, labels[i], transform=ax.transAxes, color='k', fontsize=11, va='bottom')

plt.subplots_adjust(top=0.97, bottom=0.1, right=0.86, left=0.1, hspace=0.1, wspace=0.1)
label_str = '$v$ [m s$^{-1}$]'
cax = plt.axes([0.8, 0.28, 0.1, 0.5])
cax.set_visible(False)
cb = plt.colorbar(im, ax=cax)
cb.formatter.set_powerlimits((-2, 2))
cb.update_ticks()
cb.set_label(label_str)

fig.savefig('flex_v.png', dpi=300)


# plot viscosity profile
fig, axarr = plt.subplots(2, sharex='col')
fig.set_size_inches([8,4])

levels = np.linspace(0,0.24,25)
ax = axarr[0]
im =ds_gotm1.data_vars['num'].plot(ax=ax, levels=levels, add_colorbar=False)

ax = axarr[1]
ds_gotm2.data_vars['num'].plot(ax=ax, levels=levels, add_colorbar=False)

labels = ['(a) $k$-$\epsilon$', '(b) CVMix']

for i, ax in enumerate(axarr):
    ax.set_title('')
    ax.set_xlabel('')
    ax.set_ylabel('$z$ [m]')
    ax.text(0.03, 0.05, labels[i], transform=ax.transAxes, color='w', fontsize=11, va='bottom')

plt.subplots_adjust(top=0.97, bottom=0.1, right=0.86, left=0.1, hspace=0.1, wspace=0.1)
label_str = '$\\nu_m$ [m$^2$ s$^{-1}$]'
cax = plt.axes([0.8, 0.28, 0.1, 0.5])
cax.set_visible(False)
cb = plt.colorbar(im, ax=cax)
cb.formatter.set_powerlimits((-2, 2))
cb.update_ticks()
cb.set_label(label_str)

fig.savefig('flex_num.png', dpi=300)


# plot diffusivity profile
fig, axarr = plt.subplots(2, sharex='col')
fig.set_size_inches([8,4])

levels = np.linspace(0,0.27,28)
ax = axarr[0]
im =ds_gotm1.data_vars['nuh'].plot(ax=ax, levels=levels, add_colorbar=False)

ax = axarr[1]
ds_gotm2.data_vars['nuh'].plot(ax=ax, levels=levels, add_colorbar=False)

labels = ['(a) $k$-$\epsilon$', '(b) CVMix']

for i, ax in enumerate(axarr):
    ax.set_title('')
    ax.set_xlabel('')
    ax.set_ylabel('$z$ [m]')
    ax.text(0.03, 0.05, labels[i], transform=ax.transAxes, color='w', fontsize=11, va='bottom')

plt.subplots_adjust(top=0.97, bottom=0.1, right=0.86, left=0.1, hspace=0.1, wspace=0.1)
label_str = '$\\nu_h$ [m$^2$ s$^{-1}$]'
cax = plt.axes([0.8, 0.28, 0.1, 0.5])
cax.set_visible(False)
cb = plt.colorbar(im, ax=cax)
cb.formatter.set_powerlimits((-2, 2))
cb.update_ticks()
cb.set_label(label_str)

fig.savefig('flex_nuh.png', dpi=300)
