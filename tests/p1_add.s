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
	subl $36, %esp

	movl $1, %eax
	movl $5, %esi
	pushl $3
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %edi
	pushl $4
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -4(%ebp)
	pushl %edi
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl %edi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	orl %ecx, %ebx
	pushl -4(%ebp)
	call is_bool
	movl %eax, %edi
	addl $4, %esp
	pushl -4(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %edi, %eax
	orl %ecx, %eax
	movl %ebx, %ecx
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
	pushl -4(%ebp)
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
	pushl -4(%ebp)
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
	pushl -4(%ebp)
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

	pushl %eax
	call print_any
	addl $4, %esp
	pushl $3
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %edi
	pushl %edi
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl %edi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	orl %ecx, %ebx
	pushl %esi
	call is_bool
	movl %eax, %edi
	addl $4, %esp
	pushl %esi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %edi, %eax
	orl %ecx, %eax
	movl %ebx, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_3
	pushl %edi
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
	pushl %edi
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

	cmpl %esi, %ecx		#Start of if
	jne elselbl_4
	pushl %edi
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

	movl %eax, %ebx
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %edi
	pushl %ebx
	call is_bool
	movl %eax, -32(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -32(%ebp), %eax
	movl %eax, -36(%ebp)
	orl %ecx, -36(%ebp)
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
	movl -36(%ebp), %ecx
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
	pushl $89
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -20(%ebp)
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
	pushl -20(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -20(%ebp)
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
	jne elselbl_7
	pushl %edi
	call project_int
	movl %eax, %ebx
	addl $4, %esp
	pushl -20(%ebp)
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
	pushl %edi
	call is_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -20(%ebp)
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
	jne elselbl_8
	pushl %edi
	call project_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -20(%ebp)
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

	pushl %eax
	call print_any
	addl $4, %esp
	movl %esi, %edi
	pushl %edi
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl %edi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	orl %ecx, %ebx
	pushl %esi
	call is_bool
	movl %eax, %edi
	addl $4, %esp
	pushl %esi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %edi, %eax
	orl %ecx, %eax
	movl %ebx, %ecx
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
	jmp endlbl_9
elselbl_9:
	pushl %edi
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

	cmpl %esi, %ecx		#Start of if
	jne elselbl_10
	pushl %edi
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
	movl %eax, %ebx
	addl $4, %esp
	pushl $0
	call inject_int
	movl %eax, %edi
	addl $4, %esp
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %edi
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	movl %eax, %edi
	addl $4, %esp
	pushl $2
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %edi
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl $3
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call create_list
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_big
	movl %eax, -16(%ebp)
	addl $4, %esp
	pushl $0
	call inject_int
	movl %eax, %edi
	addl $4, %esp
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %edi
	pushl -16(%ebp)
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	movl %eax, %edi
	addl $4, %esp
	pushl $2
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %edi
	pushl -16(%ebp)
	call set_subscript
	addl $12, %esp
	pushl $2
	call inject_int
	movl %eax, %edi
	addl $4, %esp
	pushl $4
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %edi
	pushl -16(%ebp)
	call set_subscript
	addl $12, %esp
	movl -16(%ebp), %edi
	pushl %ebx
	call is_bool
	movl %eax, -12(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -12(%ebp), %eax
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
	jne elselbl_11
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
	jmp endlbl_11
elselbl_11:
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
	jne elselbl_12
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
	movl %ecx, %ebx
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
	movl %ecx, %edi
	pushl %ebx
	call is_bool
	movl %eax, -24(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -24(%ebp), %ebx
	orl %ecx, %ebx
	pushl %edi
	call is_bool
	movl %eax, -28(%ebp)
	addl $4, %esp
	pushl %edi
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

	cmpl %esi, %ecx		#Start of if
	jne elselbl_13
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
	jmp endlbl_13
elselbl_13:
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
	jne elselbl_14
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
	jmp endlbl_14
elselbl_14:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_14:

endlbl_13:

	pushl %eax
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
