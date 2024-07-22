import pygame
import random
import logging

from settings import *

class ParticleEngine:
    def __init__(self, max_particles, draw_target, camera) -> None:
        self._camera = camera
        self._max_particles = max_particles
        self._draw_target = draw_target
        self._particles = []

        for i in range(max_particles):
            self._particles.append(None)
    
    def generate_particles(self, particle_type: str, position: list, properties: dict):
        
        # type, position, size, shape, color, lifetime, properties
        
        if particle_type == JUMP_PARTICLE:
            index = 0
            for particle in self._particles:
                if particle == None:   
                    size = 4
                    shape = PARTICLE_CIRCLE
                    color = (200,200,255)
                    lifetime = 4
                    if index <= len(self._particles) -1:
                        self._particles[index] = [particle_type, position, size, shape, color, lifetime, properties]
                    return
                index += 1

        elif particle_type == DUST_PARTICLE:
            number_of_particles = random.randint(1,2)
            index = 0
            for particle in self._particles:
                if particle == None:
                    x_pos = random.randint(1, 2)
                    size = 2
                    position[0] += x_pos
                    shape = PARTICLE_CIRCLE
                    color = (200,200,255)
                    lifetime = 3
                    if index <= len(self._particles) -1:
                        self._particles[index] = [particle_type, position, size, shape, color, lifetime, properties]
                    number_of_particles -= 1
                    if number_of_particles <= 0:
                        return
                index += 1
            # logging.debug(f"could not add particle! all available particle slots full")

            
    def update(self, delta):
        ...

    def draw(self):
        index = 0
        for particle in self._particles:
            if particle is not None:
                if particle[5] <= 0:
                    self._particles[index] = None
                    continue
                else:

                    if particle[0] == JUMP_PARTICLE:
                        pygame.draw.circle(self._draw_target, particle[4], (particle[1][0] - self._camera.x, particle[1][1] - self._camera.y), particle[2], particle[5])
                        particle[2] += 1
                        particle[5] -= 1
                    
                    if particle[0] == DUST_PARTICLE:

                        
                        pygame.draw.circle(self._draw_target, particle[4], (particle[1][0] - self._camera.x, particle[1][1] - self._camera.y), particle[2], particle[5])
                        particle[1][1] -= 1
                        # if particle[5] % 2 == 0:
                        particle[2] += 0.5
                        particle[5] -= 1
            index += 1

        ...