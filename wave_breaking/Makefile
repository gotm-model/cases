#
# Makefile for 'waves_breaking' setup.
# targets are:
#    run_all
#    prescribed kepsilon komega generic: to run model

name	= wave_breaking
setup	= $(name)

include ../Rules.make

all:
	@echo
	@echo "usage: make run_all|namelists|<turbulence model - eg. kepsilon>
	@echo

run_all: generic kepsilon komega prescribed clean

generic kepsilon komega prescribed: 
	@echo
	@echo "Generating input files for: "$@
	@echo
	ln -sf $@.xml $(setup).xml && $(MAKE) namelist && $(MAKE) run && mv $(name).nc $@.nc && mv log.$(name) log.$@.$(name)

$(name)_clean:
	$(RM) $(name).xml
	$(RM) generic.nc kepsilon.nc komega.nc prescribed.nc
	$(RM) log.*.$(name)

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#-----------------------------------------------------------------------
