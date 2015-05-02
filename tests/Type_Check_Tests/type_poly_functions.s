.data
negError:
.asciz "Attempt to negate a non basic type.\n"
addError:
.asciz "Attempt to add a basic type to a non basic type.\n"
debugMsg1:
.asciz "Debug Message 1.\n"
debugMsg2:
.asciz "Debug Message 2.\n"
__init__:
.asciz "__init__"

.text
.globl $lambda1,main
$lambda1:                
	pushl %ebp              
	movl %esp, %ebp         
	subl $0, %esp           
	pushl %ebx              
	pushl %edi              
	pushl %esi              
	movl $1, %eax           
	movl $5, %ebx           
	movl 8(%ebp), %esi      #$free_vars_$lambda1

	pushl $0                
	call  inject_int        #inject_int(0)
	movl %eax, %eax         #%eax -> __$tmp15
	addl $4, %esp           
	pushl %eax              
	pushl %esi              
	call  get_subscript     #get_subscript($free_vars_$lambda1, __$tmp15)
	movl %eax, %eax         #%eax -> __$tmp16
	addl $8, %esp           
	movl %eax, %esi         #__$tmp16 -> false
	call  input_int         #input_int()
	movl %eax, %eax         #%eax -> __$tmp21
	addl $0, %esp           
	pushl %eax              
	call  is_true           #is_true(__$tmp21)
	movl %eax, %eax         #%eax -> __$tmp22
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp22)
	movl %eax, %eax         #%eax -> __$tmp23
	addl $4, %esp           

	cmpl %ebx, %eax         #Start of if(__$tmp23 == True)
	jl elselbl_1            
	pushl $3                
	call  inject_int        #inject_int(3)
	movl %eax, %eax         #%eax -> __$tmp17
	addl $4, %esp           
	movl %eax, %eax         #__$tmp17 -> __$tmp20
	jmp endlbl_1            
elselbl_1:               
	pushl $0                
	call  inject_int        #inject_int(0)
	movl %eax, %eax         #%eax -> __$tmp18
	addl $4, %esp           
	pushl %eax              
	pushl %esi              
	call  get_subscript     #get_subscript(false, __$tmp18)
	movl %eax, %eax         #%eax -> __$tmp19
	addl $8, %esp           
	movl %eax, %eax         #__$tmp19 -> __$tmp20
endlbl_1:                

	movl %eax, %eax         #__$tmp20 -> %eax

	popl %esi               
	popl %edi               
	popl %ebx               
	addl $0, %esp           
	leave                   
	ret                     
