from vec import *
import math
import random

def random_vec_on_unitdisk():
    raw=Vector([2*random.random()-1,2*random.random()-1,0])
    if raw*raw>1:
        return raw*(1/1.415)
    else:
        return raw
class Camera(object):
    def __init__(self,lookfrom,lookat,vup,vfov,aspect,aperture,focus_dist):
        theta=vfov*math.pi/180
        self.lens_radius=aperture/2
        half_height=math.tan(theta/2)
        half_width=aspect*half_height
        self.origin=lookfrom
        w=(lookfrom-lookat).unify()
        self.u=cross(vup,w).unify()
        self.v=cross(w,self.u)

        self.lower_left_corner=self.origin-focus_dist*half_width*self.u-self.v*focus_dist*half_height-focus_dist*w
        self.horizontal=2*focus_dist*half_width*self.u
        self.vertical=2*focus_dist*half_height*self.v

    def get_ray(self,u,v):
        rd=self.lens_radius*random_vec_on_unitdisk()
        offset=self.u*rd.x+self.v*rd.y
        return Ray(self.origin+offset,self.lower_left_corner+u*self.horizontal+v*self.vertical-self.origin-offset)
