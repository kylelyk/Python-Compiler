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
	subl $24, %esp

	movl $1, -16(%ebp)
	movl $5, -4(%ebp)
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
	call create_list
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_big
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	movl %eax, %esi
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
	pushl -4(%ebp)
	pushl %ecx
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl $5
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl -4(%ebp)
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl %ebx
	pushl %esi
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $2
	call inject_int
	movl %eax, %esi
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
	movl %eax, -8(%ebp)
	addl $4, %esp
	pushl $34
	call inject_int
	movl %eax, %ebx
	addl $4, %esp
	pushl $3
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ebx
	pushl %ecx
	pushl -8(%ebp)
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
	movl %eax, %ebx
	addl $4, %esp
	pushl $4
	call inject_int
	movl %eax, -20(%ebp)
	addl $4, %esp
	pushl $4
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl -20(%ebp)
	pushl %ecx
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl $4
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ebx
	pushl %ecx
	pushl -8(%ebp)
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
	movl %eax, %ebx
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
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl %ebx
	pushl -16(%ebp)
	pushl -8(%ebp)
	call set_subscript
	addl $12, %esp
	pushl $6
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl -4(%ebp)
	pushl -8(%ebp)
	call set_subscript
	addl $12, %esp
	pushl -8(%ebp)
	pushl %esi
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $3
	call inject_int
	movl %eax, -24(%ebp)
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
	movl %eax, %esi
	addl $4, %esp
	pushl $0
	call inject_int
	movl %eax, %ebx
	addl $4, %esp
	pushl $2345
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	pushl %esi
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	movl %eax, %ebx
	addl $4, %esp
	pushl $2345
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	pushl %esi
	call set_subscript
	addl $12, %esp
	pushl $2
	call inject_int
	movl %eax, %ebx
	addl $4, %esp
	pushl $2345
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	pushl %esi
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
	pushl %esi
	call set_subscript
	addl $12, %esp
	pushl %esi
	pushl -24(%ebp)
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl %edi
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
