import math
#===========================defines some critical vector operations==================

class Vector(object):
    def __init__(self, vec):
        if vec is None:
            print("You sent me a None vec noob !")
        self.x = vec[0]
        self.y = vec[1]
        self.z = vec[2]
        self.length = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __add__(self, other):
        return Vector([self.x + other.x, self.y + other.y, self.z + other.z])

    def __sub__(self, other):
        return Vector([self.x - other.x, self.y - other.y, self.z - other.z])

    def unify(self):
        return Vector([self.x / self.length, self.y / self.length, self.z / self.length])

    def __mul__(self, other):
        if type(other) == type(self):
            return self.x * other.x+self.y * other.y+self.z * other.z
        else:
            return Vector([self.x * other, self.y * other, self.z * other])

    __rmul__ = __mul__

def reflect(vecin,vecn):
    return vecin-2*(vecin*vecn)*vecn
def refract(vecin,vecn,n):   # used in glasses, water, and things like that
    unit_vecin=vecin.unify()
    dot_product=unit_vecin*vecn
    discriminant=1-n*n*(1-dot_product*dot_product)
    if discriminant>0:
        refracted = n*(vecin-vecn*dot_product)-vecn*math.sqrt(discriminant)
        return [True, refracted]
    else:
        return [False, None]

def cross(vec1, vec2):
    xx = (vec1.y * vec2.z - vec2.y * vec1.z)
    yy = (vec2.x * vec1.z - vec1.x * vec2.z)
    zz = (vec1.x * vec2.y - vec2.x * vec1.y)
    vecout = Vector([xx, yy, zz])
    return vecout
def mul_trans(vec1, vec2):
    return Vector([vec1.x*vec2.x,vec1.y*vec2.y,vec1.z*vec2.z])

class Ray(object):
    def __init__(self, origin, direction):  # origin and direction are vec3
        self.origin = origin
        self.direction = direction

    def point_at_para(self, t):
        return self.origin + t * self.direction
