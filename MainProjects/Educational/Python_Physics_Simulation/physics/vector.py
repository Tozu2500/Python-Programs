import math

class Vector2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)
    
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)
    
    def __neg__(self):
        return Vector2D(-self.x, -self.y)
    
    def __repr__(self):
        return f"Vector2D({self.x:.2f}, {self.y:.2f})"
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def cross(self, other):
        return self.x * other.y - self.y * other.x
    
    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def magnitude_squared(self):
        return self.x * self.x + self.y * self.y
    
    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return Vector2D(self.x / mag, self.y / mag)
        return Vector2D(0, 0)
    
    def normalized(self):
        return self.normalize()
    
    def distance_to(self, other):
        return (self - other).magnitude()
    
    def distance_squared_to(self, other):
        return (self - other).magnitude_squared()
    
    def rotate(self, angle_rad):
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return Vector2D(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
    
    def angle(self):
        return math.atan2(self.y, self.x)
    
    def perpendicular(self):
        return Vector2D(-self.y, self.x)
    
    def project_onto(self, other):
        other_mag_sq = other.magnitude_squared()
        if other_mag_sq == 0:
            return Vector2D(0, 0)
        scalar = self.dot(other) / other_mag_sq
        return other * scalar
    
    def reflect(self, normal):
        normal_normalized = normal.normalized()
        return self - normal_normalized * (2 * self.dot(normal_normalized))
    
    def copy(self):
        return Vector2D(self.x, self.y)
    
    @staticmethod
    def zero():
        return Vector2D(0, 0)
    
    @staticmethod
    def from_angle(angle_rad, magnitude=1.0):
        return Vector2D(math.cos(angle_rad) * magnitude, math.sin(angle_rad) * magnitude)