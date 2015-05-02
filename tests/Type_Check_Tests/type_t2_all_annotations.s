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
	subl $8, %esp           
	pushl %ebx              
	pushl %edi              
	pushl %esi              
	movl $1, %eax           
	movl $5, -4(%ebp)       
	movl 8(%ebp), %eax      #$free_vars_$lambda1
	movl 12(%ebp), %eax     #x$1

	movl %eax, %esi         #x$1 -> __$tmp1
	pushl $5                
	call  inject_int        #inject_int(5)
	movl %eax, %eax         #%eax -> __$tmp11
	addl $4, %esp           
	movl %eax, %edi         #__$tmp11 -> __$tmp2
	pushl %esi              
	call  is_bool           #is_bool(__$tmp1)
	movl %eax, %ebx         #%eax -> __$tmp27
	addl $4, %esp           
	pushl %esi              
	call  is_int            #is_int(__$tmp1)
	movl %eax, %eax         #%eax -> __$tmp28
	addl $4, %esp           
	movl %ebx, -8(%ebp)     #__$tmp27 -> __$tmp29
	orl %eax, -8(%ebp)      #__$tmp28 bitor __$tmp29
	pushl %edi              
	call  is_bool           #is_bool(__$tmp2)
	movl %eax, %ebx         #%eax -> __$tmp30
	addl $4, %esp           
	pushl %edi              
	call  is_int            #is_int(__$tmp2)
	movl %eax, %eax         #%eax -> __$tmp31
	addl $4, %esp           
	movl %ebx, %ecx         #__$tmp30 -> __$tmp32
	orl %eax, %ecx          #__$tmp31 bitor __$tmp32
	movl -8(%ebp), %eax     #__$tmp29 -> __$tmp33
	andl %ecx, %eax         #__$tmp32 bitand __$tmp33
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp33)
	movl %eax, %eax         #%eax -> __$tmp34
	addl $4, %esp           

	cmpl -4(%ebp), %eax     #Start of if(__$tmp34 == True)
	jl elselbl_1            
	pushl %esi              
	call  project_boolint   #project_boolint(__$tmp1)
	movl %eax, %ebx         #%eax -> __$tmp12
	addl $4, %esp           
	pushl %edi              
	call  project_boolint   #project_boolint(__$tmp2)
	movl %eax, %eax         #%eax -> __$tmp13
	addl $4, %esp           
	movl %eax, %eax         #__$tmp13 -> __$tmp14
	addl %ebx, %eax         #__$tmp12 + __$tmp14
	pushl %eax              
	call  inject_int        #inject_int(__$tmp14)
	movl %eax, %eax         #%eax -> __$tmp15
	addl $4, %esp           
	movl %eax, %eax         #__$tmp15 -> __$tmp26
	jmp endlbl_1            
elselbl_1:               
	pushl %esi              
	call  is_big            #is_big(__$tmp1)
	movl %eax, %ebx         #%eax -> __$tmp22
	addl $4, %esp           
	pushl %edi              
	call  is_big            #is_big(__$tmp2)
	movl %eax, %eax         #%eax -> __$tmp23
	addl $4, %esp           
	movl %ebx, %ecx         #__$tmp22 -> __$tmp24
	andl %eax, %ecx         #__$tmp23 bitand __$tmp24
	pushl %ecx              
	call  inject_bool       #inject_bool(__$tmp24)
	movl %eax, %eax         #%eax -> __$tmp25
	addl $4, %esp           

	cmpl -4(%ebp), %eax     #Start of if(__$tmp25 == True)
	jl elselbl_2            
	pushl %esi              
	call  project_big       #project_big(__$tmp1)
	movl %eax, %ebx         #%eax -> __$tmp16
	addl $4, %esp           
	pushl %edi              
	call  project_big       #project_big(__$tmp2)
	movl %eax, %eax         #%eax -> __$tmp17
	addl $4, %esp           
	pushl %eax              
	pushl %ebx              
	call  add               #add(__$tmp16, __$tmp17)
	movl %eax, %eax         #%eax -> __$tmp18
	addl $8, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp18)
	movl %eax, %eax         #%eax -> __$tmp19
	addl $4, %esp           
	movl %eax, %eax         #__$tmp19 -> __$tmp21
	jmp endlbl_2            
