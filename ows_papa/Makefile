#$Id: Makefile,v 1.1.1.1 2003/03/11 13:38:57 kbk Exp $
#
# Makefile for 'ows_papa' setup.
#

SHELL	= /bin/sh

name	= ows_papa
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
