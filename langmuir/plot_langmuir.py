
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
filename1 = 'langmuir.nc'
filename2 = 'langmuir.cvmix.lf17.nc'
ds_gotm1 = load_data(filename1)
ds_gotm2 = load_data(filename2)


# plot surface forcing
fig, axarr = plt.subplots(4,sharex='col')
fig.set_size_inches([7,8])

ax = axarr[0]
hflux = ds_gotm1.data_vars['heat'] + ds_gotm1.data_vars['I_0']
hflux.plot(ax=ax, color='gray', linewidth=1)
hflux.rolling(time=40, center=True).mean().plot(
    ax=ax, color='k', linewidth=1.5)
ax.set_ylim([-300, 600])
ax.axhline(0.0, color='k', linestyle=':', linewidth=0.75)

ax = axarr[1]
rho_w = 1027.0
pme = ds_gotm1.data_vars['precip'] * rho_w * 1e6 # m/s -> mg/m^2/s
pme.plot(ax=ax, color='gray', linewidth=1)
pme.rolling(time=40, center=True).mean().plot(
    ax=ax, color='k', linewidth=1.5)
ax.set_ylim([-100, 150])
ax.axhline(0.0, color='k', linestyle=':', linewidth=0.75)

ax = axarr[2]
ustar = ds_gotm1.data_vars['u_taus']
ustar.plot(ax=ax, color='gray', linewidth=1)
ustar.rolling(time=40, center=True).mean().plot(
    ax=ax, color='k', linewidth=1.5)

ax = axarr[3]
laturb = ds_gotm2.data_vars['La_Turb']
laturb = laturb.where(laturb < 1.e3, drop=True)
laturb.plot(ax=ax, color='gray', linewidth=1)
laturb.rolling(time=40, center=True).mean().plot(
    ax=ax, color='k', linewidth=1.5)
ax.set_ylim([0.1,0.7])
ax.axhline(0.3, color='k', linestyle=':', linewidth=0.75)

ylabels = ['$Q_0$ [W m$^{-2}$]', '$F_0$ [mg m$^{-2}$ s$^{-1}$]', '$u^*$ [m s$^{-1}$]', 'La$_t$']

for i, ax in enumerate(axarr):
    ax.set_title('')
    ax.set_xlabel('')
    ax.set_ylabel(ylabels[i])
    ax.set_xlim([np.datetime64('2012-03-21'), np.datetime64('2013-03-21')])

plt.tight_layout()
fig.savefig('langmuir-forcing.png', dpi=300)


# plot temperature profile
fig, axarr = plt.subplots(3,sharex='col')
fig.set_size_inches([8,6])

ax = axarr[0]
levels = np.linspace(5,17,41)
ds_gotm1.data_vars['temp_obs'].plot(ax=ax, levels=levels, add_colorbar=False)

ax = axarr[1]
im =ds_gotm1.data_vars['temp'].plot(ax=ax, levels=levels, add_colorbar=False)

ax = axarr[2]
ds_gotm2.data_vars['temp'].plot(ax=ax, levels=levels, add_colorbar=False)

labels = ['(a) Observation', '(b) KC04', '(c) LF17']

for i, ax in enumerate(axarr):
    ax.set_title('')
    ax.set_xlabel('')
    ax.set_ylabel('$z$ [m]')
    ax.set_xlim([np.datetime64('2012-03-21'), np.datetime64('2013-03-21')])
    ax.text(0.03, 0.05, labels[i], transform=ax.transAxes, color='w', fontsize=11, va='bottom')

plt.subplots_adjust(top=0.97, bottom=0.1, right=0.86, left=0.1, hspace=0.1, wspace=0.1)
label_str = '$T$ [$^\circ$C]'
cax = plt.axes([0.8, 0.28, 0.1, 0.5])
cax.set_visible(False)
cb = plt.colorbar(im, ax=cax)
cb.formatter.set_powerlimits((-2, 2))
cb.update_ticks()
cb.set_label(label_str)

fig.savefig('langmuir.png', dpi=300)
