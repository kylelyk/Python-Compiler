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
	pushl $0
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call create_dict
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_big
	movl %eax, %ecx
	addl $4, %esp

	cmpl %ebx, %ecx		#Start of if
	jne elselbl_1
	pushl $42
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_1
elselbl_1:
	pushl $0
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call create_list
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_big
	movl %eax, %ecx
	addl $4, %esp

	cmpl %ebx, %ecx		#Start of if
	jne elselbl_2
	pushl $43
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_2
elselbl_2:
	pushl $2
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call create_list
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_big
	movl %eax, %edi
	addl $4, %esp
	pushl $0
	call inject_int
	movl %eax, %esi
	addl $4, %esp
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call is_bool
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %ebx, %ecx		#Start of if
	jne elselbl_3
	pushl %ecx
	call project_bool
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	negl %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_3
elselbl_3:
	pushl %ecx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %ebx, %ecx		#Start of if
	jne elselbl_4
	pushl %ecx
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	negl %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_4
elselbl_4:
	pushl $negError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_4:

endlbl_3:

	pushl %eax
	pushl %esi
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	movl %eax, %esi
	addl $4, %esp
	pushl $0
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %esi
	pushl %edi
	call set_subscript
	addl $12, %esp

	cmpl %ebx, %edi		#Start of if
	jne elselbl_5
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call is_bool
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %ebx, %ecx		#Start of if
	jne elselbl_6
	pushl %ecx
	call project_bool
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	negl %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_6
elselbl_6:
	pushl %ecx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %ebx, %ecx		#Start of if
	jne elselbl_7
	pushl %ecx
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	negl %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_7
elselbl_7:
	pushl $negError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_7:

endlbl_6:


	cmpl %ebx, %eax		#Start of if
	jne elselbl_8
	pushl $78
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_8
elselbl_8:
	movl %ebx, %eax
endlbl_8:

	jmp endlbl_5
elselbl_5:
	pushl $45
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_5:

endlbl_2:

endlbl_1:

	pushl %eax
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
