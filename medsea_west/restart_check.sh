#!/bin/bash

fabm_calc=False

make namelist restart_offline=False fabm_calc=$fabm_calc
gotm >& gotm_1.log
mv restart.nc restart_1.nc
mv WMED1D_annual_daily.nc WMED1D_annual_daily_1.nc

make namelist restart_offline=False stop="1996-07-01 00:00:00" fabm_calc=$fabm_calc
gotm >& gotm_2a.log
cp restart.nc  restart_2a.nc 
mv WMED1D_annual_daily.nc WMED1D_annual_daily_2a.nc

make namelist restart_offline=True start="1996-07-01 00:00:00" fabm_calc=$fabm_calc restart_allow_missing_variable=False
gotm >& gotm_2b.log
mv restart.nc  restart_2b.nc 
mv WMED1D_annual_daily.nc WMED1D_annual_daily_2b.nc

md5sum restart_1.nc restart_2b.nc

