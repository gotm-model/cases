#
# Rules.make is included by all test cases to perform common tasks
#

# GOTM target version
ver=5.3

ifndef GOTMDIR
export GOTMDIR = $(HOME)/source/repos/GOTM/code
endif

SCHEMADIR = $(GOTMDIR)/schemas

tarflags =  --files-from filelist -C ../ -cvzf
tarflags =  -C ../ --files-from filelist -cvzf

all: namelist run

namelist:
	editscenario --schemadir=$(SCHEMADIR) --targetversion=gotm-$(ver) $(setup).xml -e nml .

namelist-gui:
	editscenario --schemadir=$(SCHEMADIR) --targetversion=gotm-$(ver) $(setup).xml -e nml . -g

scenario:
	editscenario --schemadir=$(SCHEMADIR) --targetversion=gotm-$(ver) $(setup).xml -e zip $(setup).gotmscenario

run:
	@echo
	@echo "running gotm"
	@echo
#	../gotm 2> log.$(name)
	gotm 2> log.$(name)
	@echo

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
