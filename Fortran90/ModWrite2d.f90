module ModWrite2d
  ! A set of routines to help write an output file that must be written
  ! in short portions over the course of a simulation.  We will never be 
  ! given the full array at once; rather, one row (e.g., one timestep) at
  ! a time.  This file could be further generalized by allowing multiple
  ! files to be handled and generating LUNs that are not in use.
  implicit none

  public
  save

  ! Logical unit for output file.
  integer, parameter :: lun=10
  
  ! Has our file been opened and initialized?
  logical :: IsInitialized = .false.

  ! Size of domain
  integer :: iSize

  ! Format code for writing a single record:
  character(len=18) :: StringFmt
  

contains
  !============================================================================
  subroutine init_file(NameFileIn, NameProbIn, iSizeIn, jSizeIn, xIn, &
       yStartIn, yStopIn)
    ! Create file, write header.  Requires name of file and problem
    ! (NameFileIn, NameProbIn), size of domain in x and y (i/jSizeIn), 
    ! points across x-domain (xIn), and the first y-point (yStartIn).

    ! ARGUMENTS: name of file and problem, size of domain, x-domain.
    character(len=*), intent(in) :: NameFileIn, NameProbIn
    integer, intent(in)          :: iSizeIn, jSizeIn
    real, intent(in)             :: xIn(iSizeIn), yStartIn, yStopIn

    integer ::  j
    character(len=24) :: StringFmtX
    !------------------------------------------------------------------------
    ! Open file and assign it to logical unit "lun".
    open(lun, file=NameFileIn, status='replace')

    ! Save iSize.
    iSize = iSizeIn
    
    ! Write header:
    write(lun, '(a)') NameProbIn
    write(lun, "(a,'[',f5.2,',',f5.2,'] ',a,f5.1,',',f5.1,a)") &
         'Domain: x=',xIn(1), xIn(iSizeIn), 't=[',yStartIn, yStopIn,']'
    write(lun, "(a, i5.5, 'x',i5.5)") 'Domain size (x, Time) = ', &
         iSizeIn, jSizeIn
    
    ! Write grid to file, too.
    write(StringFmtX, "(a, i6.6, a)") '(a13,', iSizeIn, '(1x, ES12.6))'
    write(lun, StringFmtX) 'Grid:', xIn
    
    ! Create a format code for a single record.
    write(StringFmt, "(a, i4.4,a)") '(', iSizeIn+1, '(1x, ES12.6))'
    
    ! Finally, set initializtion as true.
    IsInitialized = .true.

  end subroutine init_file

  !============================================================================
  subroutine write_record(yIn, DomainIn)
    ! Write a single record (one row of data, DomainIn) to file for 
    ! current "time" or "y-position", yIn.

    real, intent(in) :: yIn, DomainIn(iSize)

    !------------------------------------------------------------------------
    if(.not. IsInitialized)then
       write(*,*)'ERROR: Writing to unopened file!'
       stop
    end if
    
    write(lun, StringFmt) yIn, DomainIn
    
  end subroutine write_record

  !============================================================================
  subroutine close_file()
    ! Finalize the file by closing the lun.
    
    close(lun)

  end subroutine close_file

  !============================================================================
end module ModWrite2d
