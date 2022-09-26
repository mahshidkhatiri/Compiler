symbol_table={'RW':{(1,'Loop'):'LOOP',(2,'Until'):'UNTIL',(3,'Str'):'STR',(4,'Num'):'NUM',(5,'Begin'):'BEGIN',(6,'Block'):'BLOCK',(7,'Flt'):'FLOAT',(8,'Condition'):'CONDITION',(9,'End'):'END',(10,'Array'):'ARRAY'},
              'DL_OP':{(11,'%'):'comment_one_line',(12,'%%'):'comment_more',(13,'"'):'QM',(14,'('):'LP',(15,')'):'RP',(16,'|'):'VL',(17,'//'):'DVC',(18,'+'):'ADD',(19,'-'):'MNS',(20,'/'):'DVL',(21,'*'):'MUL',
                       (22,'=='):'EQ',(23,'>='):'MEQ',(24,'<='):'LEQ',(25,'>'):'LSS',(26,'<'):'MR',(27,':='):'ASSIGN',(28,'['):'LB',(29,']'):'RB'},
              'ID':{}}
def checkfloat(a):
    index=a.find('.')
    if a[0:index].isdigit() and a[index+1:].isdigit():
        return True
    else:
        return False
token=[] 
a="" 
ad=30
file = open('code.txt', 'r')
bo=1
char_p=''
stop=''
char=''
while bo:
    z=0
    if stop=='':
        if (a.isdigit()==False and checkfloat(a)==False) or (a=="" and char.isdigit()==False):
            if char.isspace() == True and a.find('var')==-1:
                a=a
            else:
                if char in ['"','(',')','|','+','-','*','/',':','>','=','<','[',']'] and a=="" :
                    if char_p+char in['//','>=','<=',':=','==']:
                        for j in symbol_table['DL_OP'] :
                            x,y=j
                            if char_p+char==y:
                                c=('DL_OP',symbol_table['DL_OP'][j])
                                token.append(c)
                    elif char=='"':
                        for j in symbol_table['DL_OP'] :
                            x,y=j
                            if char==y:
                                c=('DL_OP',symbol_table['DL_OP'][j])
                                token.append(c)
                        char=file.read(1)
                        if not char: 
                                token=[]
                                token.append("ERROR")
                                break
                        b=''
                        while char!='"':
                            b+=char
                            char=file.read(1)
                            if not char: 
                                token=[]
                                token.append("ERROR")
                                break
                        if char: 
                            c=(b,'STRING')
                            token.append(c)
                        for j in symbol_table['DL_OP'] :
                            x,y=j
                            if char==y:
                                c=('DL_OP',symbol_table['DL_OP'][j])
                                token.append(c)
                    else:
                        if char==">" or char=="<" or char=="/":
                            char_p=char
                            char=file.read(1)
                            if char_p+char in['//','>=','<=']:
                                z=1
                            else:
                                z=1
                                for j in symbol_table['DL_OP'] :
                                    x,y=j
                                    if char_p==y:
                                        c=('DL_OP',symbol_table['DL_OP'][j])
                                        token.append(c)
                        else:
                            for j in symbol_table['DL_OP'] :
                                x,y=j
                                if char==y:
                                    c=('DL_OP',symbol_table['DL_OP'][j])
                                    token.append(c)
                elif a.find("var")==0:
                    if char.isdigit()==True:
                        a+=char
                    elif char.isspace() == True:
                        b=False
                        for j in symbol_table['ID'] :
                            if j==a:
                                b=True
                                c=(str(symbol_table['ID'][j]),str(a))
                                token.append(c)
                        if b==False:
                            s=str(a)
                            symbol_table['ID'][s]=ad
                            c=(str(ad),str(a))
                            token.append(c)
                            ad+=1
                        a=""
                    elif char in ['"','(',')','|','+','-','*','/',':','>','=','<','[',']']:
                        b=False
                        for j in symbol_table['ID'] :
                            if j==a:
                                b=True
                                c=(str(symbol_table['ID'][j]),str(a))
                                token.append(c)
                        if b==False:
                            s=str(a)
                            symbol_table['ID'][s]=ad
                            c=(str(ad),str(a))
                            token.append(c)
                            ad+=1
                        a=""
                        z=1
                    else:
                        token.append("ERROR")
                        break
                elif char=='%' and a=="":
                    char_p=char
                    char=file.read(1) 
                    if char+char_p=='%%':
                        stop='%%'
                        char=''
                        c=('DL_OP','comment_more')
                        token.append(c)
                    elif char_p=="%" and char!="%" :
                        stop='\n'
                        c=('DL_OP','comment_one_line')
                        token.append(c)
                else:
                    a+=char
                    for j in symbol_table['RW'] :
                        x,y=j
                        if a==y :
                            char=file.read(1)
                            z=1
                            if char.isalpha() == False:
                                c=('RW',symbol_table['RW'][j])
                                token.append(c)
                                a=""
        else:
            if a=="":
                a=char
            if a!="":
                if char.isdigit()==True or char=='.':
                    a+=char
                else:
                    if '.' in a:
                        c=(a,'FLT')
                        token.append(c)
                    else:
                        c=(a,'INT')
                        token.append(c)
                    z=1
                    a=""
    elif (stop=='%%' and char+char_p==stop) or (stop=='\n' and char==stop):
        a=""
        char = file.read(1)
        while char!='\n' and stop=="%%":
            if not char: 
                break
            if char.isspace() == True:
                a=''
            else:
                token.append("ERROR")
                bo=0
                break
            char = file.read(1) 
        stop=''
        z=1
    else:
        a+=char
    if z==0:          
        char_p=char
        char = file.read(1) 
        if not char: 
            if a!="" and stop=='':
                token.append("ERROR")
            elif a!="" and stop=='%%':
                token=[]
                token.append("ERROR")
            break
        
file.close()
file1 = open("token.txt", "w")
file1 = open("token.txt", "a")  
l=0
while l<len(token):
    x,y=token[l]
    print(y)
    file1.write(str(y)+"\n")
    l+=1
file1.close()