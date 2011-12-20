#
# Makefile for 'waves_breaking' setup.
# targets are:
#    namelists
#    run_all
#    prescribed kepsilon komega generic: to generate input files
#    for specific turbulence closure models (will be placed in
#    subdirectories)

name	= wave_breaking
setup	= $(name)

all:
	@echo
	@echo "usage: make run_all|namelists|<turbulence model - eg. kepsilon>
	@echo

run_all: prescribed kepsilon komega generic clean

include ../Rules.make

namelists: prescribed_nml kepsilon_nml komega_nml generic_nml

scenarios:
	( $(MAKE) kepsilon_nml   ; $(MAKE) scenario ; mv ../wave_breaking.gotmscenario ../wave_breaking.kepsilon.gotmscenario   ; $(MAKE) clean)
	( $(MAKE) prescribed_nml ; $(MAKE) scenario ; mv ../wave_breaking.gotmscenario ../wave_breaking.prescribed.gotmscenario ; $(MAKE) clean)
	( $(MAKE) komega_nml     ; $(MAKE) scenario ; mv ../wave_breaking.gotmscenario ../wave_breaking.komega.gotmscenario     ; $(MAKE) clean)
	( $(MAKE) generic_nml    ; $(MAKE) scenario ; mv ../wave_breaking.gotmscenario ../wave_breaking.generic.gotmscenario    ; $(MAKE) clean)
	( cd .. ; ln -sf wave_breaking.kepsilon.gotmscenario wave_breaking.gotmscenario )

examples:
	( $(MAKE) kepsilon_nml   ; $(MAKE) example ; mv ../wave_breaking.tar.gz ../wave_breaking.kepsilon.tar.gz   ; $(MAKE) clean)
	( $(MAKE) prescribed_nml ; $(MAKE) example ; mv ../wave_breaking.tar.gz ../wave_breaking.prescribed.tar.gz ; $(MAKE) clean)
	( $(MAKE) komega_nml     ; $(MAKE) example ; mv ../wave_breaking.tar.gz ../wave_breaking.komega.tar.gz     ; $(MAKE) clean)
	( $(MAKE) generic_nml    ; $(MAKE) example ; mv ../wave_breaking.tar.gz ../wave_breaking.generic.tar.gz    ; $(MAKE) clean)
	( cd .. ; ln -sf wave_breaking.kepsilon.tar.gz wave_breaking.tar.gz )

prescribed_nml kepsilon_nml komega_nml generic_nml:
	@echo
	@echo "Generating input files for: "$@
	@echo
	mkdir -p $@
	ln -sf ../Rules.make
	( cd $@ ; \
	  ln -sf ../wave_breaking.$(shell echo $@ | cut -d_ -f 1).values \
	  wave_breaking.values ; \
	  $(MAKE) -f ../Makefile namelist \
	)
	$(RM) Rules.make
	ln -sf $@/airsea.nml
	ln -sf $@/gotmmean.nml
	ln -sf $@/gotmturb.nml
	ln -sf $@/obs.nml
	ln -sf $@/gotmrun.nml
	ln -sf $@/kpp.nml

prescribed kepsilon komega generic: 
	$(MAKE) $@_nml
	$(MAKE) run
	mv log.$(name) log.$@.$(name)
	mv $(name).nc $(name).$@.nc

$(name)_clean:

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#-----------------------------------------------------------------------
