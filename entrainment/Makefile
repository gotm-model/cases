#
# Makefile for 'entrainment' setup.
# targets are:
#    generic kepsilon komega MellorYamada: run model

name	= entrainment
setup	= $(name)

help:
	@echo
	@echo "usage: 'make kepsilon' to run k-epsilon model"  
	@echo "usage: 'make komega' to run k-omega model"  
	@echo "usage: 'make MellorYamada' to run Mellor-Yamada model"  
	@echo "usage: 'make generic' to run GLS model"  
	@echo

include ../Rules.make

kepsilon komega MellorYamada generic:
	@echo
	@echo "Generating input files for: "$@
	@echo
	ln -sf $@.xml $(setup).xml && $(MAKE) namelist && $(MAKE) run && mv $(name).nc $@.nc && mv log.$(name) log.$@.$(name)

$(name)_clean:
	$(RM) $(name).xml
	$(RM) kepsilon.nc komega.nc MellorYamada.nc generic.nc
	$(RM) log.*.$(name)


#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#-----------------------------------------------------------------------
