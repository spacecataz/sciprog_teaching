program format_example

  implicit none

  ! Declare a number to print:
  real :: x = 1234.56789
  ! Create an array of format specifiers to test on our number:
  integer, parameter :: nCode = 5
  character(len=6), dimension(nCode) :: code = &
       (/' f10.4',' e10.4', 'ES10.4', ' G10.4', ' G10.3'/)

  ! Other variables we need:
  character(len=13) :: FormatNow
  integer :: i

  ! Loop over each format specifier:
  do i=1,nCode
     ! Build a format code to use:
     write(FormatNow,"('(2a,',a,',a)')")code(i)
     ! Apply format code to print number:
     write(*,FormatNow) code(i),"|", x,"|"
  end do
end program format_example
