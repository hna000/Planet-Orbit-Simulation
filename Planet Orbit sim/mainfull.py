import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Milky Way simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
GREY = (80, 78, 81)
PURPLE = (221, 160, 221)
ORANGE = (255,200,124)
PINK = (255, 160, 137)
PLBLUE = (175,238,238)
DKBLUE = (0,170,228)

FONT = pygame.font.SysFont("comicsans", 10)

class Planet:
    AU = 149.6e6*1000
    G = 6.67428e-11
    SCALE = 12/AU
    TIMESTEP = 3600*30


    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
       
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 1)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y))


    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / (distance**2)
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force
        return force_x, force_y
    
    def update_pos(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))



def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 1, YELLOW, 1.98892*10**30)
    sun.sun = True

    earth = Planet(-1*Planet.AU, 0, 0.009, BLUE, 5.9742*10**24)
    earth.y_vel = 29.783*1000

    mars = Planet(-1.524*Planet.AU, 0, 0.0045, RED, 6.39*10**23)
    mars.y_vel = 24.077*1000

    murcury = Planet(0.387*Planet.AU, 0, 0.0035, GREY, 3.30*10**23)
    murcury.y_vel = -47.4*1000

    venus = Planet(0.723*Planet.AU, 0, 0.0085, PURPLE, 4.8685*10**24)
    venus.y_vel = -35.02*1000

    jupiter = Planet(-5.2*Planet.AU, 0, 0.1, PINK, 1.898*10**27)
    jupiter.y_vel = 13.1*1000

    saturn = Planet(9.58*Planet.AU, 0, 0.085, ORANGE, 568*10**24)
    saturn.y_vel = -9.7*1000

    uranus = Planet(-19.22*Planet.AU, 0, 0.036, PLBLUE, 86.8*10**24)
    uranus.y_vel = 6.8*1000

    neptune = Planet(30.1*Planet.AU, 0, 0.03, DKBLUE, 102*10**24)
    neptune.y_vel = -5.4*1000

    planets = [sun, earth, mars, murcury, venus, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_pos(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()