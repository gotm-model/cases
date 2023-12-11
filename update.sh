#!/usr/bin/bash

setups="estuary"
setups="black_sea"
setups="channel"
setups="nns_annual"
setups="blacksea channel couette entrainment estuary flex gotland lago_maggiore liverpool_bay medsea_east medsea_west nns_annual nns_seasonal ows_papa plume resolute reynolds rouse seagrass wave_breaking"


for s in $setups; do
   echo "SETUP: "$s
   cd $s
   git checkout gotm.yaml
   sed -i -e "s/-0.17         /2.00000000E-04/g" -e "s/0.78         /7.50000000E-04/g" gotm.yaml
   cp gotm.yaml gotm.yaml.org
   #python ~/source/repos/GOTM/code/scripts/python/update_setup.py --gotm ~/local/gcc/9/gotm/6/bin/gotm --detail default gotm.yaml
   /home/kb/local/gcc/12/gotm/7/bin/gotm gotm.yaml.org --ignore_unknown_config --write_yaml gotm.yaml
   cd ..
done





