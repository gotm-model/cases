#
# Makefile for 'entrainment' setup.
# targets are:
#    run_all
#    kepsilon komega generic MellorYamada kpp: run model

name	= entrainment
setup	= $(name)

include ../Rules.make

all:
	@echo
	@echo "usage: make run_all|<turbulence model - eg. kepsilon>
	@echo

run_all: kepsilon komega generic MellorYamada kpp clean

kepsilon komega generic MellorYamada kpp:
	@echo
	@echo "Generating input files for: "$@
	@echo
	ln -sf $@.xml $(setup).xml && $(MAKE) namelist && $(MAKE) run && mv $(name).nc $@.nc && mv log.$(name) log.$@.$(name)


$(name)_clean:
	$(RM) $(name).xml
	$(RM) generic.nc kepsilon.nc komega.nc kpp.nc MellorYamada.nc
	$(RM) log.*.$(name)

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#-----------------------------------------------------------------------
