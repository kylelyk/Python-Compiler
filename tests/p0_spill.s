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
	subl $152, %esp

	movl $1, %eax
	movl $5, -8(%ebp)
	pushl $1
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -20(%ebp)
	pushl $2
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -28(%ebp)
	pushl $3
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -24(%ebp)
	pushl $4
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -16(%ebp)
	pushl $5
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %ebx
	pushl $6
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %esi
	pushl $7
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %edi
	pushl $8
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -4(%ebp)
	movl %edi, -144(%ebp)
	movl -4(%ebp), %eax
	movl %eax, -136(%ebp)
	pushl -144(%ebp)
	call is_bool
	movl %eax, %edi
	addl $4, %esp
	pushl -144(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %edi, -132(%ebp)
	orl %ecx, -132(%ebp)
	pushl -136(%ebp)
	call is_bool
	movl %eax, %edi
	addl $4, %esp
	pushl -136(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %edi, %eax
	orl %ecx, %eax
	movl -132(%ebp), %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl -8(%ebp), %ecx		#Start of if
	jne elselbl_1
	pushl -144(%ebp)
	call project_int
	movl %eax, %edi
	addl $4, %esp
	pushl -136(%ebp)
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	addl %edi, %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_1
elselbl_1:
	pushl -144(%ebp)
	call is_big
	movl %eax, %edi
	addl $4, %esp
	pushl -136(%ebp)
	call is_big
	movl %eax, %ecx
	addl $4, %esp
	movl %edi, %eax
	andl %ecx, %eax
	pushl %eax
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl -8(%ebp), %ecx		#Start of if
	jne elselbl_2
	pushl -144(%ebp)
	call project_big
	movl %eax, %edi
	addl $4, %esp
	pushl -136(%ebp)
	call project_big
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl %edi
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

	movl %eax, %edi
	movl -20(%ebp), %eax
	movl %eax, -68(%ebp)
	movl -28(%ebp), %eax
	movl %eax, -60(%ebp)
	pushl -68(%ebp)
	call is_bool
	movl %eax, -124(%ebp)
	addl $4, %esp
	pushl -68(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -124(%ebp), %eax
	movl %eax, -120(%ebp)
	orl %ecx, -120(%ebp)
	pushl -60(%ebp)
	call is_bool
	movl %eax, -116(%ebp)
	addl $4, %esp
	pushl -60(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -116(%ebp), %eax
	orl %ecx, %eax
	movl -120(%ebp), %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl -8(%ebp), %ecx		#Start of if
	jne elselbl_3
	pushl -68(%ebp)
	call project_int
	movl %eax, -52(%ebp)
	addl $4, %esp
	pushl -60(%ebp)
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	addl -52(%ebp), %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_3
elselbl_3:
	pushl -68(%ebp)
	call is_big
	movl %eax, -36(%ebp)
	addl $4, %esp
	pushl -60(%ebp)
	call is_big
	movl %eax, %ecx
	addl $4, %esp
	movl -36(%ebp), %eax
	andl %ecx, %eax
	pushl %eax
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl -8(%ebp), %ecx		#Start of if
	jne elselbl_4
	pushl -68(%ebp)
	call project_big
	movl %eax, -32(%ebp)
	addl $4, %esp
	pushl -60(%ebp)
	call project_big
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl -32(%ebp)
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

	movl %eax, -76(%ebp)
	movl -24(%ebp), %eax
	movl %eax, -64(%ebp)
	pushl -76(%ebp)
	call is_bool
	movl %eax, -104(%ebp)
	addl $4, %esp
	pushl -76(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -104(%ebp), %eax
	movl %eax, -112(%ebp)
	orl %ecx, -112(%ebp)
	pushl -64(%ebp)
	call is_bool
	movl %eax, -108(%ebp)
	addl $4, %esp
	pushl -64(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -108(%ebp), %eax
	orl %ecx, %eax
	movl -112(%ebp), %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl -8(%ebp), %ecx		#Start of if
	jne elselbl_5
	pushl -76(%ebp)
	call project_int
	movl %eax, -128(%ebp)
	addl $4, %esp
	pushl -64(%ebp)
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	addl -128(%ebp), %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_5
elselbl_5:
	pushl -76(%ebp)
	call is_big
	movl %eax, -92(%ebp)
	addl $4, %esp
	pushl -64(%ebp)
	call is_big
	movl %eax, %ecx
	addl $4, %esp
	movl -92(%ebp), %eax
	andl %ecx, %eax
	pushl %eax
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl -8(%ebp), %ecx		#Start of if
	jne elselbl_6
	pushl -76(%ebp)
	call project_big
	movl %eax, -88(%ebp)
	addl $4, %esp
	pushl -64(%ebp)
	call project_big
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl -88(%ebp)
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

	movl %eax, -100(%ebp)
	movl -16(%ebp), %eax
	movl %eax, -72(%ebp)
	pushl -100(%ebp)
	call is_bool
	movl %eax, -48(%ebp)
	addl $4, %esp
	pushl -100(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -48(%ebp), %eax
	movl %eax, -40(%ebp)
	orl %ecx, -40(%ebp)
	pushl -72(%ebp)
	call is_bool
	movl %eax, -56(%ebp)
	addl $4, %esp
	pushl -72(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -56(%ebp), %eax
	orl %ecx, %eax
	movl -40(%ebp), %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl -8(%ebp), %ecx		#Start of if
	jne elselbl_7
	pushl -100(%ebp)
	call project_int
	movl %eax, -84(%ebp)
	addl $4, %esp
	pushl -72(%ebp)
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	addl -84(%ebp), %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_7
elselbl_7:
	pushl -100(%ebp)
	call is_big
	movl %eax, -44(%ebp)
	addl $4, %esp
	pushl -72(%ebp)
	call is_big
	movl %eax, %ecx
	addl $4, %esp
	movl -44(%ebp), %eax
	andl %ecx, %eax
	pushl %eax
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl -8(%ebp), %ecx		#Start of if
	jne elselbl_8
	pushl -100(%ebp)
	call project_big
	movl %eax, -80(%ebp)
	addl $4, %esp
	pushl -72(%ebp)
	call project_big
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl -80(%ebp)
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

	movl %eax, -96(%ebp)
	movl %ebx, -12(%ebp)
	pushl -96(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -96(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	orl %ecx, %ebx
	pushl -12(%ebp)
	call is_bool
	movl %eax, -140(%ebp)
	addl $4, %esp
	pushl -12(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -140(%ebp), %eax
	orl %ecx, %eax
	movl %ebx, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl -8(%ebp), %ecx		#Start of if
	jne elselbl_9
	pushl -96(%ebp)
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
	pushl -96(%ebp)
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

	cmpl -8(%ebp), %ecx		#Start of if
	jne elselbl_10
	pushl -96(%ebp)
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

	movl %eax, %ebx
	pushl %ebx
	call is_bool
	movl %eax, -148(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -148(%ebp), %ebx
	orl %ecx, %ebx
	pushl %esi
	call is_bool
	movl %eax, -152(%ebp)
	addl $4, %esp
	pushl %esi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -152(%ebp), %eax
	orl %ecx, %eax
	movl %ebx, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl -8(%ebp), %ecx		#Start of if
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

	cmpl -8(%ebp), %ecx		#Start of if
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

	movl %eax, %ebx
	pushl %ebx
	call is_bool
	movl %eax, %esi
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %esi, %ebx
	orl %ecx, %ebx
	pushl %edi
	call is_bool
	movl %eax, %esi
	addl $4, %esp
	pushl %edi
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

	cmpl -8(%ebp), %ecx		#Start of if
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

	cmpl -8(%ebp), %ecx		#Start of if
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

	pushl -4(%ebp)
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
