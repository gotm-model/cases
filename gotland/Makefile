#$Id$
#
# Makefile for 'gotland' setup.
#

SHELL	= /bin/sh

name	= gotland
setup	= $(name)

export NML_EXTRA=bio bio_iow

all:
	@echo
	@echo "usage: make run_all or make realclean"
	@echo

run_all: namelists run

include ../Rules.make

namelists: namelist

scenarios: namelist scenario

examples: namelist example

clean:

realclean: clean
	$(RM) log.$(name)
	$(RM) $(name).nc

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#-----------------------------------------------------------------------
