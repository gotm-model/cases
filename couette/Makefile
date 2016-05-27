#
# Makefile for 'couette' setup.
# targets are:
#    run_all
#    kepsilon komega MellorYamada: run model

name	= couette
setup	= $(name)

help:
	@echo
	@echo "usage: 'make kepsilon' to run k-epsilon model"  
	@echo "usage: 'make komega' to run k-omega model"  
	@echo "usage: 'make MellorYamada' to run Mellor-Yamada model"  
	@echo

include ../Rules.make

kepsilon komega MellorYamada:
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
