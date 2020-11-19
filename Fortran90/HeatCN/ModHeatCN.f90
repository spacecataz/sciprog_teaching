module ModHeatCN
  ! A module that contains all the necessary tools for solving the 
  ! heat equation using the Crank-Nicholson method.  The problem is
  ! 1D in space for an arbitrary space/time domain size.  BCS are
  ! Dirichlet and set by variable "Bound_I".

  ! This module requires ModWrite2d and LAPACK to compile.
  ! Use compiler flag -llapack to compile against lapack.
  ! Also, be sure to force double precision to prevent failures.

  ! To use this module, do the following in an external program:
  !  1) "Use ModHeatCN"
  !  2) Set timestep, gridsize, etc.
  !  3) call init_sim()
  !  4) Set array DomainNow to your initial conditions.
  !  5) call integrate()
  !  6) call finalize_sim()

  use ModWrite2d, ONLY: write_record, init_file, close_file

  implicit none

  save
  public  ! This says that all variables and subroutines in this file
          ! can be used by any file using this module.

  ! Parameter-like variables.
  real    :: dt = 0.01, dx = 0.1, tLim(2)=(/0.0,0.1/), xLim(2) = (/0.0, 1.0/)
  real    :: cDiffusion = 1.0
  real    :: Bound_I(2) = (/0,0/) ! Dirichlet boundary values.
  integer :: nT, nX

  ! Output controls:
  logical            :: DoTest = .false.
  character(len=100) :: NameOutFile

  ! Domain variables
  real, allocatable :: Coeffs_II(:,:)
  real, allocatable :: DomainNow(:), DomainNext(:)
  real, allocatable :: xGrid(:), tGrid(:)

  ! Variables that shouldn't be used by others.
  logical, private :: IsInitialized = .false.
 
contains
  !============================================================================
  subroutine init_sim(DxIn, DtIn)
    ! Set up the simulation, initialize domain, etc.
    ! Setting initial conditions is left to the external user.
    
    real, intent(in) :: DxIn, DtIn
    
    integer:: i
    real, allocatable :: CoeffA(:,:), CoeffB(:,:), invA(:,:)
    real :: r
    
    !------------------------------------------------------------------------
    ! Set dx, dt based on inputs.  Because we cannot change our inputs, we
    ! copy them to new memory locations.
    dx = DxIn
    dt = DtIn

    write(*,*) '...initializing arrays...'

    ! Determine size of arrays.
    nX = ceiling( (xLim(2)-xLim(1))/dx + 1.0 )
    nT = ceiling( (tLim(2)-tLim(1))/dt + 1.0 ) 

    if(DoTest) write(*,*) '   Grid size (nX, nT) = ', nX, nT

    ! Allocations
    allocate(DomainNext(nX))
    allocate(DomainNow(nX))
    allocate(xGrid(nX))
    allocate(tGrid(nT))
    allocate(Coeffs_II(nX, nX))

    ! It's usually a good idea to fill matrices with zeros.
    DomainNow  = 0
    DomainNext = 0
    xGrid      = 0
    tGrid      = 0
    
    ! Set up time grid.
    do i=1, nT
       tGrid(i) = tLim(1) + (i-1)*dT
    end do

    ! Set up space grid.
    do i=1, nX
       xGrid(i)     = (i-1) * dx
    end do

    ! Create "r", our important factor.
    r= cDiffusion**2.0 * dt / dx**2.0
    if(DoTest)write(*,*) "r = ", r

    ! Create our matrix "A" and "B" of coefficients:
    allocate(CoeffA(nX,nX))
    allocate(CoeffB(nX,nX))
    allocate(invA(nX, nX))
    ! First and last row:
    CoeffA(1, 1:2)      = (/2.0+2.0*r, -1.*r/)
    CoeffA(nX, nX-1:nX) = (/-1.*r, 2.0+2.0*r/)
    CoeffB(1, 1:2)      = (/2.0-2.0*r,     r/)
    CoeffB(nX, nX-1:nX) = (/    r, 2.0-2.0*r/)
    ! Rest of elements:
    do i=2, nX-1
       CoeffA(i, i-1:i+1) = (/-1.*r, 2.0+2.0*r, -1.*r/)
       CoeffB(i, i-1:i+1) = (/    r, 2.0-2.0*r,     r/)
    end do

    if(DoTest)then
       write(*,*) 'A-Matrix:'
       do i=1, nX
          write(*,'(11(1x, E12.6))') CoeffA(i, :)
       end do
       write(*,*) 'B-Matrix:'
          do i=1, nX
          write(*,'(11(1x, E12.6))') CoeffB(i, :)
       end do
    end if

    ! Calculate A-1*B to get Coeffs_II
    invA = inv(CoeffA)
    Coeffs_II = matmul(invA, CoeffB)

    ! Get rid of unneeded Coeff arrays.
    deallocate(CoeffA)
    deallocate(CoeffB)

    call init_file('results.txt', 'Heat Equation Crank-Nicholson', &
         nX, nT, xGrid, tGrid(1), tGrid(nT))

    ! We're ready to roll.
    IsInitialized = .true.

  end subroutine init_sim

  !============================================================================
  subroutine integrate
    ! Integrate!
    integer :: j
    !------------------------------------------------------------------------
    if(.not. IsInitialized) then
       write(*,*) "Domain not intialized!"
       stop
    end if
    
    do j=1, nT-1
       call write_record(tGrid(j), DomainNow) ! Write domain to file.
       DomainNext = matmul(Coeffs_II, DomainNow) ! Integrate via matrices.
       DomainNow=DomainNext ! Move forward by copying Next to Now.
       ! Enforce boundary conditions:
       DomainNow(1) = Bound_I(1)
       DomainNow(nX)= Bound_I(2)
    end do
    
    ! Write final vector to file.
    call write_record(tGrid(nT), DomainNow)
    
  end subroutine integrate
  !============================================================================
  subroutine finalize_sim
    ! Finalize the simulation by deallocating arrays.  This is a good habit!
    
    !------------------------------------------------------------------------
    deallocate(DomainNow)
    deallocate(DomainNext)
    deallocate(xGrid)
    deallocate(tGrid)

    ! Indicate that we are no longer initialized.
    IsInitialized = .false.
    
    call close_file

    write(*,'(a,i8.8,a)')'Finished simulation.  Produced ', nX*nT, ' points.'
  end subroutine finalize_sim

  !============================================================================
  function inv(A) result(Ainv)
    ! Return the inverse of matrix A.
    real,    dimension(:,:), intent(in) :: A
    real,    dimension(size(A,1),size(A,2)) :: Ainv
    
    real,    dimension(size(A,1)) :: work  ! work array for LAPACK
    integer, dimension(size(A,1)) :: ipiv   ! pivot indices
    integer :: n, info
    !------------------------------------------------------------------------

    ! Store A in Ainv to prevent it from being overwritten by LAPACK
    Ainv = A
    n = size(A,1)
    
    ! DGETRF computes an LU factorization of a general M-by-N matrix A
    ! using partial pivoting with row interchanges.  It is from LAPACK.
    call DGETRF(n, n, Ainv, n, ipiv, info)
    
    if (info /= 0) then
       stop 'Matrix is numerically singular!'
    end if
    
    ! DGETRI computes the inverse of a matrix using the LU factorization
    ! computed by DGETRF.  It is from LAPAPCK.
    call DGETRI(n, Ainv, n, ipiv, work, n, info)
    
    if (info /= 0) then
       stop 'Matrix inversion failed!'
    end if
  end function inv
  !============================================================================

end module ModHeatCN