elselbl_2:               
	pushl $addError         
	call  error_pyobj       #error_pyobj(addError)
	movl %eax, %eax         #%eax -> __$tmp20
	addl $4, %esp           
	movl %eax, %eax         #__$tmp20 -> __$tmp21
endlbl_2:                

	movl %eax, %eax         #__$tmp21 -> __$tmp26
endlbl_1:                

	movl %eax, %eax         #__$tmp26 -> %eax

	popl %esi               
	popl %edi               
	popl %ebx               
	addl $8, %esp           
	leave                   
	ret                     
main:                    
	pushl %ebp              
	movl %esp, %ebp         
	subl $12, %esp          
	pushl %ebx              
	pushl %edi              
	pushl %esi              
	movl $1, %eax           
	movl $5, %esi           

	call  input_int         #input_int()
	movl %eax, %eax         #%eax -> __$tmp37
	addl $0, %esp           
	pushl %eax              
	call  is_true           #is_true(__$tmp37)
	movl %eax, %eax         #%eax -> __$tmp38
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp38)
	movl %eax, %eax         #%eax -> __$tmp39
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp39 == True)
	jl elselbl_3            
	pushl $4                
	call  inject_int        #inject_int(4)
	movl %eax, %eax         #%eax -> __$tmp35
	addl $4, %esp           
	movl %eax, %eax         #__$tmp35 -> __$tmp36
	jmp endlbl_3            
elselbl_3:               
	movl %ebx, %eax         #false -> __$tmp36
endlbl_3:                

	movl %eax, %edi         #__$tmp36 -> a$0
	call  input_int         #input_int()
	movl %eax, %eax         #%eax -> __$tmp42
	addl $0, %esp           
	pushl %eax              
	call  is_true           #is_true(__$tmp42)
	movl %eax, %eax         #%eax -> __$tmp43
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp43)
	movl %eax, %eax         #%eax -> __$tmp44
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp44 == True)
	jl elselbl_4            
	movl %ebx, %eax         #true -> __$tmp41
	jmp endlbl_4            
elselbl_4:               
	pushl $8                
	call  inject_int        #inject_int(8)
	movl %eax, %eax         #%eax -> __$tmp40
	addl $4, %esp           
	movl %eax, %eax         #__$tmp40 -> __$tmp41
endlbl_4:                

	movl %eax, -4(%ebp)     #__$tmp41 -> b$0
	call  input_int         #input_int()
	movl %eax, %eax         #%eax -> __$tmp56
	addl $0, %esp           
	pushl %eax              
	call  is_true           #is_true(__$tmp56)
	movl %eax, %eax         #%eax -> __$tmp57
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp57)
	movl %eax, %eax         #%eax -> __$tmp58
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp58 == True)
	jl elselbl_5            
	pushl $2                
	call  inject_int        #inject_int(2)
	movl %eax, %eax         #%eax -> __$tmp45
	addl $4, %esp           
	pushl %eax              
	call  create_list       #create_list(__$tmp45)
	movl %eax, %eax         #%eax -> __$tmp46
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp46)
	movl %eax, -8(%ebp)     #%eax -> __$tmp47
	addl $4, %esp           
	pushl $0                
	call  inject_int        #inject_int(0)
	movl %eax, %ebx         #%eax -> __$tmp48
	addl $4, %esp           
	pushl $2                
	call  inject_int        #inject_int(2)
	movl %eax, %eax         #%eax -> __$tmp49
	addl $4, %esp           
	pushl %eax              
	pushl %ebx              
	pushl -8(%ebp)          
	call  set_subscript     #set_subscript(__$tmp47, __$tmp48, __$tmp49)
	movl %eax, %eax         #%eax -> __$tmp50
	addl $12, %esp          
	pushl $1                
	call  inject_int        #inject_int(1)
	movl %eax, %ebx         #%eax -> __$tmp51
	addl $4, %esp           
	pushl $11               
	call  inject_int        #inject_int(11)
	movl %eax, %eax         #%eax -> __$tmp52
	addl $4, %esp           
	pushl %eax              
	pushl %ebx              
	pushl -8(%ebp)          
	call  set_subscript     #set_subscript(__$tmp47, __$tmp51, __$tmp52)
	movl %eax, %eax         #%eax -> __$tmp53
	addl $12, %esp          
	movl -8(%ebp), %eax     #__$tmp47 -> __$tmp55
	jmp endlbl_5            
