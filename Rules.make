#
# Rules.make is included by all test cases to perform common tasks
#

# GOTM target version
ver=4.1.0

ifndef GOTMDIR
export GOTMDIR = $(HOME)/GOTM/gotm-git
endif

SCHEMADIR = $(GOTMDIR)/gui.py/schemas/scenario/

tarflags =  --files-from filelist -C ../ -cvzf
tarflags =  -C ../ --files-from filelist -cvzf

all: namelist run

namelist:
#	editscenario.py -e nml --schemadir=$(SCHEMADIR) $(setup).xml . --targetversion=gotm-$(ver)
	editscenario.py --skipvalidation -e nml --schemadir=$(SCHEMADIR) $(setup).xml . --targetversion=gotm-$(ver)

run:
	@echo
	@echo "running gotm"
	@echo
	gotm 2> log.$(name)
	@echo

scenario:
	editscenario.py -e zip --schemadir=$(SCHEMADIR) $(setup).xml $(setup).gotmscenario --targetversion=gotm-$(ver)

example:
	echo -n "Created at: " > timestamp
	date >> timestamp
	tar $(tarflags) ../$(setup).tar.gz

clean:

realclean: clean
	$(RM) log.$(name)
	$(RM) $(name).nc

distclean: realclean $(name)_clean
	$(RM) *.nml
	$(RM) -r *~ $(name).gotmscenario

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#----------------------------------------------------------------------
