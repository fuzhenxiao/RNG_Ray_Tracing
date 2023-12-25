from vec import *
import math


# I call it Robject (Ray-hitable-Object) because "Object" has been occupied by Python itself

class Hitrecord(object):  # this is used for transporting hit point info
    def __init__(self, t, p, normal,material):
        self.t = t
        self.p = p
        self.normal = normal
        self.material=material

class Robjectlist(object):
    def __init__(self,listofrobjects):
        self.robjectlist=listofrobjects
        self.hitrecord=Hitrecord(None,None,None,None)
    def hit(self,ray,tmin,tmax):
        hit_anything=False
        closest_so_far=tmax
        for i in self.robjectlist:   #this "i" is an robject like a sphere
            if i.hit(ray, tmin,closest_so_far):
                hit_anything=True
                closest_so_far=i.hitrecord.t
                self.hitrecord=i.hitrecord
        return hit_anything


class Sphere(object):
    def __init__(self, center, radius,material):
        # center is a Vec and radius is float
        self.center = center
        self.r = radius
        self.hitrecord=Hitrecord(None,None,None,material)

    def hit(self, ray, tmin, tmax):
        oc = ray.origin - self.center
        a = ray.direction * ray.direction
        b = oc * ray.direction
        c = oc * oc - self.r * self.r
        discriminant = b * b - a * c
        if discriminant > 0:
            temp = (-b - math.sqrt(discriminant)) / a
            if (temp < tmax) & (temp > tmin):
                self.hitrecord.t = temp
                self.hitrecord.p = ray.point_at_para(self.hitrecord.t)
                self.hitrecord.normal = (self.hitrecord.p - self.center)*(1 / self.r)
                return True
            temp = (-b + math.sqrt(discriminant)) / a
            if (temp < tmax) & (temp > tmin):
                self.hitrecord.t = temp
                self.hitrecord.p = ray.point_at_para(self.hitrecord.t)
                self.hitrecord.normal = (self.hitrecord.p - self.center)*(1 / self.r)
                return True
        else:
            return False
class Rectangle(object):
    def __init__(self,x0,y0,x1,y1,k,material):
        self.x0=x0
        self.y0=y0
        self.x1=x1
        self.x0=x0
        self.k=k
        self.hitrecord=Hitrecord(None,None,None,material)
    def hit(self,ray,tmin,tmax): # tmin tmax is close to thickness
        t=(self.k-ray.origin.z)/ray.direction.z
        if (t<tmin)|(t>tmax):
            return False
        x=ray.origin.x+t*ray.direction.x
        y=ray.origin.y+t*ray.direction.y
        if (x<self.x0) or (x>self.x1) or (y<self.y0) or (y>self.y1):
            return False
        self.hitrecord.t=t
        self.hitrecord.p=ray.point_at_para(t)
        self.hitrecord.normal=Vector([0,0,1])
        return  True



