#
# Master Makefile for making GOTM git examples
#

SHELL = /bin/bash

ver=4.1.x

ifndef GOTMDIR
export GOTMDIR=$(HOME)/GOTM/gotm-git
endif

# Set the subdirectories of the different test cases
SUBDIRS = $(shell grep -v not_ready READY_CASES)

all: link

gotm-exe:
	$(MAKE) -C $(GOTMDIR)/src

link: gotm-exe
	ln -sf $(GOTMDIR)/bin/gotm_prod_$(FORTRAN_COMPILER) gotm

release: distclean examples scenarios
	tar -cvzf templates.tar.gz templates/
	tar -cvzf gotm-cases-v4.2.tar.gz *.tar.gz
	. ./RSYNC

namelist:
ifdef SUBDIRS
	set -e; for i in $(SUBDIRS); do $(MAKE) -C $$i $@; done
endif

example:
ifdef SUBDIRS
	set -e; for i in $(SUBDIRS); do $(MAKE) -C $$i $@; done
endif

scenario:
ifdef SUBDIRS
	set -e; for i in $(SUBDIRS); do $(MAKE) -C $$i $@; done
endif

run: link
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
	$(RM) *.tar.gz gotm

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#----------------------------------------------------------------------- 
