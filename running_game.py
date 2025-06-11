import pygame
from sys import exit
from random import randint, choice
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0

        self.player_jump = pygame.image.load('graphics/player/player_jump.png').convert_alpha()

        player_crouch_1 = pygame.image.load('graphics/player/player_crouch_1.png').convert_alpha()
        player_crouch_2 = pygame.image.load('graphics/player/player_crouch_2.png').convert_alpha()
        self.player_crouch_walk = [player_crouch_1, player_crouch_2]
        self.crouch_active = False

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 370))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('sounds/jump.mp3')
        self.jump_sound.set_volume(0.4)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] and self.rect.bottom >= 370):
            self.gravity -= 20
            self.jump_sound.play()

        elif(keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]):
            self.crouch_active = True
            
        
        else:
            self.crouch_active = False

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 370:
            self.rect.bottom = 370
            self.gravity = 0

    def animation_state(self):
        #jump
        if self.rect.bottom < 370:
            self.image = self.player_jump
        
        #crouch
        elif self.crouch_active:
            self.rect.bottom = 390
            self.player_index += 0.1
            if(self.player_index >= len(self.player_crouch_walk)):
                self.player_index = 0
            self.image = self.player_crouch_walk[int(self.player_index)]
        
        #walk
        else:
            self.player_index += 0.1
            if (self.player_index >= len(self.player_walk)):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if(type == 'mosq'):
            mosq_1 = pygame.image.load('graphics/enemy/mosquito1.png').convert_alpha()
            mosq_2 = pygame.image.load('graphics/enemy/mosquito2.png').convert_alpha()
            self.frames = [mosq_1, mosq_2]
            y_pos = 270
        else:
            cat_1 = pygame.image.load('graphics/enemy/cat1.png').convert_alpha()
            cat_2 = pygame.image.load('graphics/enemy/cat2.png').convert_alpha()
            self.frames = [cat_1, cat_2]
            y_pos = 370
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        #cat
        self.animation_index += 0.1
        if (self.animation_index >= len(self.frames)):
            self.animation_index= 0
        self.image = self.frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()



def display_score():
    curr_time = (pygame.time.get_ticks() // 1000)  - start_time
    score_surface = test_font.render(f'score:{curr_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    return curr_time

def collision_sprite():
    #if this collision list has any values, return false
    if(pygame.sprite.spritecollide(player.sprite, obstacle_group, False)):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init() #starts pygame, needed to use it

                                #width, height
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('running game!')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('sounds/Leaping Lizards!.ogg')
bg_music.play(loops = -1)

#groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#sky
sky_surface = pygame.image.load('background/Sky_scroll.png').convert()
scroll = 0
tiles = math.ceil(400 / sky_surface.get_width()) + 1


#ground
ground_surface = pygame.image.load('background/Ground.png').convert()

#cat
cat_frame_1 = pygame.image.load('graphics/enemy/cat1.png').convert_alpha()
cat_frame_2 = pygame.image.load('graphics/enemy/cat2.png').convert_alpha()
cat_frames = [cat_frame_1, cat_frame_2]
cat_frame_index = 0
cat_surface = cat_frames[cat_frame_index]

#mosquio
mosq_frame_1 = pygame.image.load('graphics/enemy/mosquito1.png').convert_alpha()
mosq_frame_2 = pygame.image.load('graphics/enemy/mosquito2.png').convert_alpha()
mosq_frames = [mosq_frame_1, mosq_frame_2]
mosq_frame_index = 0
mosq_frame = mosq_frames[mosq_frame_index]

obstacle_rect_list = []

#player
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0

player_jump = pygame.image.load('graphics/player/player_jump.png').convert_alpha()

player_crouch_1 = pygame.image.load('graphics/player/player_crouch_1.png').convert_alpha()
player_crouch_2 = pygame.image.load('graphics/player/player_crouch_2.png').convert_alpha()
player_crouch_walk = [player_crouch_1, player_crouch_2]
crouch_active = False

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80, 370)) 
player_grav = 0

#intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png')
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center= (400, 200))

game_name = test_font.render('My Game!!', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 320))

#timer
obstacle_timer = pygame.USEREVENT + 1 
pygame.time.set_timer(obstacle_timer, 1500)

#draw all our elements and update everything
while True:
    #check for all player input (event loop)
    for event in pygame.event.get(): #loops through every possible event
        if event.type == pygame.QUIT: #if user closes window
            pygame.quit()
            exit()

        if game_active:
            #jump
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['mosq','cat','cat','cat'])))
                        

        else:
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)


    if game_active:
        

        #sky scroll
        i = 0
        while(i < tiles):
            screen.blit(sky_surface, (sky_surface.get_width()*i + scroll, 0))
            i += 1
            
        scroll -= 1
        if abs(scroll) > sky_surface.get_width():
            scroll = 0

        #blit = block image transfer, put one surface on another
        #screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 350))
        score = display_score()

        #player movement
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

        

    #game over / intro
    else:
        screen.fill((94, 100, 180))
        screen.blit(player_stand, player_stand_rect)
        

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)
        
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
