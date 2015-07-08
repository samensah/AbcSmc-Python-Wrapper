CC = g++
#CFLAGS = -g -std=c++0x
CFLAGS = -O2
MKFILE_PATH := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

ABCDIR = $(MKFILE_PATH)/../AbcSmc
ABC_INC = -I$(ABCDIR) -I$(ABCDIR)/sqdb

ABC_LIB = -L$(ABCDIR) -labc -ljsoncpp -lsqdb $(ABCDIR)/sqlite3.o
GSL_LIB = -lm -L$$TACC_GSL_LIB/ -L$$HPC_GSL_LIB/ -lgsl -lgslcblas -lpthread -ldl

libabc_no_mpi:
	$(MAKE) -C $(ABCDIR) -f Makefile all_no_mpi

abc_sql: libabc_no_mpi main_sql.cpp
	$(CC) $(CFLAGS) $(ABC_INC) $(GSL_INC) main_sql.cpp -o abc_sql $(ABC_LIB) $(GSL_LIB)

dice: dice_game.cpp
	$(CC) $(CFLAGS) $(GSL_INC) dice_game.cpp -o dice_game $(GSL_LIB)

clean:
	$(MAKE) -C $(ABCDIR) clean
	rm -f dice_game abc_simulator_sql
