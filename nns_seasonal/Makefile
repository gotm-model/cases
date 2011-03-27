#$Id$
#
# Makefile for 'nns_seasonal' setup.
#

SHELL	= /bin/sh

name	= nns_seasonal
setup	= $(name)

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
	$(RM) *.nml

realclean: clean
	$(RM) log.$(name)
	$(RM) $(name).nc

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#-----------------------------------------------------------------------
