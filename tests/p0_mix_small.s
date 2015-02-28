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
	subl $16, %esp

	movl $1, %eax
	movl $5, %esi
	call input_int
	movl %eax, %ecx
	addl $0, %esp
	movl %ecx, %edi
	pushl $4
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -16(%ebp)
	pushl %edi
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl %edi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %edi
	orl %ecx, %edi
	pushl -16(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -16(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	orl %ecx, %eax
	movl %edi, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_1
	pushl %edi
	call project_int
	movl %eax, %ebx
	addl $4, %esp
	pushl -16(%ebp)
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
	jmp endlbl_1
elselbl_1:
	pushl %edi
	call is_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -16(%ebp)
	call is_big
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	andl %ecx, %eax
	pushl %eax
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_2
	pushl %edi
	call project_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -16(%ebp)
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
	jmp endlbl_2
elselbl_2:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_2:

endlbl_1:

	movl %eax, %ebx
	pushl $6
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

	cmpl %esi, %ecx		#Start of if
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

	cmpl %esi, %ecx		#Start of if
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

	movl %eax, %edi
	pushl %ebx
	call is_bool
	movl %eax, -4(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -4(%ebp), %eax
	movl %eax, -8(%ebp)
	orl %ecx, -8(%ebp)
	pushl %edi
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl %edi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	orl %ecx, %eax
	movl -8(%ebp), %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_5
	pushl %ebx
	call project_int
	movl %eax, %ebx
	addl $4, %esp
	pushl %edi
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
	jmp endlbl_5
elselbl_5:
	pushl %ebx
	call is_big
	movl %eax, %ebx
	addl $4, %esp
	pushl %edi
	call is_big
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	andl %ecx, %eax
	pushl %eax
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_6
	pushl %ebx
	call project_big
	movl %eax, %ebx
	addl $4, %esp
	pushl %edi
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
	jmp endlbl_6
elselbl_6:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_6:

endlbl_5:

	movl %eax, %edi
	call input_int
	movl %eax, %ecx
	addl $0, %esp
	pushl %ecx
	call is_bool
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_7
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
	jmp endlbl_7
elselbl_7:
	pushl %ecx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_8
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
	jmp endlbl_8
elselbl_8:
	pushl $negError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_8:

endlbl_7:

	movl %eax, -12(%ebp)
	pushl %edi
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl %edi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %edi
	orl %ecx, %edi
	pushl -12(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -12(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	orl %ecx, %eax
	movl %edi, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_9
	pushl %edi
	call project_int
	movl %eax, %ebx
	addl $4, %esp
	pushl -12(%ebp)
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
	jmp endlbl_9
elselbl_9:
	pushl %edi
	call is_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -12(%ebp)
	call is_big
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	andl %ecx, %eax
	pushl %eax
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_10
	pushl %edi
	call project_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -12(%ebp)
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
	jmp endlbl_10
elselbl_10:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_10:

endlbl_9:

	pushl %eax
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