elselbl_5:               
	pushl $8                
	call  inject_int        #inject_int(8)
	movl %eax, %eax         #%eax -> __$tmp54
	addl $4, %esp           
	movl %eax, %eax         #__$tmp54 -> __$tmp55
endlbl_5:                

	movl %eax, -12(%ebp)    #__$tmp55 -> l$0
	call  input_int         #input_int()
	movl %eax, %eax         #%eax -> __$tmp67
	addl $0, %esp           
	pushl %eax              
	call  is_true           #is_true(__$tmp67)
	movl %eax, %eax         #%eax -> __$tmp68
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp68)
	movl %eax, %eax         #%eax -> __$tmp69
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp69 == True)
	jl elselbl_6            
	pushl $1                
	call  inject_int        #inject_int(1)
	movl %eax, %eax         #%eax -> __$tmp59
	addl $4, %esp           
	pushl %eax              
	call  create_dict       #create_dict(__$tmp59)
	movl %eax, %eax         #%eax -> __$tmp60
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp60)
	movl %eax, -8(%ebp)     #%eax -> __$tmp61
	addl $4, %esp           
	pushl $6                
	call  inject_int        #inject_int(6)
	movl %eax, %ebx         #%eax -> __$tmp62
	addl $4, %esp           
	pushl $2                
	call  inject_int        #inject_int(2)
	movl %eax, %eax         #%eax -> __$tmp63
	addl $4, %esp           
	pushl %ebx              
	pushl %eax              
	pushl -8(%ebp)          
	call  set_subscript     #set_subscript(__$tmp61, __$tmp63, __$tmp62)
	movl %eax, %eax         #%eax -> __$tmp64
	addl $12, %esp          
	movl -8(%ebp), %eax     #__$tmp61 -> __$tmp66
	jmp endlbl_6            
elselbl_6:               
	pushl $8                
	call  inject_int        #inject_int(8)
	movl %eax, %eax         #%eax -> __$tmp65
	addl $4, %esp           
	movl %eax, %eax         #__$tmp65 -> __$tmp66
endlbl_6:                

	movl %eax, %ebx         #__$tmp66 -> d$0
	call  input_int         #input_int()
	movl %eax, %eax         #%eax -> __$tmp77
	addl $0, %esp           
	pushl %eax              
	call  is_true           #is_true(__$tmp77)
	movl %eax, %eax         #%eax -> __$tmp78
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp78)
	movl %eax, %eax         #%eax -> __$tmp79
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp79 == True)
	jl elselbl_7            
	pushl $0                
	call  inject_int        #inject_int(0)
	movl %eax, %eax         #%eax -> __$tmp70
	addl $4, %esp           
	pushl %eax              
	call  create_list       #create_list(__$tmp70)
	movl %eax, %eax         #%eax -> __$tmp71
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp71)
	movl %eax, %eax         #%eax -> __$tmp72
	addl $4, %esp           
	pushl %eax              
	pushl $$lambda1         
	call  create_closure    #create_closure($lambda1, __$tmp72)
	movl %eax, %eax         #%eax -> __$tmp73
	addl $8, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp73)
	movl %eax, %eax         #%eax -> __$tmp74
	addl $4, %esp           
	movl %eax, %eax         #__$tmp74 -> __$tmp76
	jmp endlbl_7            
elselbl_7:               
	pushl $8                
	call  inject_int        #inject_int(8)
	movl %eax, %eax         #%eax -> __$tmp75
	addl $4, %esp           
	movl %eax, %eax         #__$tmp75 -> __$tmp76
