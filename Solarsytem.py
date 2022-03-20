
import pygame
import math
from pygame import mixer 

pygame.init()

width, height = 1580, 920
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Planet Simulation")

background = pygame.image.load("Background.jpg")
background = pygame.transform.scale(background, (1580, 920)).convert_alpha()

pygame.mixer.music.load("Bg_music.mp3")
pygame.mixer.music.play(-1)

white = (255, 255, 255)
ghost_white = (248, 248, 255)
yellow = (255, 215, 0)
blue = (30, 144, 255)
red = (178, 34, 34)
grey = (119, 136, 153)
orange = (255, 127, 80)
khaki = (189, 183, 107)
green = (102, 205, 170)
prussian = (0, 0, 205)

font = pygame.font.Font("freesansbold.ttf", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    scale = 100 / AU        # 1AU = 100 pixels
    timestep = 3600 * 24    # 1 day

    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = ''

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, window):
        x = self.x * self.scale + width/2
        y = self.y * self.scale + height/2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.scale + width / 2
                y = y * self.scale + height / 2
                updated_points.append((x, y))

            pygame.draw.lines(window, self.color, False, updated_points, 2)
        pygame.draw.circle(window, self.color, (x, y), self.radius)

        if not self.sun:
            planet_name = font.render(f"{self.name}", False, white)
            distance_text = font.render(f"{round(self.distance_to_sun/1000, 1)}KM", False, white)
            window.blit(planet_name, (x - planet_name.get_width()/2, y - planet_name.get_height() + 35))
            window.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height() - 15))   
        else:
            planet_name = font.render(f"{self.name}", False, white)
            window.blit(planet_name, (x - planet_name.get_width()/2, y - planet_name.get_height()/2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_vel += total_fx / self.mass * self.timestep
        self.y_vel += total_fy / self.mass * self.timestep

        self.x += self.x_vel * self.timestep
        self.y += self.y_vel * self.timestep
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0 , 20, yellow, 1.98892 * 10**30)
    sun.sun = True
    sun.name = 'SUN'
    
    earth = Planet(-1 * Planet.AU, 0, 16, blue, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000
    earth.name = 'EARTH'

    mars = Planet(-1.524 * Planet.AU, 0, 12, red, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000
    mars.name = 'MARS'

    mercury = Planet(0.387 * Planet.AU, 0, 8, grey, 3.33 * 10**23)
    mercury.y_vel = -47.4 * 1000
    mercury.name = 'MERCURY'

    venus = Planet(0.723 * Planet.AU, 0, 14, ghost_white, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000
    venus.name = 'VENUS'

    jupiter = Planet(2.2 * Planet.AU, 0, 40, orange, 9.78 * 10**24)
    jupiter.y_vel = -19.5 * 1000
    jupiter.name = 'JUPITER'

    saturn = Planet(-2.8 * Planet.AU, 0, 30, khaki, 7.5 * 10**24 )
    saturn.y_vel = 17.5 * 1000
    saturn.name = 'SATURN'

    uranus = Planet(3.4 * Planet.AU, 0, 21, green, 6.7 * 10**24)
    uranus.y_vel = -16 * 1000
    uranus.name = 'URANUS'

    neptune = Planet(-4.1 * Planet.AU, 0, 19, prussian, 6.9 * 10**24)
    neptune.y_vel = 14.5 * 1000
    neptune.name = 'NEPTUNE'

    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        window.fill((0, 0, 0))
        window.blit(background,(0, 0))
        

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(window)

        pygame.display.update()        
    pygame.quit()

main()