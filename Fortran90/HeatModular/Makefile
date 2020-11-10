# Variables for compiling the solver:
FLAGS = -fdefault-real-8
OPT   = -O3
DFLAG = 
COMPILER = gfortran $(FLAGS) $(DFLAG) $(OPT)
DEPEND = \
	write2d.o   \
	ModHeatEq.o \
	HeatEq.o 

# Variables for creating PDFs, HTML, etc.:
F90SOURCE = $(wildcard *.f90)
F90PDF    = $(patsubst %.f90, %.pdf, $(F90SOURCE))

help: 
	@echo "This makefile compiles the heat equation example program."
	@echo "make heat:  Build the heat equation executable, heat.exe."
	@echo "make viz:   Build heat.exe, run it, and plot results."
	@echo "make debug: Clean and compile with debug flags turned on."
	@echo "make clean: remove results and all compile files."
	@echo "make pdf:   generate syntax-highlighted PDFs/HTMLs of source."

pdf: $(F90PDF)

%.html: %.f90
	pygmentize -f html \
	-O full,style=emacs,linenos='inline',title="Source Code: $<" \
	-o $*.html $< 

%.pdf: %.html
	wkhtmltopdf $*.html $*.pdf

debug:
	make clean
	make DFLAG='-g -fbacktrace -fbounds-check' OPT=-O0

heat: $(DEPEND)
	$(COMPILER) $^ -o $@.exe 

%.o: %.f90
	$(COMPILER) -c  $<

clean:
	rm -f *.o *.exe *.mod *~ results.txt *.html $(F90PDF)

viz: heat
	./$^.exe
	./viz_results.py results.txt
