.data
negError:
.asciz "Attempt to negate a non basic type.\n"
addError:
.asciz "Attempt to add a basic type to a non basic type.\n"
debugMsg1:
.asciz "Debug Message 1.\n"
debugMsg2:
.asciz "Debug Message 2.\n"
.text
.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $0, %esp

	movl $1, %eax
	movl $5, %eax
	call input_int
	movl %eax, %ecx
	addl $0, %esp
	pushl %ecx
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
