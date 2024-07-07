import pygame
from sys import exit
from random import randint, choice

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        bird_image1 = pygame.image.load("assets/birddown.png").convert()
        bird_image2 = pygame.image.load("assets/birdup.png").convert()
        self.bird_flap =[bird_image1,bird_image2]
        self.bird_index = 0

        self.image =self.bird_flap[self.bird_index]
        self.rect = self.image.get_rect(midbottom=(100,300))
        self.gravity = 0

        self.flap = pygame.mixer.Sound('assets/sfx/flap.wav')
        self.flap.set_volume(0.5)

    def bird_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom < 500:
            self.gravity = -8
            self.flap.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 468:
            self.rect.bottom = 468

    def animation_state(self):
        self.bird_index += 0.1
        if self.bird_index >= len(self.bird_flap): self.bird_index = 0
        self.image = self.bird_flap[int(self.bird_index)]

    def update(self):
        self.bird_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle1(pygame.sprite.Sprite):
    def __init__(self,random_number):
        super().__init__()

        self.pipe_up = pygame.image.load('assets/pipeup.png').convert_alpha()
        self.image = self.pipe_up
        self.rect = self.image.get_rect(midtop=(800, 280+random_number))
    def animation_pipe(self):
        self.rect.x -= 2.5

    def update(self):
        self.animation_pipe()
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class Obstacle2(pygame.sprite.Sprite):
    def __init__(self,random_number):
        super().__init__()
        self.pipe_down = pygame.image.load('assets/pipedown.png').convert_alpha()
        self.image = self.pipe_down
        self.rect = self.image.get_rect(midbottom=(800, 100+random_number))
    def animation_pipe(self):
        self.rect.x -= 2.5

    def update(self):
        self.animation_pipe()
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class ground_class(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ground_image = pygame.image.load("assets/ground.png").convert()
        self.image = self.ground_image
        self.rect = self.image.get_rect(midbottom=(200,600))

def collision_sprite():
    if pygame.sprite.spritecollide(bird.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    elif pygame.sprite.spritecollideany(bird.sprite, ground):
        return False
    else:
        return True

def display_score():
    global score
    for obstacle in obstacle_group:
        if obstacle.rect.x < 100:
            score += 1
    score_surf = test_font1.render(f'Score: {int(score/164)}', False, (0, 0, 0))
    score_rect = score_surf.get_rect(center=(100, 50))
    screen.blit(score_surf, score_rect)
    return score


pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('FLAPPY BIRD')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font.ttf', 50)
test_font1 = pygame.font.Font('font.ttf', 20)
game_active = False
score = 0

#background
background_image = pygame.image.load("assets/bg.png").convert()

#ground
ground_image = pygame.image.load("assets/ground.png").convert()
ground_rect2 = ground_image.get_rect(midbottom=(600,600))

#Intro Screen
bird_img = pygame.image.load("assets/bird.png").convert()
bird_img = pygame.transform.rotozoom(bird_img,0,10)
bird_rect = bird_img.get_rect(center = (400,250))

game_name = test_font.render('Flappy Bird',False,("YELLOW"))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,("YELLOW"))
game_message_rect = game_message.get_rect(center = (400,500))

#Groups
bird = pygame.sprite.GroupSingle()
bird.add(Bird())

ground = pygame.sprite.GroupSingle()
ground.add(ground_class())

obstacle_group = pygame.sprite.Group()

#obstacle spwaning rate
frame_count = 0
obstacle_spawn_interval = 20

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            frame_count += 1
            if frame_count % obstacle_spawn_interval == 0:
                random_number = randint(1, 200)
                obstacle_group.add(Obstacle1(random_number))
                obstacle_group.add(Obstacle2(random_number))

        if not game_active:
            score = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

    if game_active:
        screen.blit(background_image, (0,-125))
        screen.blit(background_image, (400, -125))
        screen.blit(ground_image, ground_rect2)

        score = display_score()

        bird.draw(screen)
        bird.update()

        ground.draw(screen)

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()



    else:
        screen.fill((94, 129, 162))
        screen.blit(bird_img, bird_rect)

        score_message = test_font.render(f'Your score: {int(score/164)}', False, ("YELLOW"))
        score_message_rect = score_message.get_rect(center=(400,500))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)


    pygame.display.update()
    clock.tick(60)
