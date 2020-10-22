! This is our program.  After compilation, the executable will start with
! this file at the start of "program" and end at "end program".
program HeatEq
  ! Similar to NMUM example 10.3, but instituted in a more generalized manner.

  ! Use publicly available subroutines from the module ModHeatEq
  ! Rather than make all values with ModHeatEq available, we'll only "use"
  ! the ones we need.  This is a good habit!
  use ModHeatEq, ONLY: init_sim, run_simulation, finalize_sim

  ! implicit none after any use statements.
  implicit none
  
  !--------------------------------------------------------------------------
  ! begin the main part of the program.
  ! We are calling user defined subroutines to execute our simulation.
  
  ! Initialize simulation using custom dt, dx.
  call init_sim(0.2, 0.02)

  ! Integrate in time, write_result to file.
  ! We can forego the parentheses if there are no arguments to pass.
  call run_simulation

  ! Deallocate all arrays.
  call finalize_sim

end program HeatEq
