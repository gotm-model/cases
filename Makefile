#$Id$
#
# Master Makefile for making gotm v4.2 examples
#

SHELL = /bin/sh

ver=4.1.x

ifndef GOTMDIR
export GOTMDIR=$(HOME)/GOTM/v$(ver)
endif

# Set the subdirectories of the different test cases
SUBDIRS = `cat CASES_READY`

all: link

gotm-exe:
	$(MAKE) -C $(GOTMDIR)/src

link: gotm-exe
	ln -sf $(GOTMDIR)/src/gotm_prod_$(FORTRAN_COMPILER) gotm

release: distclean examples scenarios
	tar -cvzf templates.tar.gz templates/
	tar -cvzf gotm-cases-v4.2.tar.gz *.tar.gz
	. ./RSYNC

namelists:
ifdef SUBDIRS
	set -e; for i in $(SUBDIRS); do $(MAKE) -C $$i $@; done
endif

examples:
ifdef SUBDIRS
	set -e; for i in $(SUBDIRS); do $(MAKE) -C $$i $@; done
endif

scenarios:
ifdef SUBDIRS
	set -e; for i in $(SUBDIRS); do $(MAKE) -C $$i $@; done
endif

run_all: link
ifdef SUBDIRS
	set -e; for i in $(SUBDIRS); do $(MAKE) -C $$i $@; done
endif

clean: realclean

realclean:
ifdef SUBDIRS
	set -e; for i in $(SUBDIRS); do $(MAKE) -C $$i $@; done
endif

distclean:
ifdef SUBDIRS
	set -e; for i in $(SUBDIRS); do $(MAKE) -C $$i $@; done
endif
	$(RM) *.tar.gz *.gotmscenario gotm

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#----------------------------------------------------------------------- 
