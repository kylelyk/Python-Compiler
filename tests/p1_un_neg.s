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

	movl $1, %esi
	movl $5, %ebx
	pushl $1
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
	pushl $1
	call inject_int
	addl $4, %esp
	pushl %eax
	call is_bool
	addl $4, %esp
	pushl %eax
	call inject_bool
	addl $4, %esp

	cmpl %ebx, %eax		#Start of if
	jne elselbl_3
	pushl %eax
	call project_bool
	addl $4, %esp
	negl %eax
	pushl %eax
	call inject_int
	addl $4, %esp
	movl %eax, %ecx
	jmp endlbl_3
elselbl_3:
	pushl %eax
	call is_int
	addl $4, %esp
	pushl %eax
	call inject_bool
	addl $4, %esp

	cmpl %ebx, %eax		#Start of if
	jne elselbl_4
	pushl %eax
	call project_int
	addl $4, %esp
	negl %eax
	pushl %eax
	call inject_int
	addl $4, %esp
	movl %eax, %ecx
	jmp endlbl_4
elselbl_4:
	pushl $negError
	call error_pyobj
	addl $4, %esp
	movl %eax, %ecx
endlbl_4:

endlbl_3:

	movl %ecx, %eax
	pushl %eax
	call is_bool
	addl $4, %esp
	pushl %eax
	call inject_bool
	addl $4, %esp

	cmpl %ebx, %eax		#Start of if
	jne elselbl_5
	pushl %eax
	call project_bool
	addl $4, %esp
	negl %eax
	pushl %eax
	call inject_int
	addl $4, %esp
	movl %eax, %ecx
	jmp endlbl_5
elselbl_5:
	pushl %eax
	call is_int
	addl $4, %esp
	pushl %eax
	call inject_bool
	addl $4, %esp

	cmpl %ebx, %eax		#Start of if
	jne elselbl_6
	pushl %eax
	call project_int
	addl $4, %esp
	negl %eax
	pushl %eax
	call inject_int
	addl $4, %esp
	movl %eax, %ecx
	jmp endlbl_6
elselbl_6:
	pushl $negError
	call error_pyobj
	addl $4, %esp
	movl %eax, %ecx
endlbl_6:

endlbl_5:

	pushl %ecx
	call print_any
	addl $4, %esp
	movl %ebx, %ecx
	pushl %ecx
	call is_bool
	addl $4, %esp
	pushl %eax
	call inject_bool
	addl $4, %esp

	cmpl %ebx, %eax		#Start of if
	jne elselbl_7
	pushl %ecx
	call project_bool
	addl $4, %esp
	negl %eax
	pushl %eax
	call inject_int
	addl $4, %esp
	jmp endlbl_7
elselbl_7:
	pushl %ecx
	call is_int
	addl $4, %esp
	pushl %eax
	call inject_bool
	addl $4, %esp

	cmpl %ebx, %eax		#Start of if
	jne elselbl_8
	pushl %ecx
	call project_int
	addl $4, %esp
	negl %eax
	pushl %eax
	call inject_int
	addl $4, %esp
	jmp endlbl_8
elselbl_8:
	pushl $negError
	call error_pyobj
	addl $4, %esp
endlbl_8:

endlbl_7:

	pushl %eax
	call print_any
	addl $4, %esp
	movl %esi, %ecx
	pushl %ecx
	call is_bool
	addl $4, %esp
	pushl %eax
	call inject_bool
	addl $4, %esp

	cmpl %ebx, %eax		#Start of if
	jne elselbl_9
	pushl %ecx
	call project_bool
	addl $4, %esp
	negl %eax
	pushl %eax
	call inject_int
	addl $4, %esp
	jmp endlbl_9
elselbl_9:
	pushl %ecx
	call is_int
	addl $4, %esp
	pushl %eax
	call inject_bool
	addl $4, %esp

	cmpl %ebx, %eax		#Start of if
	jne elselbl_10
	pushl %ecx
	call project_int
	addl $4, %esp
	negl %eax
	pushl %eax
	call inject_int
	addl $4, %esp
	jmp endlbl_10
elselbl_10:
	pushl $negError
	call error_pyobj
	addl $4, %esp
endlbl_10:

endlbl_9:

	pushl %eax
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
