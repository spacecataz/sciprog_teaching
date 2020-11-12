!==============================================================================
module ModHeatEq
  ! This is a "module" subprogram.
  ! Modules are ways to share values and subroutines across many parts
  ! of a larger F90 code.
  ! This contains methods and variables to solve the heat equation for a simple
  ! initial condition.

  ! Begin the initialization/declaration part of the code.

  ! This ensures that NO values are implicitly declared.
  ! ALWAYS include implicit none!!!
  implicit none
  save  ! "save" can be used to ensure that variables retain their values
  ! between calls to this module.  If you don't "save", variables are
  ! reset between calls to this subprogram.

  ! Variable declarations.
  ! Statically typed- variable meanings can't change within any part
  ! of the program!
  logical :: DoTest = .true.
  integer :: nT, nX
  real    :: dt, dx, tLimit=0.2, xLim(2) = (/0,1/)

  ! If you don't know how big an array is upon declaration, we need to
  ! make them allocatable. This means we allocate their size at run time.
  real, allocatable :: Domain_II(:,:)
  real, allocatable :: xGrid(:), tGrid(:)

  ! Constants: the parameter attribute means they can't change their values.
  real, parameter :: cDiffusion = 1.0

  ! The "contains" statement says "everything below this point has access to
  ! the module variables and all functions/subroutines below can be shared
  ! through the module". 
contains

  !============================================================================
  subroutine run_simulation
    ! Advance our simulation from the initial condition to the end of the time
    ! range.  This should only be called AFTER the simulation domain has
    ! been initialized using "init_sim".
    
    ! Note our local variable declarations that are not recognized elsewhere
    ! within the module.
    integer :: j
    real    :: r
    !------------------------------------------------------------------------
    write(*,*) 'Beginning Simulation.'

    ! Check for stability:
    if( .not.IsStable(dT, dx, cDiffusion) ) then
       ! If we're not stable, we need to tell the user and
       ! end the program.  Create a well formatted message:
       write(*,"(a,f10.8,' >',f10.8)")'ERROR: Stability criterion not met! ', &
            dt, (dx**2.0/(2*cDiffusion**2.0))
       stop  ! The stop statement ends the whole program!
    end if
    
    ! Integrate!
    write(*,*) '...integrating...'
    ! Calculate a coefficient...
    r= cDiffusion**2.0 * dt / dx**2.0

    ! For each point from now until the second to last time,
    ! calculate the next state.  See the full PDF for details.
    do j=1, nT-1
       ! Note the ampersand is the line continuation marker.
       Domain_II(2:nX-1,j+1) = (1.0-2.0*r) * Domain_II(2:nX-1, j) + &
            r * (Domain_II(1:nx-2,j) + Domain_II(3:nx,j))
    end do
    
    ! Write results to file.  We do this by calling an external subroutine
    ! (see write2d.f90).  Note the ampersand is the line continuation marker.
    call write2d('results.txt', nX, nT, Domain_II, &
         xGrid, tGrid, 'NMUM Chapter 10 Example 3')
    
  end subroutine run_simulation
  
  !============================================================================
  logical function IsStable(dt, dx, c)
    ! Given a dt, dx, and a diffusion coefficient, c, determine if the 
    ! simulation is stable.  Return a logical indicating the result.

    ! Functions have 0 or more inputs but only ONE output.  The output 
    ! is the variable declared with the function name (i.e., "IsStable").
    ! IsStable is sent back to caller, e.g., x = IsStable(dt, dx, c).

    real, intent(in) :: dt, dx, c
    !------------------------------------------------------------------------

    ! Note how we use the name of the function as a variable inside the function
    IsStable = .true.
    if ( dt > (dx**2.0/(2.0*c**2.0)) ) IsStable=.false.

    ! We don't need a "return" statement.  Functions return only one value
    ! every time.
    
  end function IsStable

  !============================================================================
  subroutine init_sim(DxIn, DtIn)

    ! Subroutines have 0 or more inputs and 0 or more outputs.  We must use
    ! variable attributes to set the "intent" of the variables.  Are they
    ! input, output, or both?  Inputs CAN NOT be changed within the 
    ! subroutine!  This is a good way to prevent mistakes and is a good
    ! habit!
    
    ! Set up the simulation.
    ! Note that for all inputs and outputs, we need to set their
    ! intent. intent(in) are values that cannot be edited/changed inside
    ! the subroutine.  intent(out) are returned to the caller.
    ! intent(inout) are inputs that *can* be changed.  Pick carefully!
    real, intent(in) :: DxIn, DtIn

    ! We also need just one integer.
    integer:: i
    !------------------------------------------------------------------------
    write(*,*) '...initializing simulation...'

    ! Set dx, dt based on inputs.  Because we cannot change our inputs, we
    ! copy them to new memory locations.
    dx = DxIn
    dt = DtIn
    
    ! Determine size of arrays.  "ceiling" rounds to the next highest integer.
    nX = ceiling( (xLim(2)-xLim(1))/dx + 1.0 )
    nT = ceiling( tLimit/dt +  1.0 )

    if(DoTest) write(*,*) '   Grid size (nX, nT) = ', nX, nT

    ! Now that we know size of arrays, allocate our arrays.
    allocate(Domain_II(nX, nT))
    allocate(xGrid(nX))
    allocate(tGrid(nT))

    ! It's usually a good idea to fill matrices with zeros.
    ! Make a habit of doing this.
    Domain_II = 0
    xGrid     = 0

    ! Set up grid and initial conditions.
    ! See PDF for details.
    do i=1, nX
       xGrid(i)       = (i-1) * dx
       Domain_II(i,1) = 4.0*xGrid(i) - 4.0*xGrid(i)**2.0
    end do

    ! Create time grid.
    do i=1, nT
       tGrid(i) = real(i-1) * dT
    end do

    ! We are ready to go!
    
  end subroutine init_sim

  !============================================================================
  subroutine finalize_sim
    ! Finalize the simulation by deallocating arrays.  This is a good habit!
    
    !------------------------------------------------------------------------
    deallocate(Domain_II)
    deallocate(xGrid)
    deallocate(tGrid)

    ! ALWAYS deallocate your arrays!  Otherwise, you will get memory leaks.
    
    write(*,*)'Finished simulation.  Produced ', nX*nT, ' points.'
  end subroutine finalize_sim

  !============================================================================


end module ModHeatEq
!==============================================================================
