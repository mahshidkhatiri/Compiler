import numpy as np
def first_caculator(ter,var,Gr):
    first_1=np.zeros((len(ter)+len(var),len(ter)+len(var)))
    for j in range(0,len(var)):
        s=Gr[var[j]]
        for i in range(0,len(ter)):
            for l in s:
                if l[0]==ter[i]:
                    first_1[j][len(var)+i]+=1
        for i in range(0,len(var)):
            for l in s:
                if l[0]==var[i]:
                    first_1[j][i]+=1
    first_sum = np.copy(first_1)
    first_multi = np.copy(first_1)
    while not(np.array_equal(first_multi,np.zeros((len(ter)+len(var),len(ter)+len(var))))):
        first_multi =np.matmul(first_multi,first_1)
        first_sum=first_sum+first_multi
    first={}
    for j in range(0,len(var)):
        first[var[j]]=[]
        for i in range(0,len(ter)):
            if first_sum[j][len(var)+i]==1:
                first[var[j]].append(ter[i])
    v_l_f=[]
    for j in range(0,len(var)):
        s=Gr[var[j]]
        for i in s:
            if i[0]=='landa':
                v_l_f.append(var[j])
    v_l=[]
    while not (np.array_equal(v_l,v_l_f)):
        v_l=np.copy(v_l_f)
        for j in range(0,len(var)):
            if var[j] not in v_l_f:
                s=Gr[var[j]] 
                for i in s:
                    x=True
                    for l in i:
                        if l not in v_l:
                            x=False
                    if x==True:
                        v_l_f.append(var[j])
    for i in v_l:
        first[i].append('landa')
    return first
def Follow_calculator(ter,var,Gr,fr):
    follow={}
    for j in var:
        follow[j]=[]
    for s in var:
        follow[s]=fol(s,ter,var,Gr,fr,follow)
    return follow
def fol(s,ter,var,Gr,fr,follow):
    d=[]
    for g in Gr:
        for l in range(0,len(Gr[g])):
            if s in Gr[g][l]:
                for i in range(0,len(Gr[g][l])):
                    if Gr[g][l][i]==s:
                        if i+1<len(Gr[g][l]):
                            if Gr[g][l][i+1] in ter or Gr[g][l][i+1]=="#" :
                                d.append( Gr[g][l][i+1])
                            if Gr[g][l][i+1] in  var:
                                if 'landa' in fr[Gr[g][l][i+1]]:
                                    for f in fr[Gr[g][l][i+1]]:
                                        if f!='landa':
                                            d.append(f)
                                    for f in fol(Gr[g][l][i+1],ter,var,Gr,fr,follow):
                                        d.append(f)
                                else:
                                    for f in fr[Gr[g][l][i+1]]:
                                        d.append(f)
                        if i== len(Gr[g][l])-1 and g!=s:
                            for f in follow[g]:
                                d.append(f)
    d = list(dict.fromkeys(d))
    return d
       
with open('token.txt') as f:
    lines = f.readlines()
token=[]
for i in lines:
    z=i.split('\n')
    if z[0].find("var")==0:
        z[0]="var"
    token.append(z[0])
token.append("#")
print(token)
Stack=["<S'>"]
terminals=["BEGIN","END","ASSIGN","NUM","MNS","STR","FLOAT","STRING","QM","INT","VL","FLT","RP","LP","LOOP","UNTIL",
           'EQ','MEQ','LEQ','LSS','MR',"DVL","ADD","MUL","DVC","CONDITION","BLOCK","var","comment_more","comment_one_line","ARRAY","LB","RB"]
variables=["<S'>","<START>","<MAIN>","<ASSIGN>","<LOOP>","<CONDITION>","<COMMENT>","<EXP>","<D_A>"
           ,"<ID>","<SIGN_FN>","<L_R>","<C_N>","<C_F>","<C_S>","<C>"
           ,"<EXPP>","<T>","<TT>","<I>","<C_I>","<ID_A>"
           ]