endlbl_7:                

	movl %eax, -8(%ebp)     #__$tmp76 -> f$0
	pushl %edi              
	call  print_any         #print_any(a$0)
	addl $4, %esp           
	pushl -4(%ebp)          
	call  print_any         #print_any(b$0)
	addl $4, %esp           
	pushl $1                
	call  inject_int        #inject_int(1)
	movl %eax, %eax         #%eax -> __$tmp80
	addl $4, %esp           
	pushl %eax              
	pushl -12(%ebp)         
	call  get_subscript     #get_subscript(l$0, __$tmp80)
	movl %eax, %eax         #%eax -> __$tmp81
	addl $8, %esp           
	pushl %eax              
	call  print_any         #print_any(__$tmp81)
	addl $4, %esp           
	pushl $2                
	call  inject_int        #inject_int(2)
	movl %eax, %eax         #%eax -> __$tmp82
	addl $4, %esp           
	pushl %eax              
	pushl %ebx              
	call  get_subscript     #get_subscript(d$0, __$tmp82)
	movl %eax, %eax         #%eax -> __$tmp83
	addl $8, %esp           
	pushl %eax              
	call  print_any         #print_any(__$tmp83)
	addl $4, %esp           
	movl -8(%ebp), %eax     #spilled __$tmp3 into __$tmp121
	movl %eax, -4(%ebp)     
	pushl $7                
	call  inject_int        #inject_int(7)
	movl %eax, %eax         #%eax -> __$tmp84
	addl $4, %esp           
	movl %eax, %edi         #__$tmp84 -> __$tmp5
	pushl -4(%ebp)          
	call  is_class          #is_class(__$tmp3)
	movl %eax, %eax         #%eax -> __$tmp118
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp118)
	movl %eax, %eax         #%eax -> __$tmp119
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp119 == True)
	jl elselbl_8            
	pushl -4(%ebp)          
	call  create_object     #create_object(__$tmp3)
	movl %eax, %eax         #%eax -> __$tmp85
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp85)
	movl %eax, %eax         #%eax -> __$tmp86
	addl $4, %esp           
	movl %eax, %ebx         #__$tmp86 -> __$tmp4
	pushl $__init__         
	pushl -4(%ebp)          
	call  has_attr          #has_attr(__$tmp3, __init__)
	movl %eax, %eax         #%eax -> __$tmp94
	addl $8, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp94)
	movl %eax, %eax         #%eax -> __$tmp95
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp95 == True)
	jl elselbl_9            
	pushl $__init__         
	pushl -4(%ebp)          
	call  get_attr          #get_attr(__$tmp3, __init__)
	movl %eax, %eax         #%eax -> __$tmp87
	addl $8, %esp           
	pushl %eax              
	call  get_function      #get_function(__$tmp87)
	movl %eax, %eax         #%eax -> __$tmp88
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp88)
	movl %eax, %eax         #%eax -> __$tmp89
	addl $4, %esp           
	movl %eax, -4(%ebp)     #__$tmp89 -> __$tmp7
	pushl -4(%ebp)          
	call  get_fun_ptr       #get_fun_ptr(__$tmp7)
	movl %eax, %esi         #%eax -> __$tmp90
	addl $4, %esp           
	pushl -4(%ebp)          
	call  get_free_vars     #get_free_vars(__$tmp7)
	movl %eax, %eax         #%eax -> __$tmp91
	addl $4, %esp           
	pushl %edi              
	pushl %ebx              
	pushl %eax              
	call *%esi              #__$tmp90(__$tmp91, __$tmp4, __$tmp5)
	movl %eax, %eax         #%eax -> __$tmp92
	addl $12, %esp          
	movl %eax, %eax         #__$tmp92 -> __$tmp6
	movl %ebx, %eax         #__$tmp4 -> __$tmp93
	jmp endlbl_9            
elselbl_9:               
	movl %ebx, %eax         #__$tmp4 -> __$tmp93
endlbl_9:                

	movl %eax, %eax         #__$tmp93 -> __$tmp117
	jmp endlbl_8            
