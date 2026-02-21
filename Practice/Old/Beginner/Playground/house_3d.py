"""
3D Animated House - Using PyOpenGL and GLFW
Features: Rotating house, animated door, windows, chimney with smoke
Controls: ESC to exit, Arrow keys to rotate manually
"""

import sys
import math

try:
    import glfw
    from OpenGL.GL import *
    from OpenGL.GLU import *
except ImportError:
    print("Required packages not found. Please install: pip install glfw PyOpenGL")
    sys.exit(1)


class House3D:
    def __init__(self):
        # Initialize GLFW
        if not glfw.init():
            print("Failed to initialize GLFW")
            sys.exit(1)
        
        # Create window
        self.width, self.height = 1000, 800
        self.window = glfw.create_window(self.width, self.height, "3D Animated House", None, None)
        if not self.window:
            glfw.terminate()
            print("Failed to create window")
            sys.exit(1)
        
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, self.key_callback)
        
        # OpenGL setup
        self.setup_opengl()
        
        # Animation state
        self.auto_rotation = 0.0
        self.manual_rotation_y = 0.0
        self.manual_rotation_x = 15.0
        self.door_angle = 0.0
        self.door_opening = True
        self.smoke_particles = []
        self.time = 0.0
        
        # Initialize smoke particles
        for i in range(10):
            self.smoke_particles.append({
                'y': i * 0.15,
                'x_offset': math.sin(i) * 0.1,
                'size': 0.05 + i * 0.01
            })
    
    def setup_opengl(self):
        """Configure OpenGL settings"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)
        
        # Enable lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        # Light properties
        light_pos = [5.0, 10.0, 5.0, 1.0]
        light_ambient = [0.3, 0.3, 0.3, 1.0]
        light_diffuse = [0.8, 0.8, 0.8, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]
        
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        
        # Material properties
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Set clear color (sky blue)
        glClearColor(0.529, 0.808, 0.922, 1.0)
    
    def key_callback(self, window, key, scancode, action, mods):
        """Handle keyboard input"""
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        
        # Manual rotation
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_LEFT:
                self.manual_rotation_y -= 5
            elif key == glfw.KEY_RIGHT:
                self.manual_rotation_y += 5
            elif key == glfw.KEY_UP:
                self.manual_rotation_x -= 5
            elif key == glfw.KEY_DOWN:
                self.manual_rotation_x += 5
    
    def set_material(self, r, g, b, shininess=50):
        """Set material color"""
        glColor3f(r, g, b)
        mat_specular = [0.3, 0.3, 0.3, 1.0]
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, shininess)
    
    def draw_box(self, width, height, depth):
        """Draw a 3D box centered at origin"""
        w, h, d = width/2, height/2, depth/2
        
        glBegin(GL_QUADS)
        
        # Front face
        glNormal3f(0, 0, 1)
        glVertex3f(-w, -h, d)
        glVertex3f(w, -h, d)
        glVertex3f(w, h, d)
        glVertex3f(-w, h, d)
        
        # Back face
        glNormal3f(0, 0, -1)
        glVertex3f(w, -h, -d)
        glVertex3f(-w, -h, -d)
        glVertex3f(-w, h, -d)
        glVertex3f(w, h, -d)
        
        # Top face
        glNormal3f(0, 1, 0)
        glVertex3f(-w, h, d)
        glVertex3f(w, h, d)
        glVertex3f(w, h, -d)
        glVertex3f(-w, h, -d)
        
        # Bottom face
        glNormal3f(0, -1, 0)
        glVertex3f(-w, -h, -d)
        glVertex3f(w, -h, -d)
        glVertex3f(w, -h, d)
        glVertex3f(-w, -h, d)
        
        # Right face
        glNormal3f(1, 0, 0)
        glVertex3f(w, -h, d)
        glVertex3f(w, -h, -d)
        glVertex3f(w, h, -d)
        glVertex3f(w, h, d)
        
        # Left face
        glNormal3f(-1, 0, 0)
        glVertex3f(-w, -h, -d)
        glVertex3f(-w, -h, d)
        glVertex3f(-w, h, d)
        glVertex3f(-w, h, -d)
        
        glEnd()
    
    def draw_roof(self):
        """Draw a triangular prism roof"""
        self.set_material(0.6, 0.2, 0.1)  # Dark red/brown
        
        width = 2.4
        height = 1.0
        depth = 2.2
        
        glBegin(GL_TRIANGLES)
        
        # Front triangle
        glNormal3f(0, 0, 1)
        glVertex3f(-width/2, 0, depth/2)
        glVertex3f(width/2, 0, depth/2)
        glVertex3f(0, height, depth/2)
        
        # Back triangle
        glNormal3f(0, 0, -1)
        glVertex3f(width/2, 0, -depth/2)
        glVertex3f(-width/2, 0, -depth/2)
        glVertex3f(0, height, -depth/2)
        
        glEnd()
        
        glBegin(GL_QUADS)
        
        # Left slope
        nx, ny = -height, width/2
        length = math.sqrt(nx*nx + ny*ny)
        glNormal3f(nx/length, ny/length, 0)
        glVertex3f(-width/2, 0, depth/2)
        glVertex3f(0, height, depth/2)
        glVertex3f(0, height, -depth/2)
        glVertex3f(-width/2, 0, -depth/2)
        
        # Right slope
        nx = height
        glNormal3f(nx/length, ny/length, 0)
        glVertex3f(width/2, 0, depth/2)
        glVertex3f(width/2, 0, -depth/2)
        glVertex3f(0, height, -depth/2)
        glVertex3f(0, height, depth/2)
        
        # Bottom
        glNormal3f(0, -1, 0)
        glVertex3f(-width/2, 0, -depth/2)
        glVertex3f(width/2, 0, -depth/2)
        glVertex3f(width/2, 0, depth/2)
        glVertex3f(-width/2, 0, depth/2)
        
        glEnd()
    
    def draw_door(self):
        """Draw animated door"""
        glPushMatrix()
        
        # Position at left edge of door frame
        glTranslatef(-0.25, 0, 0)
        
        # Rotate door (hinge on left side)
        glRotatef(-self.door_angle, 0, 1, 0)
        
        # Door panel
        self.set_material(0.4, 0.25, 0.1)  # Brown
        glTranslatef(0.25, 0, 0)
        self.draw_box(0.5, 0.9, 0.05)
        
        # Door knob
        glPushMatrix()
        self.set_material(0.83, 0.69, 0.22)  # Gold
        glTranslatef(0.15, 0, 0.05)
        quad = gluNewQuadric()
        gluSphere(quad, 0.05, 16, 16)
        gluDeleteQuadric(quad)
        glPopMatrix()
        
        glPopMatrix()
    
    def draw_window(self):
        """Draw a window"""
        # Frame
        self.set_material(0.3, 0.3, 0.35)
        self.draw_box(0.45, 0.45, 0.06)
        
        # Glass
        self.set_material(0.6, 0.8, 0.95)
        glPushMatrix()
        glTranslatef(0, 0, 0.02)
        self.draw_box(0.35, 0.35, 0.02)
        glPopMatrix()
        
        # Cross bars
        self.set_material(0.3, 0.3, 0.35)
        glPushMatrix()
        glTranslatef(0, 0, 0.04)
        self.draw_box(0.35, 0.03, 0.02)
        self.draw_box(0.03, 0.35, 0.02)
        glPopMatrix()
    
    def draw_chimney(self):
        """Draw chimney"""
        self.set_material(0.5, 0.3, 0.2)  # Brick color
        self.draw_box(0.3, 0.6, 0.3)
    
    def draw_smoke(self):
        """Draw animated smoke particles"""
        glDisable(GL_LIGHTING)
        
        for i, particle in enumerate(self.smoke_particles):
            alpha = 1.0 - (particle['y'] / 1.5)
            if alpha < 0:
                alpha = 0
            
            gray = 0.7 + 0.2 * alpha
            glColor4f(gray, gray, gray, alpha)
            
            glPushMatrix()
            x_offset = math.sin(self.time * 2 + i) * 0.1 + particle['x_offset']
            glTranslatef(x_offset, particle['y'], 0)
            
            quad = gluNewQuadric()
            gluSphere(quad, particle['size'], 8, 8)
            gluDeleteQuadric(quad)
            
            glPopMatrix()
        
        glEnable(GL_LIGHTING)
    
    def draw_ground(self):
        """Draw green ground plane"""
        self.set_material(0.2, 0.6, 0.2)  # Green
        
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glVertex3f(-10, 0, 10)
        glVertex3f(10, 0, 10)
        glVertex3f(10, 0, -10)
        glVertex3f(-10, 0, -10)
        glEnd()
    
    def draw_sun(self):
        """Draw a sun"""
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 0.9, 0.3)  # Yellow
        
        glPushMatrix()
        glTranslatef(5, 6, -5)
        quad = gluNewQuadric()
        gluSphere(quad, 0.5, 20, 20)
        gluDeleteQuadric(quad)
        glPopMatrix()
        
        glEnable(GL_LIGHTING)
    
    def draw_house(self):
        """Draw the complete house"""
        # Main body
        glPushMatrix()
        self.set_material(0.9, 0.85, 0.7)  # Cream/beige
        glTranslatef(0, 1, 0)
        self.draw_box(2, 2, 2)
        glPopMatrix()
        
        # Roof
        glPushMatrix()
        glTranslatef(0, 2, 0)
        self.draw_roof()
        glPopMatrix()
        
        # Door
        glPushMatrix()
        glTranslatef(0, 0.5, 1.03)
        self.draw_door()
        glPopMatrix()
        
        # Front windows
        glPushMatrix()
        glTranslatef(-0.6, 1.3, 1.03)
        self.draw_window()
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.6, 1.3, 1.03)
        self.draw_window()
        glPopMatrix()
        
        # Side windows (left)
        glPushMatrix()
        glTranslatef(-1.03, 1.3, 0)
        glRotatef(90, 0, 1, 0)
        self.draw_window()
        glPopMatrix()
        
        # Side windows (right)
        glPushMatrix()
        glTranslatef(1.03, 1.3, 0)
        glRotatef(-90, 0, 1, 0)
        self.draw_window()
        glPopMatrix()
        
        # Chimney
        glPushMatrix()
        glTranslatef(0.5, 2.7, -0.5)
        self.draw_chimney()
        glPopMatrix()
        
        # Smoke
        glPushMatrix()
        glTranslatef(0.5, 3.0, -0.5)
        self.draw_smoke()
        glPopMatrix()
    
    def update(self, delta_time):
        """Update animation state"""
        self.time += delta_time
        
        # Auto rotation
        self.auto_rotation += 15 * delta_time
        
        # Door animation
        door_speed = 45  # degrees per second
        if self.door_opening:
            self.door_angle += door_speed * delta_time
            if self.door_angle >= 90:
                self.door_angle = 90
                self.door_opening = False
        else:
            self.door_angle -= door_speed * delta_time
            if self.door_angle <= 0:
                self.door_angle = 0
                self.door_opening = True
        
        # Update smoke particles
        for particle in self.smoke_particles:
            particle['y'] += 0.3 * delta_time
            if particle['y'] > 1.5:
                particle['y'] = 0
                particle['size'] = 0.05
            else:
                particle['size'] += 0.02 * delta_time
    
    def render(self):
        """Render the scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Set up projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width / self.height, 0.1, 100)
        
        # Set up modelview
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Camera position
        gluLookAt(
            0, 3, 8,    # Eye position
            0, 1.5, 0,  # Look at point
            0, 1, 0     # Up vector
        )
        
        # Apply rotations
        glRotatef(self.manual_rotation_x, 1, 0, 0)
        glRotatef(self.manual_rotation_y + self.auto_rotation, 0, 1, 0)
        
        # Draw sun (before other rotations affect it too much)
        self.draw_sun()
        
        # Draw ground
        self.draw_ground()
        
        # Draw house
        self.draw_house()
    
    def run(self):
        """Main loop"""
        last_time = glfw.get_time()
        
        print("3D Animated House")
        print("-----------------")
        print("Controls:")
        print("  Arrow keys: Rotate view")
        print("  ESC: Exit")
        print()
        
        while not glfw.window_should_close(self.window):
            current_time = glfw.get_time()
            delta_time = current_time - last_time
            last_time = current_time
            
            self.update(delta_time)
            self.render()
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        
        glfw.terminate()


if __name__ == "__main__":
    try:
        house = House3D()
        house.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        glfw.terminate()
