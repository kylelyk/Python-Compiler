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
	movl $5, %ebx
	pushl $4
	call inject_int
	addl $4, %esp
	movl %eax, %ecx
	pushl %ecx
	call is_bool
	addl $4, %esp
	pushl %eax
	call inject_bool
	addl $4, %esp

	cmpl %ebx, %eax		#Start of if
	jne elselbl_1
	pushl %ecx
	call project_bool
	addl $4, %esp
	negl %eax
	pushl %eax
	call inject_int
	addl $4, %esp
	jmp endlbl_1
elselbl_1:
	pushl %ecx
	call is_int
	addl $4, %esp
	pushl %eax
	call inject_bool
	addl $4, %esp

	cmpl %ebx, %eax		#Start of if
	jne elselbl_2
	pushl %ecx
	call project_int
	addl $4, %esp
	negl %eax
	pushl %eax
	call inject_int
	addl $4, %esp
	jmp endlbl_2
elselbl_2:
	pushl $negError
	call error_pyobj
	addl $4, %esp
endlbl_2:

endlbl_1:

	pushl %eax
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
