from vec import *
from color_manager import *
import scipy.stats as stats
import numpy as np
from PIL import Image
from Robject import *
from Camera import *
from Material import *
from multiprocessing import Pool
import seaborn as sns
import random
import matplotlib.pyplot as plt
import time
def generatepic(resox=200,resoy=100,pswdeviation=0,randombit=2):
	lookfrom=Vector([0,0.5,0.2])
	lookat=Vector([0,0,-1])
	focus_dist=lookfrom-lookat
	focus_dist=focus_dist.length
	vup=Vector([0,1,0])
	camera=Camera(lookfrom,lookat,vup,100,400/200,0.05,focus_dist)

	x_reso=resox
	y_reso=resoy
	pic=np.zeros((y_reso,x_reso,3))
	#TheRNG=TRNG_Nbit_cube('skewed',randombit,pswdeviation)
	TheRNG=RNG_fromfile('randomsource.txt',randombit)
	robjectlist=[]
	robjectlist.append(Sphere(Vector([-0.5,0,-1]),0.5,Lambertian(Vector([0.8,0.3,0.3]),TheRNG)))
	robjectlist.append(Sphere(Vector([0,-100.5,-1]),100,Lambertian(Vector([0.8,0.8,0.0]),TheRNG)))
	robjectlist.append(Sphere(Vector([0.5,0,-1]),0.5,Metal(Vector([0.8,0.8,0.8]),0.3,TheRNG)))
	#robjectlist.append(Sphere(Vector([-1,0,-1]),-0.5,Dielectric(ri=1.5)))
	world=Robjectlist(robjectlist)
	gamma=2
	sample_num=75
	for j in range(0,x_reso):
		#print(j)
		for i in range(0,y_reso):
			pixel_color=Vector([0,0,0])
			for sample_index in range(0,sample_num):
				u=(j+random.random())/x_reso
				v=(i+random.random())/y_reso
				ray=camera.get_ray(u,v)
				pixel_color+=color(ray,world,0)*(1/(sample_num))
			rr=math.pow(pixel_color.x,1/gamma)
			gg=math.pow(pixel_color.y,1/gamma)
			bb=math.pow(pixel_color.z,1/gamma)
			pic[i,j,0]=int(rr*255.99)
			pic[i,j,1]=int(gg*255.99)
			pic[i,j,2]=int(bb*255.99)
	#im=Image.fromarray(pic.astype('uint8'),mode="RGB")
	#im=im.transpose(Image.FLIP_TOP_BOTTOM)
	#im.show()
	#im.save('./TRNG_fromfile.png')
	#print('=====')
	#print(TheRNG.repeat)
	#print(TheRNG.time)
	#print(TheRNG.pool.size)
	#print('=====')
	print('Random Vector Call Time',TheRNG.time)
	return pic

def standardgeneratepic(resox=200,resoy=100):
	lookfrom=Vector([0,0.5,0.2])
	lookat=Vector([0,0,-1])
	focus_dist=lookfrom-lookat
	focus_dist=focus_dist.length
	vup=Vector([0,1,0])
	camera=Camera(lookfrom,lookat,vup,100,400/200,0.05,focus_dist)

	x_reso=resox
	y_reso=resoy
	pic=np.zeros((y_reso,x_reso,3))
	TheRNG=RNG_cube()
	robjectlist=[]
	#robjectlist.append(Sphere(Vector([0,1,-1]),0.5,LightSource(Vector([15,15,15]))))
	robjectlist.append(Sphere(Vector([-0.5,0,-1]),0.5,Lambertian(Vector([0.8,0.3,0.3]),TheRNG)))
	robjectlist.append(Sphere(Vector([0,-100.5,-1]),100,Lambertian(Vector([0.8,0.8,0.0]),TheRNG)))
	robjectlist.append(Sphere(Vector([0.5,0,-1]),0.5,Metal(Vector([0.8,0.8,0.8]),0.3,TheRNG)))
	#robjectlist.append(Sphere(Vector([-1,0,-1]),-0.5,Dielectric(ri=1.5)))
	world=Robjectlist(robjectlist)
	gamma=2
	sample_num=75
	for j in range(0,x_reso):
		#print(j)
		for i in range(0,y_reso):
			pixel_color=Vector([0,0,0])
			for sample_index in range(0,sample_num):
				u=(j+random.random())/x_reso
				v=(i+random.random())/y_reso
				ray=camera.get_ray(u,v)
				pixel_color+=color(ray,world,0)*(1/(sample_num))
			rr=math.pow(pixel_color.x,1/gamma)
			gg=math.pow(pixel_color.y,1/gamma)
			bb=math.pow(pixel_color.z,1/gamma)
			pic[i,j,0]=int(rr*255.99)
			pic[i,j,1]=int(gg*255.99)
			pic[i,j,2]=int(bb*255.99)
	#im=Image.fromarray(pic.astype('uint8'),mode="RGB")
	#im=im.transpose(Image.FLIP_TOP_BOTTOM)
	#im.show()
	#im.save('./ref.png')
	#print(TheRNG.time)
	return pic

