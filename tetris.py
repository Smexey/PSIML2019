import numpy as np

import copy

# path = input()
path = "C:\\Users\\pajse\\Desktop\\publictetr\\set\\9.txt"

f = open(path,'r')
mat = []
for i in range(20):
    line = f.readline()
    temp = []
    for char in line:
        if char!='\n':
            temp.append(char)
    mat.append(temp)

mat = np.array(mat)

blocks = []
tempmat=[]
for line in f:
    if line =='\n' or len(line) == 0:
        if len(tempmat)>0:
            
            blocks.append(np.array(tempmat))
            tempmat=[]
    

    temp = []
    for char in line:
        if char!='\n':
            temp.append(char)
    if len(temp)>0:
        tempmat.append(temp)


if len(tempmat)>0:
    
    blocks.append(np.array(tempmat))
    tempmat=[]
    
#kraj ucitavanja



def allrotas(block):
    #print(block)
    returner = []
    returner.append(block)
    for i in range(1,4):
        
        returner.append(np.rot90(returner[i-1]))
        #print(returner[i])

    return returner

def score(mat):
    suma=0
    for l in mat:
        flag=True
        for char in l:
            if char==' ':
                flag = False
        if flag==True:
            suma+=1
    return suma



def makenew(mat,block,offsety,offsetx):
    newmat = copy.copy(mat)

    #za out of bounds
    if offsety+len(block)>len(mat) or offsetx+len(block[0])>len(mat[0]):
        newmat[0][0]= 'Q'
        return newmat
    
    for i in range(len(block)):
        for j in range(len(block[i])):
            if newmat[i+offsety][j+offsetx] ==' ':
                if block[i][j]=='#':
                    newmat[i+offsety][j+offsetx] = '#'
            else:
                if block[i][j]=='#':
                    newmat[0][0]= 'Q'
                    return newmat

    return newmat


max_score = -1
max_r = 0
max_c = 0
block_index = 0

for counter,lala in enumerate(blocks):
    for r,block in enumerate(allrotas(lala)):
        for x in range(10-len(block[0])+1):
            y=0
            #IZMENITI OVO DA RADI KAKO TREBA ZA OBA TASKA
            #print(block)
            while makenew(mat,block,y,x)[0][0]!= 'Q':
                #print(makenew(mat,block,y,x))
                y+=1
            
            y-=1
            newmat = makenew(mat,block,y,x)
            if score(newmat)>max_score:
                #print("VTP")
                print(newmat)
                print(block)
                max_score = score(newmat)
                print(max_score)
                max_r = r
                max_c = x
                block_index = counter
    

print(block_index,max_r*90,max_c)
#task2

max_score = -1
max_r = 0
max_c = 0
block_index = 0
max_s = ''

for counter,lala in enumerate(blocks):
    for r,block in enumerate(allrotas(lala)):
        for x in range(10-len(block[0])+1):
            #za svaku start poz
            s = ''
            y=0
            cangoleft = False
            wentdown = False
            while True:
                moveddown = False
                while makenew(mat,block,y,x)[0][0]!= 'Q':
                    #ide na dole do kolizije
                    moveddown = True
                    y+=1

                #vrati se unazad jednu
                if moveddown: y-=1

                x1 = x
                while makenew(mat,block,y,x1)[0][0]!= 'Q' and wentdown == False:
                    print(makenew(mat,block,y,x1))
                    #ide na desno do kolizije ili ako moze na dole?
                    if makenew(mat,block,y+1,x1)[0][0]!='Q':
                        s+=str(x1-x)
                        cangoleft = True
                        wentdown = True
                        y+=1
                        
                    x1+=1

                #ako se pomerao u desno
                if x1!=x: x1-=1

                if wentdown==False and cangoleft == True:
                    x1 = x
                    while makenew(mat,block,y,x1)[0][0]!= 'Q':
                        #ide na LEVO do kolizije ili ako moze na dole?
                        if makenew(mat,block,y+1,x1)[0][0]!='Q':
                            s+=str(x1-x)
                            cangoleft = True
                            wentdown = True
                            y+=1
                        x1-=1
                    x1+=1
                #jel mi treba ovaj uslov?
                if wentdown == False:
                    newmat = makenew(mat,block,y,x1)
                    if score(newmat)>max_score:
                        #print("VTP")
                        print(newmat)
                        print(block)
                        max_score = score(newmat)
                        print(max_score)
                        max_r = r
                        max_c = x
                        block_index = counter
                        max_s = str(block_index) + " " + str(max_r*90)+ ' ' + s
                        print("maxs je",max_s)
                    break
                
    
print(max_s)



