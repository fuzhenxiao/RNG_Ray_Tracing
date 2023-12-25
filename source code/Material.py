import math
import scipy.stats as stats
import numpy as np
from vec import *
import random
#========================virtual RNGs are defined below=================

def betadistribution(minv,maxv,mean,std):
    scale=maxv-minv
    loca=minv
    unscaledmean=(mean-minv)/scale
    unscaledvar=(std/scale)**2
    t=unscaledmean/(1-unscaledmean)
    beta=((t/unscaledvar)-(t*t)-2*t-1)/((t*t*t)+(3*t*t)+(3*t)+1)
    alpha=beta*t
    if alpha<=0 or beta<=0:
        print("this is a meaningless distribution")
    return stats.beta(alpha,beta,scale=scale,loc=loca)

class SkewedMTJ(object):
    def __init__(self,prob):
        #self.prob_1=random.random()
        self.prob_1=prob
        self.prob_0=1-self.prob_1
    def get_bit(self):
        x=random.random()
        if x < self.prob_1:
            return 1
        else:
            return 0
    
class StandardMTJ(object):
    def __init__(self):
        self.prob_1=0.5
        self.prob_0=0.5
    def get_bit(self):
        x=random.random()
        if x < self.prob_1:
            return 1
        else:
            return 0

class TRNG_4bit(object): #1 sign bit, 3 fixed point floating bit
    def __init__(self,type="standard"): # standard or skewed
        if type=="standard":
            self.mtj1=StandardMTJ()
            self.mtj2=StandardMTJ()
            self.mtj3=StandardMTJ()
            self.mtj4=StandardMTJ()
        else:
            self.mtj1=SkewedMTJ()
            self.mtj2=SkewedMTJ()
            self.mtj3=SkewedMTJ()
            self.mtj4=SkewedMTJ()
            print(self.mtj1.prob_1)
            print(self.mtj2.prob_1)
            print(self.mtj3.prob_1)
            print(self.mtj4.prob_1)
    def get_random_vec(self):
        vec=[]
        for i in range(0,3):
            bit1=self.mtj1.get_bit()
            bit2=self.mtj2.get_bit()
            bit3=self.mtj3.get_bit()
            bit4=self.mtj4.get_bit()
            value=bit1*(-1)+2**((-1)*bit2)+2**((-2)*bit3)+2**((-3)*bit4)
            vec.append(value)
        return Vector(vec)


class TRNG_Nbit(object): #1 sign bit, 3 fixed point floating bit
    def __init__(self,type="standard",bitn=4,deviation=0): # standard or skewed
        if type=="standard":
            self.MTJlist=[]
            for i in range(0,bitn):
                self.MTJlist.append(StandardMTJ())
        else:
            self.deviation=deviation
            self.MTJlist=[]
            for i in range(0,bitn):
                if self.deviation==0:
                    someprob=0.5
                else:
                    someprobsource=betadistribution(0,1,0.5,self.deviation)
                    someprob=someprobsource.rvs(1)
                if someprob<0:
                    someprob=0
                elif someprob>1:
                    someprob=1
                else:
                    someprob=someprob
                self.MTJlist.append(SkewedMTJ(prob=someprob))
    def get_probs(self):
        for item in self.MTJlist:
            print(item.prob_1)
    def get_random_vec(self):
        flag=True
        vec=[]
        while flag:
            rawvec=[]
            for i in range(0,3):
                value=0
                for j in range(1,len(self.MTJlist)):
                    value+= (2**((-1)*j))*(self.MTJlist[j].get_bit())
                if self.MTJlist[0].get_bit()==0:
                    value=(-1)*value #neg
                else:
                    value=1*value  #pos
                rawvec.append(value)
            vec=Vector(rawvec)
            if vec*vec>1:
                flag=True
            else:
                flag=False
        return vec




class RNG(object):
    def __init__(self):
        self.type="normalRNG"

    def get_random_vec(self):
        flag=True
        raw=None
        while flag:
            raw=Vector([2*random.random()-1,2*random.random()-1,2*random.random()-1])
            if raw*raw>1:
                flag=True
            else:
                flag=False
        return raw

class TRNG_Nbit_cube(object): #1 sign bit, 3 fixed point floating bit
    def __init__(self,type="standard",bitn=4,deviation=0): # standard or skewed
        if type=="standard":
            self.MTJlist=[]
            for i in range(0,bitn):
                self.MTJlist.append(StandardMTJ())
        else:
            self.deviation=deviation
            self.MTJlist=[]
            for i in range(0,bitn):
                if self.deviation==0:
                    someprob=0.5
                else:
                    someprobsource=betadistribution(0,1,0.5,self.deviation)
                    someprob=someprobsource.rvs(1)
                if someprob<0:
                    someprob=0
                elif someprob>1:
                    someprob=1
                else:
                    someprob=someprob
                self.MTJlist.append(SkewedMTJ(prob=someprob))
    def get_probs(self):
        for item in self.MTJlist:
            print(item.prob_1)
    def get_random_vec(self):
        vec=[]
        for i in range(0,3):
            value=0
            for j in range(1,len(self.MTJlist)):
                value+= (2**((-1)*j))*(self.MTJlist[j].get_bit())
            if self.MTJlist[0].get_bit()==0:
                value=(-1)*value #neg
            else:
                value=1*value  #pos
            vec.append(value)
        vec=Vector(vec)*(1/math.sqrt(3))
        return vec




