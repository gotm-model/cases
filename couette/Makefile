#
# Makefile for 'couette' setup.
# targets are:
#    namelists
#    run_all
#    kepsilon komega MellorYamada: to generate input files
#    for specific turbulence closure models (will be placed in
#    subdirectories)

name	= couette
setup	= $(name)

include ../Rules.make

all:
	@echo
	@echo "usage: make run_all|namelists|<turbulence model - eg. kepsilon>
	@echo

run_all: kepsilon komega MellorYamada clean


namelists: kepsilon_nml komega_nml MellorYamada_nml

scenarios:
	( $(MAKE) kepsilon_nml     ; $(MAKE) scenario ; mv ../couette.gotmscenario ../couette.kepsilon.gotmscenario     ; $(MAKE) clean)
	( $(MAKE) komega_nml       ; $(MAKE) scenario ; mv ../couette.gotmscenario ../couette.komega.gotmscenario       ; $(MAKE) clean)
	( $(MAKE) MellorYamada_nml ; $(MAKE) scenario ; mv ../couette.gotmscenario ../couette.MellorYamada.gotmscenario ; $(MAKE) clean)
	( cd .. ; ln -sf couette.kepsilon.gotmscenario couette.gotmscenario )

examples:
	( $(MAKE) kepsilon_nml     ; $(MAKE) example ; mv ../couette.tar.gz ../couette.kepsilon.tar.gz     ; $(MAKE) clean)
	( $(MAKE) komega_nml       ; $(MAKE) example ; mv ../couette.tar.gz ../couette.komega.tar.gz       ; $(MAKE) clean)
	( $(MAKE) MellorYamada_nml ; $(MAKE) example ; mv ../couette.tar.gz ../couette.MellorYamada.tar.gz ; $(MAKE) clean)
	( cd .. ; ln -sf couette.kepsilon.tar.gz couette.tar.gz )

kepsilon_nml komega_nml MellorYamada_nml:
	@echo
	@echo "Generating input files for: "$@
	@echo
	mkdir -p $@
	ln -sf ../Rules.make
	( cd $@ ; \
	  ln -sf ../couette.$(shell echo $@ | cut -d_ -f 1).values \
	  couette.values ; \
	  $(MAKE) -f ../Makefile namelist \
	)
	$(RM) Rules.make
	ln -sf $@/airsea.nml
	ln -sf $@/gotmmean.nml
	ln -sf $@/gotmturb.nml
	ln -sf $@/obs.nml
	ln -sf $@/gotmrun.nml
	ln -sf $@/kpp.nml

kepsilon komega MellorYamada: 
	$(MAKE) $@_nml
	$(MAKE) run
	mv log.$(name) log.$@.$(name)
	mv $(name).nc $(name).$@.nc

$(name)_clean:

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#-----------------------------------------------------------------------
