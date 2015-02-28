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

	movl $1, %ebx
	movl $5, %eax
	pushl $3
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
	pushl $6
	call inject_int
	movl %eax, %esi
	addl $4, %esp
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %esi
	pushl %ecx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $2
	call inject_int
	movl %eax, %esi
	addl $4, %esp
	pushl $2
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %esi
	pushl %ecx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $42
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %ebx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl %edi
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
