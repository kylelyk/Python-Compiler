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
	subl $208, %esp

	movl $1, %eax
	movl $5, %esi
	pushl $5
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %ebx
	pushl $6
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -36(%ebp)
	pushl $7
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -12(%ebp)
	movl -36(%ebp), %eax
	movl %eax, -8(%ebp)
	movl -8(%ebp), %edi
	pushl %ebx
	call is_bool
	movl %eax, -176(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -176(%ebp), %eax
	movl %eax, -172(%ebp)
	orl %ecx, -172(%ebp)
	pushl %edi
	call is_bool
	movl %eax, -160(%ebp)
	addl $4, %esp
	pushl %edi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -160(%ebp), %eax
	orl %ecx, %eax
	movl -172(%ebp), %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_1
	pushl %ebx
	call project_int
	movl %eax, -164(%ebp)
	addl $4, %esp
	pushl %edi
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	addl -164(%ebp), %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_1
elselbl_1:
	pushl %ebx
	call is_big
	movl %eax, -180(%ebp)
	addl $4, %esp
	pushl %edi
	call is_big
	movl %eax, %ecx
	addl $4, %esp
	movl -180(%ebp), %eax
	andl %ecx, %eax
	pushl %eax
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_2
	pushl %ebx
	call project_big
	movl %eax, -168(%ebp)
	addl $4, %esp
	pushl %edi
	call project_big
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl -168(%ebp)
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
	pushl $11
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -32(%ebp)
	pushl $13
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -28(%ebp)
	pushl $17
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, -16(%ebp)
	pushl $19
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	pushl %eax
	call is_bool
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_3
	pushl %eax
	call project_bool
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	negl %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	jmp endlbl_3
elselbl_3:
	pushl %eax
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_4
	pushl %eax
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	negl %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	jmp endlbl_4
elselbl_4:
	pushl $negError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
endlbl_4:

endlbl_3:

	movl %ecx, -24(%ebp)
	pushl %ebx
	call is_bool
	movl %eax, -40(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -40(%ebp), %eax
	movl %eax, -200(%ebp)
	orl %ecx, -200(%ebp)
	pushl -24(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -24(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	orl %ecx, %eax
	movl -200(%ebp), %ecx
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
	pushl -24(%ebp)
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
	pushl -24(%ebp)
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
	pushl -24(%ebp)
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

	movl %eax, -44(%ebp)
	movl -32(%ebp), %ebx
	pushl -44(%ebp)
	call is_bool
	movl %eax, -48(%ebp)
	addl $4, %esp
	pushl -44(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -48(%ebp), %eax
	movl %eax, -52(%ebp)
	orl %ecx, -52(%ebp)
	pushl %ebx
	call is_bool
	movl %eax, -56(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -56(%ebp), %eax
	orl %ecx, %eax
	movl -52(%ebp), %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_7
	pushl -44(%ebp)
	call project_int
	movl %eax, -60(%ebp)
	addl $4, %esp
	pushl %ebx
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	addl -60(%ebp), %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_7
elselbl_7:
	pushl -44(%ebp)
	call is_big
	movl %eax, -68(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_big
	movl %eax, %ecx
	addl $4, %esp
	movl -68(%ebp), %eax
	andl %ecx, %eax
	pushl %eax
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_8
	pushl -44(%ebp)
	call project_big
	movl %eax, -64(%ebp)
	addl $4, %esp
	pushl %ebx
	call project_big
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl -64(%ebp)
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

	movl %eax, -88(%ebp)
	movl -28(%ebp), %ebx
	pushl -88(%ebp)
	call is_bool
	movl %eax, -96(%ebp)
	addl $4, %esp
	pushl -88(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -96(%ebp), %eax
	movl %eax, -84(%ebp)
	orl %ecx, -84(%ebp)
	pushl %ebx
	call is_bool
	movl %eax, -92(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -92(%ebp), %eax
	orl %ecx, %eax
	movl -84(%ebp), %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_9
	pushl -88(%ebp)
	call project_int
	movl %eax, -72(%ebp)
	addl $4, %esp
	pushl %ebx
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	addl -72(%ebp), %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	jmp endlbl_9
elselbl_9:
	pushl -88(%ebp)
	call is_big
	movl %eax, -80(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_big
	movl %eax, %ecx
	addl $4, %esp
	movl -80(%ebp), %eax
	andl %ecx, %eax
	pushl %eax
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_10
	pushl -88(%ebp)
	call project_big
	movl %eax, -76(%ebp)
	addl $4, %esp
	pushl %ebx
	call project_big
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	pushl -76(%ebp)
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
	movl -36(%ebp), %eax
	pushl %eax
	call is_bool
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_11
	pushl %eax
	call project_bool
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	negl %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	jmp endlbl_11
elselbl_11:
	pushl %eax
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_12
	pushl %eax
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	negl %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	jmp endlbl_12
elselbl_12:
	pushl $negError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
endlbl_12:

endlbl_11:

	movl %ecx, -112(%ebp)
	pushl %ebx
	call is_bool
	movl %eax, -148(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -148(%ebp), %eax
	movl %eax, -156(%ebp)
	orl %ecx, -156(%ebp)
	pushl -112(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -112(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	orl %ecx, %eax
	movl -156(%ebp), %ecx
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
	pushl -112(%ebp)
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
	pushl -112(%ebp)
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
	pushl -112(%ebp)
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

	movl %eax, -144(%ebp)
	movl -12(%ebp), %eax
	movl %eax, -20(%ebp)
	pushl -144(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -144(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	orl %ecx, %ebx
	pushl -20(%ebp)
	call is_bool
	movl %eax, -140(%ebp)
	addl $4, %esp
	pushl -20(%ebp)
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

	cmpl %esi, %ecx		#Start of if
	jne elselbl_15
	pushl -144(%ebp)
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
	jmp endlbl_15
elselbl_15:
	pushl -144(%ebp)
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
	jne elselbl_16
	pushl -144(%ebp)
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
	jmp endlbl_16
elselbl_16:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_16:

endlbl_15:

	movl %eax, %ebx
	movl -12(%ebp), %eax
	movl %eax, -108(%ebp)
	pushl %ebx
	call is_bool
	movl %eax, -152(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -152(%ebp), %eax
	movl %eax, -208(%ebp)
	orl %ecx, -208(%ebp)
	pushl -108(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -108(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	orl %ecx, %eax
	movl -208(%ebp), %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_17
	pushl %ebx
	call project_int
	movl %eax, %ebx
	addl $4, %esp
	pushl -108(%ebp)
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
	pushl -108(%ebp)
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
	jne elselbl_18
	pushl %ebx
	call project_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -108(%ebp)
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

	movl %eax, -132(%ebp)
	movl -12(%ebp), %eax
	movl %eax, -124(%ebp)
	pushl -132(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -132(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	orl %ecx, %ebx
	pushl -124(%ebp)
	call is_bool
	movl %eax, -120(%ebp)
	addl $4, %esp
	pushl -124(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -120(%ebp), %eax
	orl %ecx, %eax
	movl %ebx, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_19
	pushl -132(%ebp)
	call project_int
	movl %eax, %ebx
	addl $4, %esp
	pushl -124(%ebp)
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
	jmp endlbl_19
elselbl_19:
	pushl -132(%ebp)
	call is_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -124(%ebp)
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
	jne elselbl_20
	pushl -132(%ebp)
	call project_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -124(%ebp)
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
	jmp endlbl_20
elselbl_20:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_20:

endlbl_19:

	movl %eax, %ebx
	movl -8(%ebp), %eax
	movl %eax, -116(%ebp)
	pushl %ebx
	call is_bool
	movl %eax, -192(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -192(%ebp), %eax
	movl %eax, -204(%ebp)
	orl %ecx, -204(%ebp)
	pushl -116(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -116(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	orl %ecx, %eax
	movl -204(%ebp), %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_21
	pushl %ebx
	call project_int
	movl %eax, %ebx
	addl $4, %esp
	pushl -116(%ebp)
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
	jmp endlbl_21
elselbl_21:
	pushl %ebx
	call is_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -116(%ebp)
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
	jne elselbl_22
	pushl %ebx
	call project_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -116(%ebp)
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
	jmp endlbl_22
elselbl_22:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_22:

endlbl_21:

	movl %eax, -100(%ebp)
	movl -16(%ebp), %eax
	pushl %eax
	call is_bool
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_23
	pushl %eax
	call project_bool
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	negl %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	jmp endlbl_23
elselbl_23:
	pushl %eax
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_24
	pushl %eax
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	negl %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	jmp endlbl_24
elselbl_24:
	pushl $negError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
endlbl_24:

endlbl_23:

	movl %ecx, -104(%ebp)
	pushl -100(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -100(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, -196(%ebp)
	orl %ecx, -196(%ebp)
	pushl -104(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -104(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ebx, %eax
	orl %ecx, %eax
	movl -196(%ebp), %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_25
	pushl -100(%ebp)
	call project_int
	movl %eax, %ebx
	addl $4, %esp
	pushl -104(%ebp)
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
	jmp endlbl_25
elselbl_25:
	pushl -100(%ebp)
	call is_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -104(%ebp)
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
	jne elselbl_26
	pushl -100(%ebp)
	call project_big
	movl %eax, %ebx
	addl $4, %esp
	pushl -104(%ebp)
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
	jmp endlbl_26
elselbl_26:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_26:

endlbl_25:

	movl %eax, -136(%ebp)
	movl -16(%ebp), %eax
	pushl %eax
	call is_bool
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_27
	pushl %eax
	call project_bool
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	negl %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	jmp endlbl_27
elselbl_27:
	pushl %eax
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_28
	pushl %eax
	call project_int
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
	negl %eax
	pushl %eax
	call inject_int
	movl %eax, %ecx
	addl $4, %esp
	jmp endlbl_28
elselbl_28:
	pushl $negError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
endlbl_28:

endlbl_27:

	movl %ecx, -4(%ebp)
	pushl -136(%ebp)
	call is_bool
	movl %eax, %ebx
	addl $4, %esp
	pushl -136(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	orl %ecx, %ebx
	pushl -4(%ebp)
	call is_bool
	movl %eax, -128(%ebp)
	addl $4, %esp
	pushl -4(%ebp)
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -128(%ebp), %eax
	orl %ecx, %eax
	movl %ebx, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_29
	pushl -136(%ebp)
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
	jmp endlbl_29
elselbl_29:
	pushl -136(%ebp)
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
	jne elselbl_30
	pushl -136(%ebp)
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
	jmp endlbl_30
elselbl_30:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_30:

endlbl_29:

	movl %eax, %ebx
	pushl %ebx
	call is_bool
	movl %eax, -184(%ebp)
	addl $4, %esp
	pushl %ebx
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -184(%ebp), %ebx
	orl %ecx, %ebx
	pushl %edi
	call is_bool
	movl %eax, -188(%ebp)
	addl $4, %esp
	pushl %edi
	call is_int
	movl %eax, %ecx
	addl $4, %esp
	movl -188(%ebp), %eax
	orl %ecx, %eax
	movl %ebx, %ecx
	andl %eax, %ecx
	pushl %ecx
	call inject_bool
	movl %eax, %ecx
	addl $4, %esp

	cmpl %esi, %ecx		#Start of if
	jne elselbl_31
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
	jmp endlbl_31
elselbl_31:
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
	jne elselbl_32
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
	jmp endlbl_32
elselbl_32:
	pushl $addError
	call error_pyobj
	movl %eax, %ecx
	addl $4, %esp
	movl %ecx, %eax
endlbl_32:

endlbl_31:

	pushl %eax
	call print_any
	addl $4, %esp

	movl $0, %eax
	leave
	ret
