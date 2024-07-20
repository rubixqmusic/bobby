import pygame
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
                    lifetime = 6
                    self._particles[index] = [particle_type, position, size, shape, color, lifetime, properties]
                    break
                index += 1

            
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

            index += 1

        ...