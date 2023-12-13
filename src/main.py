from game_server import GameServer
import pygame

if __name__ == "__main__":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()        
            
    server = GameServer()

    server.run()
