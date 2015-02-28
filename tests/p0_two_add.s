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

	movl $1, %eax
	movl $5, -4(%ebp)
	pushl $3
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %ebx
	pushl $4
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %esi
	pushl %ebx
	call is_bool
	movl %eax, %edi
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	orl %ecx, %edi
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
	movl %edi, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl -4(%ebp), %ecx		#Start of if
	jne elselbl_1
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
	jmp endlbl_1
elselbl_1:
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

	cmpl -4(%ebp), %ecx		#Start of if
	jne elselbl_2
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
	pushl $5
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %esi
	pushl %ebx
	call is_bool
	movl %eax, %edi
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	orl %ecx, %edi
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
	movl %edi, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl -4(%ebp), %ecx		#Start of if
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

	cmpl -4(%ebp), %ecx		#Start of if
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


	movl $0, %eax
	leave
	ret
