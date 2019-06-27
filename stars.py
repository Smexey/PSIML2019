from PIL import Image
import numpy as np
from PIL import ImageChops
import copy

pathsrc = input()
pathdst = input()

star1 = input()
star1 = list(star1.split())
star1 = (int(star1[0]),int(star1[1]))
    

star2 = input()
star2 = list(star2.split())
star2 = (int(star2[0]),int(star2[1]))
 
star3 = input()
star3 = list(star3.split())
star3 = (int(star3[0]),int(star3[1]))
 
#######################################################

# pathsrc = "C:\\Users\\pajse\\Desktop\\publicstar\\set\\9_src.png"
# pathdst = "C:\\Users\\pajse\\Desktop\\publicstar\\set\\9_dst.png"

# star1 = (66, 293)
# star2 = (560, 592)
# star3 = (766, 743)

# pathsrc = "C:\\Users\\pajse\\Desktop\\publicstar\\set\\0_src.png"
# pathdst = "C:\\Users\\pajse\\Desktop\\publicstar\\set\\0_dst.png"

# star1 = (937.000000, 274.000000)
# star2 = (283.000000, 986.000000)
# star3 = (563.000000, 475.000000)


# pathsrc = "C:\\Users\\pajse\\Desktop\\publicstar\\set\\4_src.png"
# pathdst = "C:\\Users\\pajse\\Desktop\\publicstar\\set\\4_dst.png"

# star1 = (62.000000, 147.000000)
# star2 = (831.000000, 995.000000)
# star3 = (531.000000, 63.000000)



imgsrc = Image.open(pathsrc)

imgdst = Image.open(pathdst)

imgsrcold = copy.copy(imgsrc)

t = imgsrc.getbbox()
newimsrc = imgsrc.crop(t)
imgsrc=newimsrc.resize(imgsrc.size)



r=0
mean_min=200
size_min = imgsrc.size

for alfa in np.linspace(0,360,360):
    newim = imgdst.rotate(alfa)
    t = newim.getbbox()
    
    newim = newim.crop(t)
    newsize = newim.size
    newim = newim.resize(imgsrc.size)
    d = ImageChops.difference(imgsrc, newim)
    newmean = np.mean(d)

    if newmean<mean_min:
        mean_min = newmean
        r = alfa
        size_min = newsize
        
r1=r

for alfa in np.linspace(r1-1,r1+1,200):
    newim = imgdst.rotate(alfa)
    t = newim.getbbox()
    
    newim = newim.crop(t)
    newsize = newim.size
    newim = newim.resize(imgsrc.size)
    d = ImageChops.difference(imgsrc, newim)
    newmean = np.mean(d)

    if newmean<mean_min:
        mean_min = newmean
        r = alfa
        size_min = newsize
  
coords_src_center = imgsrcold.getbbox()
#print(coords_src_center)



#print(coords_src_center)
coords_src_center = (((coords_src_center[0]+coords_src_center[2])/2),((coords_src_center[1]+coords_src_center[3])/2))

#print(coords_src_center)



newim = imgdst.rotate(r)
#newim.save('out.bmp')
coords_newim_center = newim.getbbox()
coords_newim_center = (((coords_newim_center[0]+coords_newim_center[2])/2),((coords_newim_center[1]+coords_newim_center[3])/2))
#print(coords_newim_center)

#brv pavle majstore
r = 360-r
#print(r)

#print(size_min)
#print(newimsrc.size)
scale = size_min[0]/newimsrc.size[0]
#print(scale)


#print(coords_newim_center)
coords_newim_center = np.subtract(coords_newim_center,np.divide(imgsrcold.size,2))

#print(coords_newim_center)

coords_newim_center = [coords_newim_center[0]*np.cos(np.pi*(360-r)/180) - coords_newim_center[1]*np.sin(np.pi*(360-r)/180),
                        coords_newim_center[0]*np.sin(np.pi*(360-r)/180) + coords_newim_center[1]*np.cos(np.pi*(360-r)/180)]

coords_newim_center = np.add(coords_newim_center,np.divide(imgsrcold.size,2))

#print(coords_newim_center)

def finddst(star1,r):

    
    delta_star1 = (np.subtract(star1,coords_src_center))
    #print(delta_star1)
    delta_star1 = (np.multiply(delta_star1,scale))
    #print(delta_star1)

    


    delta_star1 = [delta_star1[0]*np.cos(np.pi*(360-r)/180) - delta_star1[1]*np.sin(np.pi*(360-r)/180),
                            delta_star1[0]*np.sin(np.pi*(360-r)/180) + delta_star1[1]*np.cos(np.pi*(360-r)/180)]

    coords_star1 = np.add(delta_star1,coords_newim_center)
    #print(coords_star1)
    #print("----")
    return coords_star1


def iscircle(img,x,y):
    if img.getpixel((x,y)) != 255:
        return False
    elif img.getpixel((x-30,y+30))==0:
        return False
    elif img.getpixel((x-15,y))==0:
        return False
    return True

def isstar(img,x,y):
    if img.getpixel((x,y)) != 255:
        return False
    elif img.getpixel((x+30,y))==0:
        return False
    return True

def iscross(img,x,y):
    if img.getpixel((x,y)) != 255:
        return False
    return True

def isspiral(img,x,y):
    if img.getpixel((x,y+7)) != 255:
        return False
    return True

def isdonut(img,x,y):
    if img.getpixel((x,y+32)) != 255:
        return False
    return True

def isflower(img,x,y):
    if img.getpixel((x,y+32))==0 and img.getpixel((x-15,y))==255:
        return True
    return False



img = imgsrcold
#img.show()
width,height = img.size
tmp = []
for i in range(64,width,128):
    for j in range(64,height,128):
        if iscircle(img,i,j):
            tmp.append(('circle',i,j))
            #print('circle',i,j)
            continue
        elif isstar(img,i,j):
            tmp.append(('star',i,j+5))
            #print('star',i,j)
            continue
        elif iscross(img,i,j):
            tmp.append(('cross',i,j))
            #print('cross',i,j)
            continue
        elif isspiral(img,i,j):
            tmp.append(('spiral',i-3,j-2))
            #print('spiral',i,j)
            continue
        elif isdonut(img,i,j):
            tmp.append(('donut',i,j))
            #print('donut',i,j)
            continue
        elif isflower(img,i,j):
            tmp.append(('flower',i,j))
            #print('flower',i,j)
            continue
        else:
            #print(i,j)
            pass


s=''
for i in range(len(tmp)):
    s+=str(tmp[i][1]) + ' '+ str(tmp[i][2])
    if i!= (len(tmp)-1):
        s+=' '
print(s)

s=''
for i in range(len(tmp)):
    x = finddst((tmp[i][1],tmp[i][2]),r)
    s+=str(int((x[0]))) + ' ' + str(int((x[1])))
    if i!= (len(tmp)-1):
        s+=' '
print(s)

s=''
for i in range(len(tmp)):
    s+=tmp[i][0]
    if i!= (len(tmp)-1):
        s+=' '
print(s)
print(s)

# ####
# for i in range(len(tmp)):
#     x = finddst((tmp[i][1],tmp[i][2]),r)
#     print(tmp[i],x)
#     if i!= (len(tmp)-1):
#         s+=' '

# ####

temp1 = finddst(star1,r)
temp2 = finddst(star2,r)
temp3 = finddst(star3,r)

print(int(round(temp1[0])),int(round(temp1[1])), int(round(temp2[0])),int(round(temp2[1])),int(round(temp3[0])),int(round(temp3[1])))