main:                    
	pushl %ebp              
	movl %esp, %ebp         
	subl $8, %esp           
	pushl %ebx              
	pushl %edi              
	pushl %esi              
	movl $1, %eax           
	movl $5, %esi           

	pushl $1                
	call  inject_int        #inject_int(1)
	movl %eax, %eax         #%eax -> __$tmp24
	addl $4, %esp           
	pushl %eax              
	call  create_list       #create_list(__$tmp24)
	movl %eax, %eax         #%eax -> __$tmp25
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp25)
	movl %eax, %edi         #%eax -> __$tmp26
	addl $4, %esp           
	pushl $0                
	call  inject_int        #inject_int(0)
	movl %eax, %ebx         #%eax -> __$tmp27
	addl $4, %esp           
	pushl $0                
	call  inject_int        #inject_int(0)
	movl %eax, %eax         #%eax -> __$tmp28
	addl $4, %esp           
	pushl %eax              
	pushl %ebx              
	pushl %edi              
	call  set_subscript     #set_subscript(__$tmp26, __$tmp27, __$tmp28)
	movl %eax, %eax         #%eax -> __$tmp29
	addl $12, %esp          
	movl %edi, %edi         #__$tmp26 -> false
	pushl $1                
	call  inject_int        #inject_int(1)
	movl %eax, %eax         #%eax -> __$tmp30
	addl $4, %esp           
	pushl %eax              
	call  create_list       #create_list(__$tmp30)
	movl %eax, %eax         #%eax -> __$tmp31
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp31)
	movl %eax, %ebx         #%eax -> __$tmp32
	addl $4, %esp           
	pushl $0                
	call  inject_int        #inject_int(0)
	movl %eax, %eax         #%eax -> __$tmp33
	addl $4, %esp           
	pushl %edi              
	pushl %eax              
	pushl %ebx              
	call  set_subscript     #set_subscript(__$tmp32, __$tmp33, false)
	movl %eax, %eax         #%eax -> __$tmp34
	addl $12, %esp          
	pushl %ebx              
	pushl $$lambda1         
	call  create_closure    #create_closure($lambda1, __$tmp32)
	movl %eax, %eax         #%eax -> __$tmp35
	addl $8, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp35)
	movl %eax, %eax         #%eax -> __$tmp36
	addl $4, %esp           
	movl %eax, -4(%ebp)     #__$tmp36 -> bool_or_int$0
	movl -4(%ebp), %eax     #spilled __$tmp1 into __$tmp108
	movl %eax, -8(%ebp)     
	pushl -8(%ebp)          
	call  is_class          #is_class(__$tmp1)
	movl %eax, %eax         #%eax -> __$tmp70
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp70)
	movl %eax, %eax         #%eax -> __$tmp71
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp71 == True)
	jl elselbl_2            
	pushl -8(%ebp)          
	call  create_object     #create_object(__$tmp1)
	movl %eax, %eax         #%eax -> __$tmp37
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp37)
	movl %eax, %eax         #%eax -> __$tmp38
	addl $4, %esp           
	movl %eax, %ebx         #__$tmp38 -> __$tmp2
	pushl $__init__         
	pushl -8(%ebp)          
	call  has_attr          #has_attr(__$tmp1, __init__)
	movl %eax, %eax         #%eax -> __$tmp46
	addl $8, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp46)
	movl %eax, %eax         #%eax -> __$tmp47
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp47 == True)
	jl elselbl_3            
	pushl $__init__         
	pushl -8(%ebp)          
	call  get_attr          #get_attr(__$tmp1, __init__)
	movl %eax, %eax         #%eax -> __$tmp39
	addl $8, %esp           
	pushl %eax              
	call  get_function      #get_function(__$tmp39)
	movl %eax, %eax         #%eax -> __$tmp40
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp40)
	movl %eax, %eax         #%eax -> __$tmp41
	addl $4, %esp           
	movl %eax, -8(%ebp)     #__$tmp41 -> __$tmp7
	pushl -8(%ebp)          
	call  get_fun_ptr       #get_fun_ptr(__$tmp7)
	movl %eax, %edi         #%eax -> __$tmp42
	addl $4, %esp           
	pushl -8(%ebp)          
	call  get_free_vars     #get_free_vars(__$tmp7)
	movl %eax, %eax         #%eax -> __$tmp43
	addl $4, %esp           
	pushl %ebx              
	pushl %eax              
	call *%edi              #__$tmp42(__$tmp43, __$tmp2)
	movl %eax, %eax         #%eax -> __$tmp44
	addl $8, %esp           
	movl %eax, %eax         #__$tmp44 -> __$tmp3
	movl %ebx, %eax         #__$tmp2 -> __$tmp45
	jmp endlbl_3            
elselbl_3:               
	movl %ebx, %eax         #__$tmp2 -> __$tmp45
endlbl_3:                

	movl %eax, %eax         #__$tmp45 -> __$tmp69
	jmp endlbl_2            
elselbl_2:               
	pushl -8(%ebp)          
	call  is_bound_method   #is_bound_method(__$tmp1)
	movl %eax, %eax         #%eax -> __$tmp67
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp67)
	movl %eax, %eax         #%eax -> __$tmp68
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp68 == True)
	jl elselbl_4            
	pushl -8(%ebp)          
	call  get_function      #get_function(__$tmp1)
	movl %eax, %eax         #%eax -> __$tmp48
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp48)
	movl %eax, %eax         #%eax -> __$tmp49
	addl $4, %esp           
	movl %eax, %edi         #__$tmp49 -> __$tmp8
	pushl %edi              
	call  get_fun_ptr       #get_fun_ptr(__$tmp8)
	movl %eax, %ebx         #%eax -> __$tmp50
	addl $4, %esp           
	pushl %edi              
	call  get_free_vars     #get_free_vars(__$tmp8)
	movl %eax, %edi         #%eax -> __$tmp51
	addl $4, %esp           
	pushl -8(%ebp)          
	call  get_receiver      #get_receiver(__$tmp1)
	movl %eax, %eax         #%eax -> __$tmp52
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp52)
	movl %eax, %eax         #%eax -> __$tmp53
	addl $4, %esp           
	pushl %eax              
	pushl %edi              
	call *%ebx              #__$tmp50(__$tmp51, __$tmp53)
	movl %eax, %eax         #%eax -> __$tmp54
	addl $8, %esp           
	movl %eax, %eax         #__$tmp54 -> __$tmp66
	jmp endlbl_4            