def calerror(matrix1,matrix2,resox,resoy):
	errr=0
	errg=0
	errb=0
	for i in range(0,resoy):
		for j in range(0,resox):
				errr1=(matrix1[i,j,0]-matrix2[i,j,0])**2
				errg1=(matrix1[i,j,1]-matrix2[i,j,1])**2
				errb1=(matrix1[i,j,2]-matrix2[i,j,2])**2
				errr+=errr1
				errg+=errg1
				errb+=errb1
	errr=math.sqrt(errr/(resox*resoy))
	errg=math.sqrt(errg/(resox*resoy))
	errb=math.sqrt(errb/(resox*resoy))
	return errr+errg+errb

def real_vec_distribution(bitnum,deviation):
	maxy=0.5

	randomvecpoolx=[]
	randomvecpooly=[]
	randomvecpoolz=[]

	randomvecpoolx_ref=[]
	randomvecpooly_ref=[]
	randomvecpoolz_ref=[]

	time_start=time.time()
	TheRNG=RNG_fromfile('randomsource.txt',bitnum)
	RNG_ref=RNG_cube()
	for i in range(0,100000):
		vecc=TheRNG.get_random_vec()
		randomvecpoolx.append(vecc.x)
		randomvecpooly.append(vecc.y)
		randomvecpoolz.append(vecc.z)

		vecc_ref=RNG_ref.get_random_vec()
		randomvecpoolx_ref.append(vecc_ref.x)
		randomvecpooly_ref.append(vecc_ref.y)
		randomvecpoolz_ref.append(vecc_ref.z)



	time_end=time.time()-time_start
	#title1='Vector distribution of {}-Bit TRNG (Psw deviation = {})'.format(bitnum,deviation)
	#title1='Vector distribution of spintronic RNG'
	plt.figure(figsize=(16,11))
	plt.rc('axes',labelsize=35,linewidth=2)

	#plt.suptitle(title1)


	weights=np.ones_like(randomvecpoolx)/len(randomvecpoolx)

	plt.subplot(311)
	plt.axis([-0.75,0.75,0,0.7])
	plt.xticks([-0.75,-0.5,-0.25,0,0.25,0.5,0.75],fontsize=34,position=(0,-0.01))
	#plt.xticks([],fontsize=34,position=(0,-0.01))
	ax=plt.gca()
	ax.axes.xaxis.set_ticklabels([])
	#ax.grid(True, linestyle='--',linewidth=0.5,color='black')
	plt.yticks([0.0,0.5],fontsize=34,position=(-0.01,0.01))
	plt.rc('axes',labelsize=35,linewidth=2)
	plt.hist(randomvecpoolx_ref,bins=20,range=(-1,1),color=sns.desaturate('grey',1),alpha=0.7,weights=weights)
	plt.hist(randomvecpoolx,bins=20,range=(-1,1),color=sns.desaturate('red',1),alpha=0.5,weights=weights)
	#plt.text(-0.9,0.4*maxy," \n100000 random vectors\n generated from spintronic RNG\n n = {}".format(bitnum))
	#plt.text(-0.9,0.4*maxy,"100 RNGs, each generates 1000 random vectors \n using Python's built-in random function")
	#plt.xlabel("X-value of random vectors")
	#plt.ylabel("Probability")
	plt.subplot(312)
	plt.axis([-0.75,0.75,0,0.7])
	plt.xticks([-0.75,-0.5,-0.25,0,0.25,0.5,0.75],fontsize=34,position=(0,-0.01))
	#plt.xticks([],fontsize=34,position=(0,-0.01))
	ax=plt.gca()
	ax.axes.xaxis.set_ticklabels([])
	#ax.grid(True, linestyle='--',linewidth=0.5,color='black')

	plt.yticks([0.0,0.5],fontsize=34,position=(-0.01,0.01))
	plt.rc('axes',labelsize=35,linewidth=2)
	plt.hist(randomvecpooly_ref,bins=20,range=(-1,1),color=sns.desaturate('grey',1),alpha=0.7,weights=weights)
	plt.hist(randomvecpooly,bins=20,range=(-1,1),color=sns.desaturate('blue',1),alpha=0.5,weights=weights)
	#plt.xlabel("Y-value of random vectors")
	#plt.ylabel("Probability",fontsize=50,position=(0,-0.03))
	plt.subplot(313)
	plt.axis([-0.75,0.75,0,0.7])
	plt.xticks([-0.75,-0.5,-0.25,0,0.25,0.5,0.75],fontsize=34,position=(0,-0.01))
	ax=plt.gca()
	#ax.grid(True, linestyle='--',linewidth=0.5,color='black')
	plt.yticks([0.0,0.5],fontsize=34,position=(-0.01,0.01))
	plt.rc('axes',labelsize=35,linewidth=2)
	plt.hist(randomvecpoolz_ref,bins=20,range=(-1,1),color=sns.desaturate('grey',1),alpha=0.7,weights=weights)
	plt.hist(randomvecpoolz,bins=20,range=(-1,1),color=sns.desaturate('green',1),alpha=0.5,weights=weights)
	#plt.xlabel("i-component of Rand_Vec (i=x,y,z)")
	#plt.ylabel("Probability")

	plt.subplots_adjust(hspace=0)
	title1="real_n_20231015{}".format(bitnum)
	title1=title1.replace('.','p')
	#title1="refence distribution"
	path="./"+str(title1)
	plt.savefig(path)



