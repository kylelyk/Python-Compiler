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
	subl $28, %esp

	movl $1, %ebx
	movl $5, %esi
	pushl $2
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call create_dict
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_big
	movl %eax, %edi
	addl $4, %esp
	pushl $0
	call inject_int
	movl %eax, -4(%ebp)
	addl $4, %esp
	pushl $9
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl -4(%ebp)
	pushl %ecx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl %ebx
	pushl %esi
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl %esi
	pushl %edi
	call get_subscript
	movl %eax, %ecx
	addl $8, %esp
	pushl %ecx
	call print_any
	addl $4, %esp
	pushl $4
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
	movl %eax, %ebx
	addl $4, %esp
	pushl $0
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	movl %eax, %ebx
	addl $4, %esp
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $2
	call inject_int
	movl %eax, %ebx
	addl $4, %esp
	pushl $2
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $3
	call inject_int
	movl %eax, %ebx
	addl $4, %esp
	pushl $3
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $2
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

	cmpl %esi, %ecx		#Start of if
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

	pushl %eax
	pushl %edi
	call get_subscript
	movl %eax, %ecx
	addl $8, %esp
	pushl %ecx
	call print_any
	addl $4, %esp
	pushl $4
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call create_list
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_big
	movl %eax, -8(%ebp)
	addl $4, %esp
	pushl $0
	call inject_int
	movl %eax, %ebx
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
	pushl %ecx
	pushl %ebx
	pushl -8(%ebp)
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
	call create_dict
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_big
	movl %eax, %ebx
	addl $4, %esp
	pushl $3
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %esi
	pushl %ecx
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl $5
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %esi
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl %ebx
	pushl %edi
	pushl -8(%ebp)
	call set_subscript
	addl $12, %esp
	pushl $2
	call inject_int
	movl %eax, %ebx
	addl $4, %esp
	pushl $4
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call create_dict
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_big
	movl %eax, -16(%ebp)
	addl $4, %esp
	pushl $34
	call inject_int
	movl %eax, %edi
	addl $4, %esp
	pushl $3
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %edi
	pushl %ecx
	pushl -16(%ebp)
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call create_dict
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_big
	movl %eax, -24(%ebp)
	addl $4, %esp
	pushl $4
	call inject_int
	movl %eax, %edi
	addl $4, %esp
	pushl $4
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %edi
	pushl %ecx
	pushl -24(%ebp)
	call set_subscript
	addl $12, %esp
	pushl $4
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl -24(%ebp)
	pushl %ecx
	pushl -16(%ebp)
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call create_dict
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_big
	movl %eax, %edi
	addl $4, %esp
	pushl $5
	call inject_int
	movl %eax, -12(%ebp)
	addl $4, %esp
	pushl $5
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl -12(%ebp)
	pushl %ecx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $7
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %edi
	pushl %ecx
	pushl -16(%ebp)
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
	movl %eax, -20(%ebp)
	addl $4, %esp
	pushl $0
	call inject_int
	movl %eax, %edi
	addl $4, %esp
	pushl $0
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %edi
	pushl -20(%ebp)
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	movl %eax, %edi
	addl $4, %esp
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %edi
	pushl -20(%ebp)
	call set_subscript
	addl $12, %esp
	pushl $2
	call inject_int
	movl %eax, %edi
	addl $4, %esp
	pushl $2
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %edi
	pushl -20(%ebp)
	call set_subscript
	addl $12, %esp
	pushl -20(%ebp)
	pushl %esi
	pushl -16(%ebp)
	call set_subscript
	addl $12, %esp
	pushl -16(%ebp)
	pushl %ebx
	pushl -8(%ebp)
	call set_subscript
	addl $12, %esp
	pushl $3
	call inject_int
	movl %eax, -28(%ebp)
	addl $4, %esp
	pushl $4
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
	movl %eax, %ebx
	addl $4, %esp
	pushl $2
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	movl %eax, %ebx
	addl $4, %esp
	pushl $23
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $2
	call inject_int
	movl %eax, %ebx
	addl $4, %esp
	pushl $234
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $3
	call inject_int
	movl %eax, %ebx
	addl $4, %esp
	pushl $2345
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl %edi
	pushl -28(%ebp)
	pushl -8(%ebp)
	call set_subscript
	addl $12, %esp
	movl -8(%ebp), %ebx
	pushl $2
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	call get_subscript
	movl %eax, %ecx
	addl $8, %esp
	pushl %esi
	pushl %ecx
	call get_subscript
	movl %eax, %esi
	addl $8, %esp
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %esi
	call get_subscript
	movl %eax, %ecx
	addl $8, %esp
	pushl %ecx
	call print_any
	addl $4, %esp
	pushl $2
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	call get_subscript
	movl %eax, %esi
	addl $8, %esp
	pushl $3
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %esi
	call get_subscript
	movl %eax, %ecx
	addl $8, %esp
	pushl %ecx
	call print_any
	addl $4, %esp
	pushl $3
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	call get_subscript
	movl %eax, %ebx
	addl $8, %esp
	pushl $3
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	call get_subscript
	movl %eax, %ecx
	addl $8, %esp
	pushl %ecx
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
