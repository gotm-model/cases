#
# Makefile for 'channel' setup.
# targets are:
#    run_all
#    kepsilon komega MellorYamada: to run specific model

name	= channel
setup	= $(name)

include ../Rules.make

all:
	@echo
	@echo "usage: make run_all|namelists|<turbulence model - eg. kepsilon>
	@echo

run_all: kepsilon komega MellorYamada clean

kepsilon komega MellorYamada:
	@echo
	@echo "Generating input files for: "$@
	@echo
	ln -sf $@.xml $(setup).xml && $(MAKE) namelist && $(MAKE) run && mv $(name).nc $@.nc && mv log.$(name) log.$@.$(name)

$(name)_clean:
	$(RM) $(name).xml
	$(RM) kepsilon.nc komega.nc MellorYamada.nc
	$(RM) log.*.$(name)

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#-----------------------------------------------------------------------
