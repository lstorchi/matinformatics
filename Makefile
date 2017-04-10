#!gmake
##################################################
#
# Makefile for pls
#
# $Id$
#
###################################################

CXXFLAGS = -I./ -I./libbasstat/inc

OBJ  = common.o \
       pls.o

all: pls

pls: $(OBJ)
	$(CXX) -o $(@) $(OBJ) -L./libbasstat -lBasStat

clean:
	rm -rf $(OBJ) pls
