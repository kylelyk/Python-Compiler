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
	subl $8, %esp

	movl $1, %eax
	movl $5, %edi
	pushl $4
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

	cmpl %edi, %ecx		#Start of if
	jne elselbl_1
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
	jmp endlbl_1
elselbl_1:
	pushl %ecx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %edi, %ecx		#Start of if
	jne elselbl_2
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
	jmp endlbl_2
elselbl_2:
	pushl $negError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_2:

endlbl_1:

	movl %eax, %ebx
	pushl $5
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %esi
	pushl %ebx
	call is_bool
	movl %eax, -4(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -4(%ebp), %ebx
	orl %ecx, %ebx
	pushl %esi
	call is_bool
	movl %eax, -8(%ebp)
	addl $4, %esp
	pushl %esi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -8(%ebp), %eax
	orl %ecx, %eax
	movl %ebx, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %edi, %ecx		#Start of if
	jne elselbl_3
	pushl %ebx
	call project_int
	movl %eax, %ebx
	addl $4, %esp
	pushl %esi
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	addl %ebx, %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_3
elselbl_3:
	pushl %ebx
	call is_big
	movl %eax, %ebx
	addl $4, %esp
	pushl %esi
	call is_big
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	andl %ecx, %eax
	pushl %eax
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %edi, %ecx		#Start of if
	jne elselbl_4
	pushl %ebx
	call project_big
	movl %eax, %ebx
	addl $4, %esp
	pushl %esi
	call project_big
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	call add
	movl %eax, %ecx
	addl $8, %esp
	pushl %ecx
	call inject_big
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_4
elselbl_4:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_4:

endlbl_3:

	pushl %eax
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
