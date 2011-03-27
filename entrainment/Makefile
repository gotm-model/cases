#$Id: Makefile,v 1.1.1.1 2003/03/11 13:38:57 kbk Exp $
#
# Makefile for 'entrainment' setup.
# targets are:
#    namelists
#    run_all
#    kepsilon komega generic MellorYamada kpp: to generate input files
#    for specific turbulence closure models (will be placed in
#    subdirectories)

SHELL	= /bin/sh

name	= entrainment
setup	= $(name)

all:
	@echo
	@echo "usage: make run_all|namelists|<turbulence model - eg. kepsilon>
	@echo

run_all: kepsilon komega generic MellorYamada kpp clean

include ../Rules.make

namelists: kepsilon_nml komega_nml generic_nml MellorYamada_nml kpp_nml

scenarios:
	( $(MAKE) kepsilon_nml     ; $(MAKE) scenario ; mv ../entrainment.gotmscenario ../entrainment.kepsilon.gotmscenario     ; $(MAKE) clean)
	( $(MAKE) komega_nml       ; $(MAKE) scenario ; mv ../entrainment.gotmscenario ../entrainment.komega.gotmscenario       ; $(MAKE) clean)
	( $(MAKE) generic_nml      ; $(MAKE) scenario ; mv ../entrainment.gotmscenario ../entrainment.generic.gotmscenario      ; $(MAKE) clean)
	( $(MAKE) MellorYamada_nml ; $(MAKE) scenario ; mv ../entrainment.gotmscenario ../entrainment.MellorYamada.gotmscenario ; $(MAKE) clean)
	( $(MAKE) kpp_nml          ; $(MAKE) scenario ; mv ../entrainment.gotmscenario ../entrainment.kpp.gotmscenario          ; $(MAKE) clean)
	( cd .. ; ln -sf entrainment.kepsilon.gotmscenario entrainment.gotmscenario )

examples:
	( $(MAKE) kepsilon_nml     ; $(MAKE) example ; mv ../entrainment.tar.gz ../entrainment.kepsilon.tar.gz     ; $(MAKE) clean)
	( $(MAKE) komega_nml       ; $(MAKE) example ; mv ../entrainment.tar.gz ../entrainment.komega.tar.gz       ; $(MAKE) clean)
	( $(MAKE) generic_nml      ; $(MAKE) example ; mv ../entrainment.tar.gz ../entrainment.generic.tar.gz      ; $(MAKE) clean)
	( $(MAKE) MellorYamada_nml ; $(MAKE) example ; mv ../entrainment.tar.gz ../entrainment.MellorYamada.tar.gz ; $(MAKE) clean)
	( $(MAKE) kpp_nml          ; $(MAKE) example ; mv ../entrainment.tar.gz ../entrainment.kpp.tar.gz          ; $(MAKE) clean)
	( cd .. ; ln -sf entrainment.kepsilon.tar.gz entrainment.tar.gz )

kepsilon_nml komega_nml generic_nml MellorYamada_nml kpp_nml:
	@echo
	@echo "Generating input files for: "$@
	@echo
	mkdir -p $@
	ln -sf ../Rules.make
	( cd $@ ; \
	  ln -sf ../entrainment.$(shell echo $@ | cut -d_ -f 1).values \
	  entrainment.values ; \
	  $(MAKE) -f ../Makefile namelist \
	)
	$(RM) Rules.make
	ln -sf $@/airsea.nml
	ln -sf $@/gotmmean.nml
	ln -sf $@/gotmturb.nml
	ln -sf $@/obs.nml
	ln -sf $@/gotmrun.nml
	ln -sf $@/kpp.nml

kepsilon komega generic MellorYamada kpp: 
	$(MAKE) $@_nml
	$(MAKE) run
	mv log.$(name) log.$@.$(name)
	mv $(name).nc $(name).$@.nc

clean:
	$(RM) *.nml
	$(RM) -r *_nml/ 

realclean: clean
	$(RM) log.*.$(name)
	$(RM) $(name).*.nc $(name).nc
	$(RM) -r gotm timestamp 

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#-----------------------------------------------------------------------
