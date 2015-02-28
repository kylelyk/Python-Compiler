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

	movl $1, -12(%ebp)
	movl $5, -8(%ebp)
	pushl $0
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -16(%ebp)
	movl -8(%ebp), %ecx
	pushl $1
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
	movl %eax, -4(%ebp)
	addl $4, %esp
	pushl $0
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl -4(%ebp)
	pushl %edi
	call set_subscript
	addl $12, %esp
	movl -16(%ebp), %eax

	cmpl -8(%ebp), %eax		#Start of if
	jne elselbl_1
	jmp endlbl_1
elselbl_1:
	movl %ecx, %esi

	cmpl -8(%ebp), %esi		#Start of if
	jne elselbl_2
	movl %esi, %eax
	jmp endlbl_2
elselbl_2:
	pushl $99
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %edi
	call get_subscript
	movl %eax, %ecx
	addl $8, %esp
	movl %ecx, %eax
endlbl_2:

endlbl_1:


	cmpl -8(%ebp), %eax		#Start of if
	jne elselbl_3
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_3
elselbl_3:
	pushl $0
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_3:

	pushl %eax
	call print_any
	addl $4, %esp
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -16(%ebp)
	movl -12(%ebp), %ecx
	pushl $1
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
	pushl $0
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %esi
	pushl %edi
	call set_subscript
	addl $12, %esp
	movl -16(%ebp), %eax

	cmpl -8(%ebp), %eax		#Start of if
	jne elselbl_4
	movl %ecx, %ebx

	cmpl -8(%ebp), %ebx		#Start of if
	jne elselbl_5
	pushl $99
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %edi
	call get_subscript
	movl %eax, %ecx
	addl $8, %esp
	movl %ecx, %eax
	jmp endlbl_5
elselbl_5:
	movl %ebx, %eax
endlbl_5:

	jmp endlbl_4
elselbl_4:
endlbl_4:


	cmpl -8(%ebp), %eax		#Start of if
	jne elselbl_6
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_6
elselbl_6:
	pushl $0
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_6:

	pushl %eax
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