if __name__=='__main__':
	# ===================== generate one or multiple pics =================================

	print('generating pic')
	# pic1=standardgeneratepic(200,100)
	pic2=generatepic(200,100,randombit=2)
	# pic3=generatepic(200,100,randombit=4)
	# pic4=generatepic(200,100,randombit=8)
	# pic5=generatepic(200,100,randombit=16)
	#
	print('generated')
	#
	# #im=Image.fromarray(pic1.astype('uint8'),mode="RGB")
	im=Image.fromarray(pic2.astype('uint8'),mode="RGB")
	im=im.transpose(Image.FLIP_TOP_BOTTOM)
	im.show()
	# im.save('./real2.png')
	# err=calerror(pic1,pic2,200,100)
	# print('err2: ',err)
	#
	# im=Image.fromarray(pic3.astype('uint8'),mode="RGB")
	# im=im.transpose(Image.FLIP_TOP_BOTTOM)
	# im.show()
	# im.save('./real4.png')
	# err=calerror(pic1,pic3,200,100)
	# print('err4: ',err)
	#
	# im=Image.fromarray(pic4.astype('uint8'),mode="RGB")
	# im=im.transpose(Image.FLIP_TOP_BOTTOM)
	# im.show()
	# im.save('./real8.png')
	# err=calerror(pic1,pic4,200,100)
	# print('err8: ',err)
	#
	# im=Image.fromarray(pic5.astype('uint8'),mode="RGB")
	# im=im.transpose(Image.FLIP_TOP_BOTTOM)
	# im.show()
	# im.save('./real16.png')
	# err=calerror(pic1,pic5,200,100)
	# print('err16: ',err)


	#========================vec distribution=========================

	#bitnums=[2,4,8,16]
	#bitnums=[2]
	#for bit in bitnums:
	#	print('ee')
	#	real_vec_distribution(bit,1)
	#real_vec_distribution(16,1)

	#========================real psw deviation=========================

	#bitnums=[2,4,8,16]
	#for bit in bitnums:
	#	print('ee')
	#	TheRNG=RNG_fromfile('randomsource.txt',bit)
	#	print(TheRNG.get_psw_deviation(n=bit))
	#========================picture comparison=========================
	# exp=[]
	# bitlist=[2,4,8]
	# deviationlist=[0.001,0.1,0.2,0.3,0.4]
	# #bitlist=[8]
	# #deviationlist=[0.4]
	#
	# trailnum=10
	# for bitnumber in bitlist:
	# 	standardpic=standardgeneratepic(200,100)
	# 	print("generated standard pic with bitnum=  ",bitnumber)
	# 	can=[]
	# 	for deviation in deviationlist:
	# 		print("deviation=  ",deviation)
	# 		error=0
	# 		retlist=[]
	# 		resultpics=[]
	# 		poool=Pool(10)
	# 		for trialcount in range(0,trailnum):
	# 			print("test number  ",trialcount)
	# 			ret=poool.apply_async(generatepic, args=(200,100,deviation,bitnumber))
	# 			retlist.append(ret)
	# 		for ret1 in retlist:
	# 			resultpics.append(ret1.get())
	# 		for resultpic in resultpics:
	# 			error+=calerror(resultpic,standardpic,resox=200,resoy=100)/trailnum
	# 		print("error is: ",error)
	# 		can.append(error)
	# 	exp.append(can)
	# print("final result: ", exp)


	#=========================vector generation========================

	# bitnum=8
	# deviation=0.2   #0.001， 0.2，0.499
	# maxy=0.1
	#
	# randomvecpoolx=[]
	# randomvecpooly=[]
	# randomvecpoolz=[]
	#
	# time_start=time.time()
	# for j in range(0,100):
	# 	#TheRNG=TRNG_Nbit_cube('skewed',bitnum,deviation)
	# 	TheRNG=RNG_cube()
	# 	for i in range(0,1000):
	# 		vecc=TheRNG.get_random_vec()
	# 		randomvecpoolx.append(vecc.x)
	# 		randomvecpooly.append(vecc.y)
	# 		randomvecpoolz.append(vecc.z)
	#
	# time_end=time.time()-time_start
	# #title1='Vector distribution of {}-Bit TRNG (Psw deviation = {})'.format(bitnum,deviation)
	# title1='Vector distribution of PRNG'
	# plt.figure(figsize=(5,5))
	# plt.suptitle(title1)
	#
	#
	# weights=np.ones_like(randomvecpoolx)/len(randomvecpoolx)
	#
	# plt.subplot(311)
	# plt.axis([-1,1,0,maxy])
	# plt.hist(randomvecpoolx,bins=20,range=(-1,1),color=sns.desaturate('red',1),alpha=0.5,weights=weights)
	# plt.text(-0.9,0.4*maxy,"100 RNGs, each generates 1000 random vectors \n(within unit cube) \n execution time: {}s".format(str(round(time_end,3))))
	# plt.xlabel("X-value of random vectors")
	# plt.ylabel("Probability")
	# plt.subplot(312)
	# plt.axis([-1,1,0,maxy])
	# plt.hist(randomvecpooly,bins=20,range=(-1,1),color=sns.desaturate('blue',1),alpha=0.5,weights=weights)
	# plt.xlabel("Y-value of random vectors")
	# plt.ylabel("Probability")
	# plt.subplot(313)
	# plt.axis([-1,1,0,maxy])
	# plt.hist(randomvecpoolz,bins=20,range=(-1,1),color=sns.desaturate('green',1),alpha=0.5,weights=weights)
	# plt.xlabel("Z-value of random vectors")
	# plt.ylabel("Probability")
	#
	# plt.subplots_adjust(hspace=0.5)
	#
	# path="./distribution/"+str(hash(title1))
	# plt.savefig(path)



# ===================== real pic average MSE =================================

	# bitnums=[2,4,8,16]
	# for bitnum in bitnums:
	# 	avgerr=0
	# 	for i in range(0,10):
	# 		refpic=standardgeneratepic(200,100)
	# 		tocomparedpic=generatepic(200,100,randombit=bitnum)
	# 		err=calerror(refpic,tocomparedpic,200,100)
	# 		avgerr+=err/10
	# 	print(bitnum,avgerr)
