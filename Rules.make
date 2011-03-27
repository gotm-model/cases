#$Id$

ver=v4.2

ifndef GOTMDIR
GOTMDIR = $(HOME)/GOTM/v4.1.x/
endif

ifndef GOTM_CASES
GOTM_CASES = $(HOME)/gotm-cases/$(ver)
endif

tarflags =  --files-from filelist -C ../ -cvzf
tarflags =  -C ../ --files-from filelist -cvzf

namelist:
	$(GOTM_CASES)/templates/make_namelist $(name)

scenario:
#	$(GOTMDIR)/gui.py/util/nml2xml.py -ns . ../$(name).gotmscenario
	$(GOTMDIR)/gui.py/util/nml2xml.py -ns -check . ../$(name).gotmscenario
#	$(GOTMDIR)/gui.py/util/nml2xml.py ../$(name).tar.gz ../$(name).gotmscenario

run:
	@echo
	@echo "running gotm"
	@echo
	../gotm >& log.$(name)
	@echo

example:
	echo -n "Created at: " > timestamp
	date >> timestamp
	tar $(tarflags) ../$(setup).tar.gz

distclean: realclean
	$(RM) -r *~

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#----------------------------------------------------------------------- 
