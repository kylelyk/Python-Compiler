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
	subl $48, %esp

	movl $1, %eax
	movl $5, %edi
	call input_int
	movl %eax, %ecx
	addl $0, %esp
	movl %ecx, %esi
	pushl $4
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -36(%ebp)
	pushl %esi
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl %esi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	orl %ecx, %ebx
	pushl -36(%ebp)
	call is_bool
	movl %eax, %esi
	addl $4, %esp
	pushl -36(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %esi, %eax
	orl %ecx, %eax
	movl %ebx, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %edi, %ecx		#Start of if
	jne elselbl_1
	pushl %esi
	call project_int
	movl %eax, %ebx
	addl $4, %esp
	pushl -36(%ebp)
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
	pushl %esi
	call is_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -36(%ebp)
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
	jne elselbl_2
	pushl %esi
	call project_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -36(%ebp)
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

	movl %eax, -4(%ebp)
	pushl $42
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -32(%ebp)
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

	cmpl %edi, %ecx		#Start of if
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

	cmpl %edi, %ecx		#Start of if
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

	movl %eax, %esi
	pushl -32(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -32(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	orl %ecx, %ebx
	pushl %esi
	call is_bool
	movl %eax, -28(%ebp)
	addl $4, %esp
	pushl %esi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -28(%ebp), %eax
	orl %ecx, %eax
	movl %ebx, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %edi, %ecx		#Start of if
	jne elselbl_5
	pushl -32(%ebp)
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
	jmp endlbl_5
elselbl_5:
	pushl -32(%ebp)
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
	jne elselbl_6
	pushl -32(%ebp)
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
	jmp endlbl_6
elselbl_6:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_6:

endlbl_5:

	pushl %eax
	call print_any
	addl $4, %esp
	pushl $4
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %esi
	pushl $5
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -40(%ebp)
	pushl %esi
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl %esi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %esi
	orl %ecx, %esi
	pushl -40(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -40(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	orl %ecx, %eax
	movl %esi, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %edi, %ecx		#Start of if
	jne elselbl_7
	pushl %esi
	call project_int
	movl %eax, %ebx
	addl $4, %esp
	pushl -40(%ebp)
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
	jmp endlbl_7
elselbl_7:
	pushl %esi
	call is_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -40(%ebp)
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
	jne elselbl_8
	pushl %esi
	call project_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -40(%ebp)
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
	jmp endlbl_8
elselbl_8:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_8:

endlbl_7:

	movl %eax, %esi
	pushl $6
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -8(%ebp)
	pushl %esi
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl %esi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %esi
	orl %ecx, %esi
	pushl -8(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -8(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	orl %ecx, %eax
	movl %esi, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %edi, %ecx		#Start of if
	jne elselbl_9
	pushl %esi
	call project_int
	movl %eax, %ebx
	addl $4, %esp
	pushl -8(%ebp)
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
	pushl %esi
	call is_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -8(%ebp)
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
	jne elselbl_10
	pushl %esi
	call project_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -8(%ebp)
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

	movl -4(%ebp), %ebx
	pushl $6
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %esi
	pushl %ebx
	call is_bool
	movl %eax, -20(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -20(%ebp), %eax
	movl %eax, -24(%ebp)
	orl %ecx, -24(%ebp)
	pushl %esi
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl %esi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	orl %ecx, %eax
	movl -24(%ebp), %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %edi, %ecx		#Start of if
	jne elselbl_11
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
	jmp endlbl_11
elselbl_11:
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
	jne elselbl_12
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
	jmp endlbl_12
elselbl_12:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_12:

endlbl_11:

	pushl %eax
	call print_any
	addl $4, %esp
	pushl $6
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	movl -4(%ebp), %esi
	movl %eax, %ebx
	pushl %esi
	call is_bool
	movl %eax, -16(%ebp)
	addl $4, %esp
	pushl %esi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -16(%ebp), %esi
	orl %ecx, %esi
	pushl %ebx
	call is_bool
	movl %eax, -12(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -12(%ebp), %eax
	orl %ecx, %eax
	movl %esi, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %edi, %ecx		#Start of if
	jne elselbl_13
	pushl %esi
	call project_int
	movl %eax, %esi
	addl $4, %esp
	pushl %ebx
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	addl %esi, %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_13
elselbl_13:
	pushl %esi
	call is_big
	movl %eax, %esi
	addl $4, %esp
	pushl %ebx
	call is_big
	movl %eax, %ecx
	addl $4, %esp
	movl %esi, %eax
	andl %ecx, %eax
	pushl %eax
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %edi, %ecx		#Start of if
	jne elselbl_14
	pushl %esi
	call project_big
	movl %eax, %esi
	addl $4, %esp
	pushl %ebx
	call project_big
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %esi
	call add
	movl %eax, %ecx
	addl $8, %esp
	pushl %ecx
	call inject_big
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_14
elselbl_14:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_14:

endlbl_13:

	movl %eax, %ebx
	pushl $42
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
	jne elselbl_15
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
	jmp endlbl_15
elselbl_15:
	pushl %ecx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %edi, %ecx		#Start of if
	jne elselbl_16
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
	jmp endlbl_16
elselbl_16:
	pushl $negError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_16:

endlbl_15:

	movl %eax, %esi
	pushl %ebx
	call is_bool
	movl %eax, -44(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -44(%ebp), %ebx
	orl %ecx, %ebx
	pushl %esi
	call is_bool
	movl %eax, -48(%ebp)
	addl $4, %esp
	pushl %esi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -48(%ebp), %eax
	orl %ecx, %eax
	movl %ebx, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %edi, %ecx		#Start of if
	jne elselbl_17
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
	jmp endlbl_17
elselbl_17:
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
	jne elselbl_18
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
	jmp endlbl_18
elselbl_18:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_18:

endlbl_17:

	pushl %eax
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
