from vec import *
from Robject import *
import random
import math
def random_smaller_than_unit_vec():
    raw=Vector([2*random.random()-1,2*random.random()-1,2*random.random()-1])
    if raw*raw>=1:
        return raw*(1/1.5)
    else:
        return raw

def color(ray,world,depth):  #world is a robject list
    if world.hit(ray,0.0,float("inf")):
        rec=world.hitrecord
        emitted=rec.material.emitted()
        if (depth<50)&(rec.material.scatter(ray,rec)):
            return emitted+mul_trans(rec.material.attenuation,color(rec.material.scattered,world,depth+1))
        else:
            #return emitted  #too much reflection gives darkness
            return emitted


    else:
        u_ray=ray.direction
        u_ray.unify()
        t=0.5*(u_ray.y+1)
        return Vector([(1-t)*1+0.5*t,(1-t)*1+0.7*t,(1-t)*1+t])
        #return Vector([0,0,0])
