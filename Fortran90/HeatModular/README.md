# Modularized HeatEq Solver

These files are a "second attempt" at a forward-difference solver
for the 1D heat equation.  Rather than have a "one-off" program, we
break things into reusable chunks using stand alone files (e.g., `write2d.f90`)
and via Fortran90+ Modules (e.g., `ModHeatEq.f90`).

## Compilation
Of course, use the makefile.  The default target is "help" with information
on which targets to use for compiling the code and running visualization.

For instructional purposes, the commands are as follows:

```
gfortran -fdefault-real-8  -O3 -c  write2d.f90
gfortran -fdefault-real-8  -O3 -c  ModHeatEq.f90
gfortran -fdefault-real-8  -O3 -c  HeatEq.f90
gfortran -fdefault-real-8  -O3 write2d.o ModHeatEq.o HeatEq.o -o heat.exe
```

## Solution & Visualization
Output files can be quickly visualized using `viz_results.py`.
The reference solution is found in `results_correct.txt`.