elselbl_4:               
	pushl -8(%ebp)          
	call  is_unbound_method #is_unbound_method(__$tmp1)
	movl %eax, %eax         #%eax -> __$tmp64
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp64)
	movl %eax, %eax         #%eax -> __$tmp65
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp65 == True)
	jl elselbl_5            
	pushl -8(%ebp)          
	call  get_function      #get_function(__$tmp1)
	movl %eax, %eax         #%eax -> __$tmp55
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp55)
	movl %eax, %eax         #%eax -> __$tmp56
	addl $4, %esp           
	movl %eax, %edi         #__$tmp56 -> __$tmp9
	pushl %edi              
	call  get_fun_ptr       #get_fun_ptr(__$tmp9)
	movl %eax, %ebx         #%eax -> __$tmp57
	addl $4, %esp           
	pushl %edi              
	call  get_free_vars     #get_free_vars(__$tmp9)
	movl %eax, %eax         #%eax -> __$tmp58
	addl $4, %esp           
	pushl %eax              
	call *%ebx              #__$tmp57(__$tmp58)
	movl %eax, %eax         #%eax -> __$tmp59
	addl $4, %esp           
	movl %eax, %eax         #__$tmp59 -> __$tmp63
	jmp endlbl_5            
elselbl_5:               
	movl -8(%ebp), %edi     #__$tmp1 -> __$tmp10
	pushl %edi              
	call  get_fun_ptr       #get_fun_ptr(__$tmp10)
	movl %eax, %ebx         #%eax -> __$tmp60
	addl $4, %esp           
	pushl %edi              
	call  get_free_vars     #get_free_vars(__$tmp10)
	movl %eax, %eax         #%eax -> __$tmp61
	addl $4, %esp           
	pushl %eax              
	call *%ebx              #__$tmp60(__$tmp61)
	movl %eax, %eax         #%eax -> __$tmp62
	addl $4, %esp           
	movl %eax, %eax         #__$tmp62 -> __$tmp63
endlbl_5:                

	movl %eax, %eax         #__$tmp63 -> __$tmp66
endlbl_4:                

	movl %eax, %eax         #__$tmp66 -> __$tmp69
endlbl_2:                

	movl %eax, %ebx         #__$tmp69 -> a$0
	movl -4(%ebp), %edi     #bool_or_int$0 -> __$tmp4
	pushl %edi              
	call  is_class          #is_class(__$tmp4)
	movl %eax, %eax         #%eax -> __$tmp105
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp105)
	movl %eax, %eax         #%eax -> __$tmp106
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp106 == True)
	jl elselbl_6            
	pushl %edi              
	call  create_object     #create_object(__$tmp4)
	movl %eax, %eax         #%eax -> __$tmp72
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp72)
	movl %eax, %eax         #%eax -> __$tmp73
	addl $4, %esp           
	movl %eax, -4(%ebp)     #__$tmp73 -> __$tmp5
	pushl $__init__         
	pushl %edi              
	call  has_attr          #has_attr(__$tmp4, __init__)
	movl %eax, %eax         #%eax -> __$tmp81
	addl $8, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp81)
	movl %eax, %eax         #%eax -> __$tmp82
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp82 == True)
	jl elselbl_7            
	pushl $__init__         
	pushl %edi              
	call  get_attr          #get_attr(__$tmp4, __init__)
	movl %eax, %eax         #%eax -> __$tmp74
	addl $8, %esp           
	pushl %eax              
	call  get_function      #get_function(__$tmp74)
	movl %eax, %eax         #%eax -> __$tmp75
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp75)
	movl %eax, %eax         #%eax -> __$tmp76
	addl $4, %esp           
	movl %eax, %esi         #__$tmp76 -> __$tmp11
	pushl %esi              
	call  get_fun_ptr       #get_fun_ptr(__$tmp11)
	movl %eax, %edi         #%eax -> __$tmp77
	addl $4, %esp           
	pushl %esi              
	call  get_free_vars     #get_free_vars(__$tmp11)
	movl %eax, %eax         #%eax -> __$tmp78
	addl $4, %esp           
	pushl -4(%ebp)          
	pushl %eax              
	call *%edi              #__$tmp77(__$tmp78, __$tmp5)
	movl %eax, %eax         #%eax -> __$tmp79
	addl $8, %esp           
	movl %eax, %eax         #__$tmp79 -> __$tmp6
	movl -4(%ebp), %eax     #__$tmp5 -> __$tmp80
	jmp endlbl_7            