elselbl_8:               
	pushl -4(%ebp)          
	call  is_bound_method   #is_bound_method(__$tmp3)
	movl %eax, %eax         #%eax -> __$tmp115
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp115)
	movl %eax, %eax         #%eax -> __$tmp116
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp116 == True)
	jl elselbl_10           
	pushl -4(%ebp)          
	call  get_function      #get_function(__$tmp3)
	movl %eax, %eax         #%eax -> __$tmp96
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp96)
	movl %eax, %eax         #%eax -> __$tmp97
	addl $4, %esp           
	movl %eax, %esi         #__$tmp97 -> __$tmp8
	pushl %esi              
	call  get_fun_ptr       #get_fun_ptr(__$tmp8)
	movl %eax, %ebx         #%eax -> __$tmp98
	addl $4, %esp           
	pushl %esi              
	call  get_free_vars     #get_free_vars(__$tmp8)
	movl %eax, %esi         #%eax -> __$tmp99
	addl $4, %esp           
	pushl -4(%ebp)          
	call  get_receiver      #get_receiver(__$tmp3)
	movl %eax, %eax         #%eax -> __$tmp100
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp100)
	movl %eax, %eax         #%eax -> __$tmp101
	addl $4, %esp           
	pushl %edi              
	pushl %eax              
	pushl %esi              
	call *%ebx              #__$tmp98(__$tmp99, __$tmp101, __$tmp5)
	movl %eax, %eax         #%eax -> __$tmp102
	addl $12, %esp          
	movl %eax, %eax         #__$tmp102 -> __$tmp114
	jmp endlbl_10           
elselbl_10:              
	pushl -4(%ebp)          
	call  is_unbound_method #is_unbound_method(__$tmp3)
	movl %eax, %eax         #%eax -> __$tmp112
	addl $4, %esp           
	pushl %eax              
	call  inject_bool       #inject_bool(__$tmp112)
	movl %eax, %eax         #%eax -> __$tmp113
	addl $4, %esp           

	cmpl %esi, %eax         #Start of if(__$tmp113 == True)
	jl elselbl_11           
	pushl -4(%ebp)          
	call  get_function      #get_function(__$tmp3)
	movl %eax, %eax         #%eax -> __$tmp103
	addl $4, %esp           
	pushl %eax              
	call  inject_big        #inject_big(__$tmp103)
	movl %eax, %eax         #%eax -> __$tmp104
	addl $4, %esp           
	movl %eax, %esi         #__$tmp104 -> __$tmp9
	pushl %esi              
	call  get_fun_ptr       #get_fun_ptr(__$tmp9)
	movl %eax, %ebx         #%eax -> __$tmp105
	addl $4, %esp           
	pushl %esi              
	call  get_free_vars     #get_free_vars(__$tmp9)
	movl %eax, %eax         #%eax -> __$tmp106
	addl $4, %esp           
	pushl %edi              
	pushl %eax              
	call *%ebx              #__$tmp105(__$tmp106, __$tmp5)
	movl %eax, %eax         #%eax -> __$tmp107
	addl $8, %esp           
	movl %eax, %eax         #__$tmp107 -> __$tmp111
	jmp endlbl_11           
elselbl_11:              
	movl -4(%ebp), %esi     #__$tmp3 -> __$tmp10
	pushl %esi              
	call  get_fun_ptr       #get_fun_ptr(__$tmp10)
	movl %eax, %ebx         #%eax -> __$tmp108
	addl $4, %esp           
	pushl %esi              
	call  get_free_vars     #get_free_vars(__$tmp10)
	movl %eax, %eax         #%eax -> __$tmp109
	addl $4, %esp           
	pushl %edi              
	pushl %eax              
	call *%ebx              #__$tmp108(__$tmp109, __$tmp5)
	movl %eax, %eax         #%eax -> __$tmp110
	addl $8, %esp           
	movl %eax, %eax         #__$tmp110 -> __$tmp111
endlbl_11:               

	movl %eax, %eax         #__$tmp111 -> __$tmp114
endlbl_10:               

	movl %eax, %eax         #__$tmp114 -> __$tmp117
endlbl_8:                

	pushl %eax              
	call  print_any         #print_any(__$tmp117)
	addl $4, %esp           
	pushl $0                
	call  inject_int        #inject_int(0)
	movl %eax, %eax         #%eax -> __$tmp120
	addl $4, %esp           
	movl %eax, %eax         #__$tmp120 -> %eax

	popl %esi               
	popl %edi               
	popl %ebx               
	addl $12, %esp          
	leave                   
	ret                     
