import pygame
import sys
from constants import *
from logger import log_event, log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
    
        screen.fill('#000000')
        
        log_state()
        
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.has_collided(player):
                log_event("player_collision",
                          player_position=[round(player.position.x, 2), round(player.position.y, 2)],
                          asteroid_position=[round(asteroid.position.x, 2), round(asteroid.position.y, 2)],
                          asteroid_radius=asteroid.radius)
                print('Game over!')
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if shot.has_collided(asteroid):
                    log_event("asteroid_destroyed",
                              asteroid_position=[round(asteroid.position.x, 2), round(asteroid.position.y, 2)],
                              asteroid_radius=asteroid.radius,
                              shot_position=[round(shot.position.x, 2), round(shot.position.y, 2)])
                    asteroid.split()
                    shot.kill()

        for d in drawable:
            d.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000




if __name__ == "__main__":
    main()
