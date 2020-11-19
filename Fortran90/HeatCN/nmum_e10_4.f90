program example
  ! Implementation of example 10.4 from NMUM (Fink & Mathews): Crank/Nicholson
  ! for the heat equation.

  !  REQUIREMENTS: This file must be compiled against...
  !     LAPACK 
  !     Write2d.f90
  !     ModOutput.f90

  ! Always start with this implicit none.  It's the most important line
  ! in any fortran program.  It forces the user to declare all variables.
  use ModHeatCN, ONLY: init_sim, integrate, finalize_sim, &
       DomainNow, nX, xGrid, dt, dx

  implicit none

  ! Constants:
  real, parameter :: cPi = 3.14159265359
  integer :: i
  !--------------------------------------------------------------------------
  write(*,*) 'Beginning Simulation.'

  ! Initialize the system.
  call init_sim(0.1, 0.01)

  ! We want non-zero initial conditions!
  do i=1, nX
     DomainNow(i) = sin(cPi*xGrid(i)) + sin(3.0*cPi*xGrid(i)) 
  end do

  DomainNow(1)  = 0.0
  DomainNow(nX) = 0.0

  ! Integrate!
  write(*,*) '...integrating...'
  call integrate()

  ! Wrap things up.
  call finalize_sim()

end program example
