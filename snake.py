import pygame
from pygame.locals import *
from pygame.transform import *
from pygame.mixer import *
import time 
import random

block_size = 50
TEXT_ = (255,99,71)
class Apple:
    def __init__(self, main_screen):
        self.main_screen = main_screen
        self.image = pygame.image.load("resources/pizza.png").convert_alpha()
        self.image.set_colorkey((0, 0,0))
        
        self.image = pygame.transform.scale(self.image, (block_size,block_size))
        self.x = random.randint(0,15)*block_size
        self.y = random.randint(0,15)*block_size

    def draw(self):
            self.main_screen.blit(self.image, (self.x, self.y))
            pygame.display.flip()
    

    def move(self):
        self.x = random.randint(0,15)*block_size
        self.y = random.randint(0,15)*block_size


class Hamster_Object:
    def __init__(self, main_screen, length):
        self.main_screen = main_screen
        self.image = pygame.image.load("resources/hamster_block.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (block_size,block_size))
        self.length = length
        self.direction = 'down'
        self.x = [block_size] * length
        self.y = [block_size] * length
    
    def move_left(self):
        if self.direction!='right' or self.length==1:
         self.direction = 'left'
    
    def move_right(self):
        if self.direction!='left' or self.length==1:
         self.direction = 'right'
    
    def move_up(self):
        if self.direction!='down' or self.length==1:
         self.direction = 'up'
     
    def move_down(self):
        if self.direction!='up' or self.length==1:
         self.direction = 'down'
    
    def walk(self):
        
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.direction == 'left':
            self.x[0] -= block_size
        
        if self.direction == 'right':
            self.x[0] += block_size
        
        if self.direction == 'up':
            self.y[0] -= block_size
        
        
        if self.direction == 'down':
            self.y[0] += block_size
        
        self.draw()
    
    def draw(self):
        for i in range(self.length):
            self.main_screen.blit(self.image, (self.x[i], self.y[i]))
        
        pygame.display.flip()
    
    def increase(self):
        self.length +=1
        self.x.append(-1)
        self.y.append(-1)
    
class Game:
    def __init__(self):
        pygame.init()
        self.play_bg_music()
        self.screen = pygame.display.set_mode((800,800))
        pygame.display.set_caption("Hamster Game")
        pygame.display.set_icon(pygame.image.load("resources/hamster_block.png").convert_alpha())
        pygame.mixer.init()
        self.hamster = Hamster_Object(self.screen, 1)
        self.hamster.draw()
        self.beer = Apple(self.screen)
        self.beer.draw()
    

    def collision(self, x1, y1, x2, y2):
        if x1>=x2 and x1<x2+block_size:
            if y1>=y2 and y1<y2+block_size:
                return True
        
        return False

    def reset(self):
         self.hamster = Hamster_Object(self.screen, 1)
         self.beer = Apple(self.screen)
    
    def setting_background(self):
        bg =  pygame.image.load("resources/green_wallpaper.png")
        self.screen.blit(bg, (-240,-240))

    def game_over(self):
        self.setting_background()
        font = pygame.font.SysFont("Arial", 26, "bold")
        final_score = font.render(f"Game Over... Final Score: {self.hamster.length-1}", True, TEXT_)
        self.screen.blit(final_score, (170,290))

        replay = font.render("To play again press Enter! To exit press Escape!", True, TEXT_)
        self.screen.blit(replay, (110,340))
        pygame.display.flip()
    
    def play_bg_music(self):
        pygame.mixer.music.load("resources/bg_music2.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.05)

    def add_object(self):
        self.setting_background()
        self.hamster.walk()
        self.beer.draw()
        self.Score()
        pygame.display.flip()

        #snake and beer collision
        if self.collision(self.hamster.x[0], self.hamster.y[0], self.beer.x,self.beer.y):
            coll = pygame.mixer.Sound("resources/sip_sound.mp3")
            pygame.mixer.Sound.play(coll)
            coll.set_volume(0.05)
            self.hamster.increase()
            self.beer.move()
        
    
        #snake collision with itself
        for i in range(3, self.hamster.length):
            if self.collision(self.hamster.x[0], self.hamster.y[0], self.hamster.x[i], self.hamster.y[i]):
                raise "Game Over"
            
    
    
    def Score(self):
        font = pygame.font.SysFont("Arial", 26, "bold")
        score = font.render(f"Score: {self.hamster.length-1} pizza", True, TEXT_)
        self.screen.blit(score, (550, 10))
    def run(self):
        main_loop = True

        game_pause = False
        while main_loop:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        main_loop = False
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        game_pause = False
                    if not game_pause:
                        if event.key == K_LEFT:
                             self.hamster.move_left()
                        
                        if event.key == K_RIGHT:
                            
                             self.hamster.move_right()
                        
                        if event.key == K_UP:
                            
                             self.hamster.move_up()
                        
                        if event.key == K_DOWN:
                            
                             self.hamster.move_down()
                elif event.type == QUIT:
                    main_loop = False
            
            try:
              if not game_pause:  
                 self.add_object()
                 if self.hamster.x[0]<0 or self.hamster.x[0]>760 or self.hamster.y[0]<0 or self.hamster.y[0]>760:
                  raise "Game Over"
            except Exception as e:
                pygame.mixer.music.pause()
                sound = pygame.mixer.Sound("resources/hit_sound.mp3")
                pygame.mixer.Sound.play(sound)
                sound.set_volume(0.05)

                time.sleep(1)
                self.game_over() 
                game_pause = True
                self.reset()
            time.sleep(.1)


if __name__ == '__main__':
    game = Game()
    game.run()
 