Grammar={"<S'>":[["<START>","#"]],
         
         "<START>":[["BEGIN","<MAIN>","END"]],
         
         "<MAIN>":[["<ASSIGN>","<MAIN>"],
                   ["<LOOP>","<MAIN>"],
                   ["<CONDITION>","<MAIN>"],
                   ["<COMMENT>","<MAIN>"],
                   ["landa"]],
         
         "<ASSIGN>":[["<ID>","<D_A>"],
                     ["STR","<ID>","ASSIGN","QM","STRING","QM","VL"],
                     ["NUM","<ID>","ASSIGN","<EXP>","VL"],
                     ["FLOAT","<ID>","ASSIGN","<EXP>","VL"],
                     ],
         "<D_A>":[["ASSIGN","<C>","VL"],["LP","INT","RP","ASSIGN","<C_N>","VL"]],
         "<LOOP>":[["LOOP","<MAIN>","UNTIL","LP","<L_R>","RP"]],
         
         "<L_R>":[["<ID>","<SIGN_FN>","<C_I>"],
                  ["INT","<SIGN_FN>","<C_N>"],
                  ["FLT","<SIGN_FN>","<C_F>"],
                  ["STRING","EQ","<C_S>"]
                  ],
         
         "<CONDITION>":[["CONDITION","LP","<L_R>","RP","BLOCK","<MAIN>","BLOCK"]],
         
         "<COMMENT>":[["comment_more"],
                      ["comment_one_line"]],
         
         "<EXP>":[["<T>","<EXPP>"]],
         
         "<EXPP>":[["MNS","<EXP>"],
                     ["ADD","<EXP>"],
                     ["landa"]],
         "<T>":[["<I>","<TT>"]],
         "<TT>":[["MUL","<T>"],
                   ["DVL","<T>"],
                   ["DVC","<T>"],
                   ["landa"]],
         "<I>":[["INT"],["var","<ID_A>"],["FLT"]],
         "<ID>":[["var"]],
         "<ID_A>":[["LP","INT","RP"],["landa"]],
         "<SIGN_FN>":[['EQ'],['MEQ'],['LEQ'],['LSS'],['MR']],
         "<C_F>":[["<ID>"],["FLT"],["EXP"]],
         "<C_N>":[["<ID>"],["INT"],["EXP"]],
         "<C_S>":[["<ID>"],["QM","STRING","QM"]],
         "<C_I>":[["<ID>"],["QM","STRING","QM"],["FLT"],["EXP"],["INT"]],
         "<C>":[["<EXP>"],["QM","STRING","QM"],["ARRAY","LB","INT","RB"]]
         }
print("____________________________________________________________________")
print() 
first=first_caculator(terminals,variables,Grammar)
print("first = ",first)
print("____________________________________________________________________")
follow=Follow_calculator(terminals, variables, Grammar,first)        
print()             
print("follow = ",follow)
print("____________________________________________________________________")
commands=[]
d={}
for i in variables:
    d[i]=[]
for i in terminals:
    d[i]=[]
d["#"]=[]
ins=["BEGIN","END","ASSIGN","NUM","MNS","STR","FLOAT","STRING","QM","INT","VL","FLT","RP","LP","LOOP","UNTIL",
           'EQ','MEQ','LEQ','LSS','MR',"DVL","ADD","MUL","DVC","CONDITION","BLOCK","var","comment_more","comment_one_line","ARRAY","LB","RB","#"]
for a in d:
    for s in ins: 
        if a in terminals:
            if s!=a:
                d[a].append("ERROR")
            else:
                d[a].append("POP")
        elif a in variables:
            if s in first[a]:
                di=Grammar[a]
                for i in di:
                    if i[0]==s:
                        l=a+" -> "
                        for j in range(0,len(i)):
                            l=l+i[j]+" "
                        d[a].append(l)
                    
                    elif i[0] in variables:
                        if s in first[i[0]]:
                            l=a+" -> "
                            for j in range(0,len(i)):
                                l=l+i[j]+" "
                            d[a].append(l)
            elif 'landa' in first[a]: 
                if s in follow [a]:
                    l=a+" -> "+"landa"
                    d[a].append(l)
                else:
                    d[a].append("ERROR")
            else:
                d[a].append("ERROR")
        else:
            if a==s :
                d[a].append("ACCEPTED")
            else:
                d[a].append("ERROR")
a=0
while a<len(token):
    if len(Stack)!=0: 
        s=Stack.pop()
        for i in range(0,len(ins)):
            if token[a]==ins[i]:
                if d[s][i]=="POP":
                    a=a+1
                    break
                elif d[s][i]=="ERROR":
                    print("ERROR",s,token[a])
                    a=len(token)
                    break
                elif a==len(token)-1 and d[s][i]=="ACCEPTED":
                    print("ACCEPTED")
                    a=a+1
                    break
                elif a!=len(token)-1 and d[s][i]=="ACCEPTED":
                    print("ERROR",s)
                    a=len(token)
                    break
                else:
                    x=d[s][i].split()
                    if x[2]!='landa':
                        for i in range(0,len(x)-2):
                            Stack.append(x[len(x)-i-1])
                    commands.append(x)
                    break
for i in commands:
    print(i)                