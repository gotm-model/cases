#
# Master Makefile for making GOTM git examples
#

SHELL = /bin/bash

ver=4.1.x

ifndef GOTMDIR
export GOTMDIR=$(HOME)/GOTM/gotm-git
endif

ifdef GOTM_PREFIX
external_GOTM_PREFIX=$(GOTM_PREFIX)
else
GOTM_PREFIX=$(CURDIR)/build
endif

ifdef FABMDIR
FABM_ARG="-DFABM_BASE=$(FABMDIR)"
else
ifndef FABM_PREFIX
FABM_ARG="-DGOTM_USE_FABM=OFF"
endif
endif

# Set the subdirectories of the different test cases
SUBDIRS = $(shell grep -v not_ready READY_CASES)

all: link

gotm-exe:
ifndef external_GOTM_PREFIX
	@mkdir -p build
	@(cd build ; cmake $(GOTMDIR)/src -DCMAKE_INSTALL_PREFIX=`pwd` \
                                          -DGOTM_EMBED_VERSION=ON \
                                          $(FABM_ARG) || false)
	@(cd build ; make install)
endif

link: gotm-exe
	@test -x $(GOTM_PREFIX)/bin/gotm || \
         (echo "ERROR: invalid GOTM_PREFIX=$(GOTM_PREFIX)" ; false)
	@ln -sfv $(GOTM_PREFIX)/bin/gotm

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
	$(RM) -r *.tar.gz gotm build

#-----------------------------------------------------------------------
# Copyright by the GOTM-team under the GNU Public License - www.gnu.org
#----------------------------------------------------------------------- 
