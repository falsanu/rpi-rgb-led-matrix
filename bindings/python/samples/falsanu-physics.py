#!/usr/bin/env python
from samplebase import SampleBase
from datetime import datetime
from rgbmatrix import graphics
import time
import random
import math

def dist(*args):
    if len(args) == 4:
        # 2D-Distanz: hypot(dx, dy)
        return math.hypot(args[2] - args[0], args[3] - args[1])
    elif len(args) == 6:
        # 3D-Distanz: hypot(dx, dy, dz)
        return math.hypot(args[3] - args[0], args[4] - args[1], args[5] - args[2])
    else:
        raise ValueError("Falsche Anzahl an Argumenten. Erwartet werden 4 (2D) oder 6 (3D) Koordinaten.")
def get_random_color():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)

    r = random.randint(220, 255)
    g = random.randint(100, 180)
    b = random.randint(0, 50)
    return graphics.Color(r, g, b)

class Pixel():
    def __init__(self, position, size, vel, acc, canvas_w, canvas_h):
        self.position = position
        self.mass = random.randint(2,4)  #same as mass
        self.r = int(math.sqrt(self.mass)*3)
        self.vel = Vector(random.uniform(-1,1), random.uniform(-1,1))
        self.acc = Vector(-1,1)
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.color = get_random_color() 

    def collide(self, other):
        

        impact_vector = other.position.sub(self.position)
        d = impact_vector.mag()
        r = self.r + other.r

        if d < r:
            self.change_color()
            
            #Normalisieren des Impact Vektors
            impact_vector_normalized = Vector(impact_vector.x, impact_vector.y)
            impact_vector_normalized.div(d)
            # Geschwindigkeitsdifferenz
            v_diff = other.vel.sub(self.vel)
            num = v_diff.dot(impact_vector_normalized)
            mass_sum = self.mass + other.mass

            #Impulserhaltung: geschwindigkeitsänderung für self
            delta_v_a = Vector(impact_vector_normalized.x, impact_vector_normalized.y)
            delta_v_a.mult(2*other.mass * num / mass_sum)
            self.vel.add(delta_v_a)
            #Impulserhaltung: Geschwindigkeitsänderung für other
            delta_v_b = Vector(impact_vector_normalized.x, impact_vector_normalized.y)
            delta_v_b.mult(-2 * self.mass * num/mass_sum)
            other.vel.add(delta_v_b)

            # Position korrigieren um überlagerung zu vermeiden
            overlap = r - d
            dir = Vector(impact_vector_normalized.x, impact_vector_normalized.y)
            dir.mult(overlap*0.5)
            self.position.sub(dir)
            other.position.add(dir)

    def change_color(self):
        self.color = get_random_color()
    
    def draw_box(self, canvas):
        for dx in range(self.r):
            for dy in range(self.r):
                nx, ny = int(self.position.x + dx), int(self.position.y - dy)  # Stack upwards
                if nx < self.canvas_w and ny >= 0:  # Avoid negative Y values
                    canvas.SetPixel(nx, ny, self.color.red, self.color.green, self.color.blue)

    def draw_circle(self, canvas):
        """Zeichnet einen Kreis mit dem Mittelpunkt (center_x, center_y) und dem Radius."""
        for dx in range(-self.r, self.r + 1):
            for dy in range(-self.r, self.r + 1):
                if dx * dx + dy * dy <= self.r * self.r:  # Prüfe, ob der Punkt innerhalb des Kreises liegt
                    nx, ny = self.position.x + dx, self.position.y + dy
                    if 0 <= nx < self.canvas_w and 0 <= ny < self.canvas_h:
                        canvas.SetPixel(nx, ny,  self.color.red, self.color.green, self.color.blue)
        canvas.SetPixel(self.position.x, self.position.y, 0 , 0 , 0 )


    def draw_pixel(self, canvas):
        canvas.SetPixel(self.position.x, self.position.y,  self.color.red, self.color.green, self.color.blue)



    def intersects(self, other):
        #print(f"{self.x}, {self.y}, {other.x}, {other.y}") 
        d = dist(self.position.x, self.position.y, other.position.x, other.position.y)
        r = self.size + other.size
        if d < r:
            return True
        
        return False

    def calc(self):
        
        #self.vel.x *= 0.99  # 1% Geschwindigkeitsverlust pro Frame
        #self.vel.y *= 0.99
        
        self.vel.add(self.acc)
        self.vel.limit(10)
        self.position.x = self.position.x + self.vel.x
        self.position.y = self.position.y + self.vel.y

        # Korrigiere Position und Geschwindigkeit bei Randberührung
        if self.position.x + self.r > self.canvas_w:
            self.position.x = self.canvas_w - self.r  # Setze genau an den Rand
            self.vel.x *= -1
        elif self.position.x - self.r < 0:
            self.position.x = self.r  # Setze genau an den Rand
            self.vel.x *= -1

        if self.position.y + self.r > self.canvas_h:
            self.position.y = self.canvas_h - self.r  # Setze genau an den Rand
            self.vel.y *= -1
        elif self.position.y - self.r < 0:
            self.position.y = self.r  # Setze genau an den Rand
            self.vel.y *= -1


        self.acc.x = 0
        self.acc.y = 0


    def applyForce(self, force):
        f = force
        f.div(self.mass)
        self.acc.add(f)




class Vector():
    #check later: https://www.reddit.com/r/learnpython/comments/l33xe9/vectors_2d_3d_in_python/
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def add (self, v):
        self.x = self.x + v.x
        self.y = self.y + v.y

    def sub(self, b):
        return Vector(self.x - b.x, self.y - b.y)
    
    def mult(self, n):
        self.x = self.x * n
        self.y = self.y * n
    def div(self, n):
        self.x = self.x / n
        self.y = self.y / n

    def dot(self, b):
        return self.x * b.x + self.y * b.y

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def set_mag(self, new_mag):
        current_mag = self.mag()
        if current_mag == 0:
            return  # Vermeide Division durch Null
        # Normalisiere und skaliere auf die neue Magnitude
        self.x = self.x / current_mag * new_mag
        self.y = self.y / current_mag * new_mag
    def mag_sq(self):
        return self.x * self.x + self.y * self.y
    def limit(self, max_value):
        m_sq = self.mag_sq()
        if m_sq > max_value * max_value:
            self.div(math.sqrt(m_sq))
            self.mult(max_value)
        return self

class PhysicsEngine(SampleBase):
    def __init__(self, *args, **kwargs):
        super(PhysicsEngine, self).__init__(*args, **kwargs)


    def run(self):
        num_pixels = 10
        offset_canvas = self.matrix.CreateFrameCanvas()
        width = offset_canvas.width
        height = offset_canvas.height
        
        pixels = []
        for i in range(num_pixels):
            pixels.append(Pixel(Vector(random.randint(0,width), random.randint(0,height)), random.randint(1,5), 1, 1, width, height))
        counter = 0
        while True:
            counter = counter+1
            
            offset_canvas.Clear()
            current_time = time.time()
            forceV = Vector(0,1)
           

            for i in range(len(pixels)):

                particle_a = pixels[i]
                particle_a.applyForce(forceV)
                for j in range(i + 1, len(pixels)):
                    particle_b = pixels[j]
                    particle_a.collide(particle_b)

            for pixel in pixels:
                pixel.calc()
                pixel.draw_circle(offset_canvas)

            time.sleep(0.01)
            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

if __name__ == "__main__":
    physics_engine = PhysicsEngine()
    if not physics_engine.process():
        physics_engine.print_help()

