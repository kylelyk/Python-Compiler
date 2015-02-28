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
	subl $4, %esp

	movl $1, -4(%ebp)
	movl $5, %edi
	pushl $6
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
	pushl $2
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
	pushl $5
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
	pushl $8
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
	movl %eax, %ecx
	addl $4, %esp
	pushl -4(%ebp)
	pushl %ecx
	pushl %esi
	call set_subscript
	addl $12, %esp
	pushl $4
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl -4(%ebp)
	pushl %ecx
	pushl %esi
	call set_subscript
	addl $12, %esp
	pushl $5
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %edi
	pushl %ecx
	pushl %esi
	call set_subscript
	addl $12, %esp
	pushl %esi
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
