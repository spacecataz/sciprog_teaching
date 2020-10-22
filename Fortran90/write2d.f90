! This subroutine writes a 2D array, "DomainIn", and its associated x- and y-
! domain, xIn and yIn, to ascii file.  The size of the arrays, name of the
! problem associated with data, and other info are all saved in the file
! header.
!
! Arguments:
!  NameFileIn: file name of output.
!  NameProbIn: First line of header; name of problem/data description.
!  iSizeIn, jSizeIn: The size of the 2D array.
!  DomainIn: an iSizeIn x jSizeIn array.
!  xIn, yIn: The x- and y- coordinates for the points in DomainIn.
!  
subroutine write2d(NameFileIn, iSizeIn, jSizeIn, DomainIn, &
  xIn, yIn, NameProbIn)

  implicit none

  ! Here, we have an input array, but we won't know how big it is until
  ! the subroutine is called.  Therefore, we have the size of the array
  ! as input arguments.  Also, we don't know how long our character variables
  ! will need to be.  This is a case where we can use "len=*" to declare
  ! our character vars, and their length will be set at runtime.

  character(len=*), intent(in) :: NameFileIn, NameProbIn
  integer, intent(in)          :: iSizeIn, jSizeIn
  real, intent(in) :: DomainIn(iSizeIn, jSizeIn), xIn(iSizeIn), yIn(jSizeIn)

  ! Declare local variables.
  integer :: lun=10, j
  character(len=23) :: fmt2  ! Note that we have to set the size of our
  character(len=17) :: fmt   ! string/character variables.
  !------------------------------------------------------------------------
  ! Open file and assign it to logical unit "lun".
  ! There are many options for the "open" command.  Look it up!
  ! The logical unit is very important.  You cannot reuse it for another
  ! file until you close it for this file (or you'll mess up this file.)
  open(lun, file=NameFileIn, status='replace')
  
  ! Write header.  Use careful format codes to get the exact
  ! output that we want.  This page from 1995 is pretty useful:
  ! https://pages.mtu.edu/~shene/COURSES/cs201/NOTES/chap05/format.html
  write(lun, '(a)') NameProbIn
  write(lun, "(a,'[',f5.2,',',f5.2,'] ',a,f5.1,',',f5.1,a)") &
       'Domain: x=',xIn(1), xIn(iSizeIn), 't=[',yIn(1), yIn(jSizeIn),']'
  write(lun, "(a, i5.5, 'x',i5.5)") 'Domain size (x, Time) = ', iSizeIn, jSizeIn
  
  ! Write grid to file, too.  Here, we have a problem: we need to
  ! use a format code but we don't know how many numbers will be in
  ! our array until run time.  We need to first build a format code by
  ! writing characters into a string, then using that string in our
  ! write statement.
  write(*,*) 'iSizeIn = ', iSizeIn
  write(fmt2, "(a, i6.6, a)") '(a13,', iSizeIn, '(1x, E12.6))'
  write(lun, fmt2) 'Grid:', xIn

  ! Same thing here: we need to write the rest of the values, but don't
  ! know the size of our arrays until run time.  Build another format
  ! code, then use it to write each line of DomainIn.
  write(fmt, "(a, i4.4,a)") '(', iSizeIn+1, '(1x, E12.6))'
  write(*,*) 'fmt = ', fmt
  do j=1, jSizeIn
     write(lun, fmt) yIn(j), DomainIn(:,j)
  end do

  ! Always close your files!
  close(lun)

end subroutine write2d
