#$Id$
#
# Makefile for 'seagrass' setup.
#

SHELL	= /bin/sh

name	= seagrass
setup	= $(name)

export NML_EXTRA=seagrass_nml

all:
	@echo
	@echo "usage: make run_all or make realclean"
	@echo

run_all: namelists run

include ../Rules.make

namelists: namelist
	mv seagrass_nml.nml seagrass.nml

scenarios: namelist scenario

examples: namelist example

clean:
	$(RM) *.nml

realclean: clean
	$(RM) log.$(name)
	$(RM) $(name).nc

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#-----------------------------------------------------------------------
