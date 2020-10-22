# Simple makefile for "heat.exe".
# See the PDF on canvas for a full description!

default: heat

# Variables:
FLAGS = -fdefault-real-8
OPT   = -O3
DFLAG = 
COMPILER = gfortran $(FLAGS) $(DFLAG) $(OPT)
DEPEND = \
	write2d.o   \
	ModHeatEq.o \
	HeatEq.o 

help: 
	@echo "This makefile compiles the heat equation example program."
	@echo "make viz:   Update the code, run it, and plot results."
	@echo "make debug: Clean and compile with debug flags turned on."
	@echo "make clean: remove results and all compile files."

debug:
	make clean
	make DFLAG='-g -fbacktrace -fbounds-check' OPT=-O0

heat: $(DEPEND)
	$(COMPILER) $^ -o $@.exe 

%.o: %.f90
	$(COMPILER) -c  $<

clean:
	rm -f *.o *.exe *.mod *~ results.txt

viz: heat
	./$^.exe
	./viz_results.py