elselbl_7:               
	movl -4(%ebp), %eax     #__$tmp5 -> __$tmp80
endlbl_7:                

	movl %eax, %eax         #__$tmp80 -> __$tmp104
	jmp endlbl_6            
elselbl_6:               
	pushl %edi              
	call  is_bound_method   #is_bound_method(__$tmp4)
	movl %eax, %eax         #%eax -> __$tmp102
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp102)
	movl %eax, %eax         #%eax -> __$tmp103
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp103 == True)
	jl elselbl_8            
	pushl %edi              
	call  get_function      #get_function(__$tmp4)
	movl %eax, %eax         #%eax -> __$tmp83
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp83)
	movl %eax, %eax         #%eax -> __$tmp84
	addl $4, %esp           
	movl %eax, %esi         #__$tmp84 -> __$tmp12
	pushl %esi              
	call  get_fun_ptr       #get_fun_ptr(__$tmp12)
	movl %eax, -4(%ebp)     #%eax -> __$tmp85
	addl $4, %esp           
	pushl %esi              
	call  get_free_vars     #get_free_vars(__$tmp12)
	movl %eax, %esi         #%eax -> __$tmp86
	addl $4, %esp           
	pushl %edi              
	call  get_receiver      #get_receiver(__$tmp4)
	movl %eax, %eax         #%eax -> __$tmp87
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp87)
	movl %eax, %eax         #%eax -> __$tmp88
	addl $4, %esp           
	pushl %eax              
	pushl %esi              
	call *-4(%ebp)          #__$tmp85(__$tmp86, __$tmp88)
	movl %eax, %eax         #%eax -> __$tmp89
	addl $8, %esp           
	movl %eax, %eax         #__$tmp89 -> __$tmp101
	jmp endlbl_8            
elselbl_8:               
	pushl %edi              
	call  is_unbound_method #is_unbound_method(__$tmp4)
	movl %eax, %eax         #%eax -> __$tmp99
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp99)
	movl %eax, %eax         #%eax -> __$tmp100
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp100 == True)
	jl elselbl_9            
	pushl %edi              
	call  get_function      #get_function(__$tmp4)
	movl %eax, %eax         #%eax -> __$tmp90
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp90)
	movl %eax, %eax         #%eax -> __$tmp91
	addl $4, %esp           
	movl %eax, %esi         #__$tmp91 -> __$tmp13
	pushl %esi              
	call  get_fun_ptr       #get_fun_ptr(__$tmp13)
	movl %eax, %edi         #%eax -> __$tmp92
	addl $4, %esp           
	pushl %esi              
	call  get_free_vars     #get_free_vars(__$tmp13)
	movl %eax, %eax         #%eax -> __$tmp93
	addl $4, %esp           
	pushl %eax              
	call *%edi              #__$tmp92(__$tmp93)
	movl %eax, %eax         #%eax -> __$tmp94
	addl $4, %esp           
	movl %eax, %eax         #__$tmp94 -> __$tmp98
	jmp endlbl_9            
elselbl_9:               
	movl %edi, %esi         #__$tmp4 -> __$tmp14
	pushl %esi              
	call  get_fun_ptr       #get_fun_ptr(__$tmp14)
	movl %eax, %edi         #%eax -> __$tmp95
	addl $4, %esp           
	pushl %esi              
	call  get_free_vars     #get_free_vars(__$tmp14)
	movl %eax, %eax         #%eax -> __$tmp96
	addl $4, %esp           
	pushl %eax              
	call *%edi              #__$tmp95(__$tmp96)
	movl %eax, %eax         #%eax -> __$tmp97
	addl $4, %esp           
	movl %eax, %eax         #__$tmp97 -> __$tmp98
endlbl_9:                

	movl %eax, %eax         #__$tmp98 -> __$tmp101
endlbl_8:                

	movl %eax, %eax         #__$tmp101 -> __$tmp104
endlbl_6:                

	movl %eax, %esi         #__$tmp104 -> b$0
	pushl %ebx              
	call  print_any         #print_any(a$0)
	addl $4, %esp           
	pushl %esi              
	call  print_any         #print_any(b$0)
	addl $4, %esp           
	pushl $0                
	call  inject_int        #inject_int(0)
	movl %eax, %eax         #%eax -> __$tmp107
	addl $4, %esp           
	movl %eax, %eax         #__$tmp107 -> %eax

	popl %esi               
	popl %edi               
	popl %ebx               
	addl $8, %esp           
	leave                   
	ret                     
