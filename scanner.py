import numpy as np
def edge_v(l):
    edge={}
    t=["BEGIN","END","ASSIGN","NUM","MNS","STR","FLOAT","STRING","QM","INT","VL","FLT","RP","LP","LOOP","UNTIL",
           'EQ','MEQ','LEQ','LSS','MR',"DVL","ADD","MUL","DVC","CONDITION","BLOCK","var","comment_more","comment_one_line","ARRAY","LB","RB","<S'>","<START>","<MAIN>","<ASSIGN>","<LOOP>","<CONDITION>","<COMMENT>","<EXP>","<D_A>"
           ,"<ID>","<SIGN_FN>","<L_R>","<C_N>","<C_F>","<C_S>","<C>"
           ,"<EXPP>","<T>","<TT>","<I>","<C_I>","<ID_A>","#","landa"]
    for i in t:
        l_1=[]
        for m in l:
            for z in range(0,len(m[1])):
                if "." in m[1][z] and m[1][z][1:]==i:
                    if z+1<len(m[1]):
                        k=[]
                        for f in range(0,z):
                            k.append(m[1][f])
                        k.append(m[1][z][1:])
                        j="."+m[1][z+1]
                        k.append(j)
                        for f in range(z+2,len(m[1])):
                            k.append(m[1][f])
                        l_1.append([m[0],k,m[2]])
                    else:
                        k=[]
                        for f in range(0,z):
                            k.append(m[1][f])
                        j=m[1][z][1:]+"."
                        k.append(j)
                        l_1.append([m[0],k,m[2]])
        
        edge[i]=ver(l_1)
    for i in list(edge):
        if edge[i]==[]:
            del edge[i]
    return edge
    
def ver(l):
    v=[]
    x=True
    while(x):
        y=False
        l_1=[]
        for m in l:
            for z in range(0,len(m[1])):
                if "." in m[1][z]:
                    if m[1][z][1:] in variables and m[1][z][1:] not in v:
                        d=[]
                        if z+1<len(m[1]):
                            if m[1][z+1] in terminals or m[1][z+1]=='#':
                                d=[m[1][z+1]]
                            else:
                                if 'landa' in first[m[1][z+1]]:
                                    d=first[m[1][z+1]][:-1]
                                    for j in follow[m[1][z+1]]:
                                        d.append(j)
                                else:
                                     d=first[m[1][z+1]]
                        else:
                            d=m[2]
                            
                        for i in Grammar[m[1][z][1:]]:
                            x=list(i)
                            v.append(m[1][z][1:])
                            x[0]="."+x[0]
                            l_1.append([m[1][z][1:],x,d])
        for i in l_1 :
            l.append(i)
        for m in l:
            for z in range(0,len(m[1])):
                if "." in m[1][z]:
                    if m[1][z][1:] in variables and m[1][z][1:] not in v:
                        y=True
        if y==False:
            x=False
           
    return l
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
first=first_caculator(terminals,variables,Grammar)
follow=Follow_calculator(terminals, variables, Grammar,first)      
'''
print("____________________________________________________________________")
print() 

print("first = ",first)
print("____________________________________________________________________")
  
print()             
print("follow = ",follow)
print("____________________________________________________________________")
'''
list_G=[]
l=[["<S'>",[".<START>","#"],[""]]]
l=ver(l)
v=[l]
e=edge_v(l)
list_G.append([l,e])
for j in list_G :
        e=j[1]
        for i in list(e):
            l=e[i]
            if l not in v:
                e1=edge_v(l)
                list_G.append([l,e1])
                j[1][i]=len(list_G)-1
                v.append(l)
            else:
                for o in range(0,len(v)):
                    if v[o]==l:
                        j[1][i]=o
t=["BEGIN","END","ASSIGN","NUM","MNS","STR","FLOAT","STRING","QM","INT","VL","FLT","RP","LP","LOOP","UNTIL",
           'EQ','MEQ','LEQ','LSS','MR',"DVL","ADD","MUL","DVC","CONDITION","BLOCK","var","comment_more"
           ,"comment_one_line","ARRAY","LB","RB","#","landa"]
t2=["<S'>","<START>","<MAIN>","<ASSIGN>","<LOOP>","<CONDITION>","<COMMENT>","<EXP>","<D_A>"
           ,"<ID>","<SIGN_FN>","<L_R>","<C_N>","<C_F>","<C_S>","<C>"
           ,"<EXPP>","<T>","<TT>","<I>","<C_I>","<ID_A>"]
table={}
for i in range(0,len(list_G)):
    table[i]={}
    for j in t:
        if j!="landa" and j in list(list_G[i][1]):
            table[i][j]="S"+str(list_G[i][1][j])
        elif j=="landa" and j in list(list_G[i][1]):
            for k in list_G[i][0]:
                if k[1][0]=='.landa':
                    for p in k[2]:
                        table[i][p]="L"+str(list_G[i][1][j])
    for m in t2:
        if  m in list(list_G[i][1]):
            table[i][m]=str(list_G[i][1][m])
            
    for o in list_G[i][0]:
        if "."==o[1][-1][-1]:
            for k in o[2]:
                if k!="":
                    u=""
                    for d in o[1]:
                        if "." in d:
                            u+=","+d[:-1]
                        else:
                             u+=","+d
                    table[i][k]="R"+o[0]+u
                else:
                    table[i][k]="ACCEPTED"
stack=[0]
i=0
while i <len(token)+1:
    s=stack[-1]
    if i<len(token):
        if token[i] in table[s]:
            x=table[s][token[i]]
            if "S" ==x[0]:
                stack.append(token[i])
                stack.append(int(x[1:]))
                i+=1
            elif "R" ==x[0]:
                z = x[1:].split(",")
                if z[1]!="landa":
                    for j in range(0,2*(len(z)-1)):
                        stack.pop()
                    stack.append(z[0])
                    stack.append(int(table[stack[-2]][z[0]]))
                else:
                    stack.pop()
                    stack.append(z[0])
                    stack.append(int(table[stack[-2]][z[0]]))
            elif "L" ==x[0]:
                stack.append(int(x[1:]))
            print(stack)
        else:
            print(stack,"ERROR")
            i=len(token)+1
    else:
        print(table[s][""])
        i+=1
        



