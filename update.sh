#!/usr/bin/bash

x=`cat kurt`

gotm=~/local/intel/19.2/gotm/5.3/bin/gotm

for y in $x; do

  echo
  echo "$y: "
  if [ -d $y ]; then
    cd $y
    make namelist >& /dev/null
    if [ $? -eq 0 ]; then
      echo 'namelists generated'
      $gotm --read_nml --write_yaml gotm.yaml >& /dev/null
      if [ $? -eq 0 ]; then
        echo 'gotm.yaml generated'
#        $gotm >& gotm.log
      else
        echo "failed to generate gotm.yaml"
      fi
      git rm -f --ignore-unmatch  *.nml
    else
      echo "failed to generate namelists"
    fi
    rm *.nml
    cd ..
  else
    echo "setup has been moved"
  fi
done