class RNG_cube(object):
    def __init__(self):
        self.type="normalRNG"
        self.time=0

    def get_random_vec(self):
        self.time+=1
        raw=Vector([2*random.random()-1,2*random.random()-1,2*random.random()-1])
        raw=raw*(1/math.sqrt(3))
        return raw
class RNG_fromfile(object):
    def __init__(self,file='filepath',bitnum=4):
        self.type='fromfile'
        self.file=file
        print('loading randombits')
        #self.pool=np.loadtxt(file)
        with open(file, "r", encoding='utf-8') as f:  
            data= f.read()   
        acan=[]
        for i in range(0,len(data)):
            if data[i]=="1":
                acan.append(1)
            else:
                acan.append(0)
        self.pool=np.array(acan)

        print('random bits loaded')
        self.pointer=1
        self.time=0
        self.bitnum=bitnum
        self.repeat=0
    def get_psw_deviation(self,n=2):
        cans=[]
        for i in range(0,n):
            cans.append([])
        for j in range(0,len(self.pool)):
            index=j%n
            cans[index].append(self.pool[j])
        Psws=[]
        for k in range(0,n):
            onelist=np.array(cans[k])
            pswofthislist=onelist.mean()
            Psws.append(pswofthislist)
        Psws=np.array(Psws)
        pswdev=np.std(Psws)
        return pswdev

    def get_random_vec(self):
        self.time+=1
        if self.pointer+self.bitnum*3>=self.pool.size:
            self.pointer=1
            self.repeat+=1
        xs=self.pool[self.pointer:self.pointer+self.bitnum]
        self.pointer+=self.bitnum
        ys=self.pool[self.pointer:self.pointer+self.bitnum]
        self.pointer+=self.bitnum
        zs=self.pool[self.pointer:self.pointer+self.bitnum]
        self.pointer+=self.bitnum


        x=0
        for j in range(1,len(xs)):
            x+= (2**((-1)*j))*(xs[j])
        if xs[0]==0:
            x=(-1)*x #neg
        else:
            x=1*x  #pos

        y=0
        for j in range(1,len(xs)):
            y+= (2**((-1)*j))*(ys[j])
        if ys[0]==0:
            y=(-1)*y #neg
        else:
            y=1*y  #pos

        z=0
        for j in range(1,len(xs)):
            z+= (2**((-1)*j))*(zs[j])
        if zs[0]==0:
            z=(-1)*z #neg
        else:
            z=1*z  #pos

        vec=[x,y,z]
        #print(vec)
        vec=Vector(vec)*(1/math.sqrt(3))
        return vec

#=====================================materials are defined below==========================================
class LightSource(object):
    def __init__(self,attenuation):
        self.attenuation=attenuation
        self.scattered=None
    def scatter(self,ray_in,hitrecord):
        return False
    def emitted(self):
        return self.attenuation
        
class Lambertian(object):
    def __init__(self,attenuation,RNG):
        self.attenuation=attenuation #it is a vec
        self.target=None
        self.scattered=None
        #self.RNG=RNG()
        self.RNG=RNG
        #self.RNG.get_probs()
    def scatter(self,ray_in,hitrecord):
        rec=hitrecord
        self.target=rec.normal+self.RNG.get_random_vec()
        self.scattered=Ray(rec.p,self.target) # added rec.p above but subtracted rec.p here, It is meaningless
        return True
    def emitted(self,):
        return Vector([0,0,0])

class Metal(object):
    def __init__(self,attenuation,fuzz,RNG):
        self.attenuation=attenuation
        self.reflected=None
        self.scattered=None
        self.fuzz=fuzz
        #self.RNG=RNG()
        self.RNG=RNG
        #self.RNG.get_probs()
    def scatter(self,rayin,hitrecord):
        rec=hitrecord
        self.reflected=reflect(rayin.direction.unify(),rec.normal)
        self.scattered=Ray(rec.p,self.reflected+self.fuzz*self.RNG.get_random_vec())
        return ((self.scattered.direction*rec.normal)>0)
    def emitted(self,):
        return Vector([0,0,0])
class Dielectric(object):
    def __init__(self,ri):
        self.ref_idx=ri
        self.attenuation=Vector([1,1,1])
        self.scattered=None
    def scatter(self,ray_in,hitrecord):
        rec=hitrecord
        reflected=reflect(ray_in.direction,rec.normal)
        if ray_in.direction*rec.normal>0:
            outward_normal=-1*rec.normal
            n=self.ref_idx
            cosine=self.ref_idx*(ray_in.direction*rec.normal)*1/ray_in.direction.length
        else:
            outward_normal=rec.normal
            n=1/self.ref_idx
            cosine=-1*(ray_in.direction*rec.normal)/ray_in.direction.length
        refract_result=refract(ray_in.direction,outward_normal,n)
        if (refract_result[0]):
            r0=(1-self.ref_idx)/(1+self.ref_idx) * (1-self.ref_idx)/(1+self.ref_idx)
            reflect_probe=r0+(1-r0)*math.pow((1-cosine),5)
        else:
            self.scattered=Ray(rec.p,reflected)
            reflect_probe=1
        if (random.random()<reflect_probe):
            self.scattered=Ray(rec.p,reflected)
        else:
            self.scattered=Ray(rec.p,refract_result[1])
        return True
    def emitted(self,):
        return Vector([0,0,0])
