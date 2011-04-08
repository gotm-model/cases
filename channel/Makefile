#
# Makefile for 'channel' setup.
# targets are:
#    namelists
#    run_all
#    kepsilon komega MellorYamada: to run specific model
#    for specific turbulence closure models (will be placed in
#    subdirectories)

name	= channel
setup	= $(name)

include ../Rules.make

all:
	@echo
	@echo "usage: make run_all|namelists|<turbulence model - eg. kepsilon>
	@echo

run_all: kepsilon komega MellorYamada clean


namelists: kepsilon_nml komega_nml MellorYamada_nml

scenarios:
	( $(MAKE) kepsilon_nml     ; $(MAKE) scenario ; mv ../channel.gotmscenario ../channel.kepsilon.gotmscenario     ; $(MAKE) clean)
	( $(MAKE) komega_nml       ; $(MAKE) scenario ; mv ../channel.gotmscenario ../channel.komega.gotmscenario       ; $(MAKE) clean)
	( $(MAKE) MellorYamada_nml ; $(MAKE) scenario ; mv ../channel.gotmscenario ../channel.MellorYamada.gotmscenario ; $(MAKE) clean)
	( cd .. ; ln -sf channel.kepsilon.gotmscenario channel.gotmscenario )

examples:
	( $(MAKE) kepsilon_nml     ; $(MAKE) example ; mv ../channel.tar.gz ../channel.kepsilon.tar.gz     ; $(MAKE) clean)
	( $(MAKE) komega_nml       ; $(MAKE) example ; mv ../channel.tar.gz ../channel.komega.tar.gz       ; $(MAKE) clean)
	( $(MAKE) MellorYamada_nml ; $(MAKE) example ; mv ../channel.tar.gz ../channel.MellorYamada.tar.gz ; $(MAKE) clean)
	( cd .. ; ln -sf channel.kepsilon.tar.gz channel.tar.gz )

kepsilon_nml komega_nml MellorYamada_nml:
	@echo
	@echo "Generating input files for: "$@
	@echo
	mkdir -p $@
	ln -sf ../Rules.make
	( cd $@ ; \
	  ln -sf ../channel.$(shell echo $@ | cut -d_ -f 1).values \
	  channel.values ; \
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

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#-----------------------------------------------------------------------
