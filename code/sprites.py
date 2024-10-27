#from pygame.sprite import Group
from settings import *
from math import atan2, degrees # for the rotation of the gun


# REMMEBER --> when getting anything from TILED (tmx) place pos to topleft (usually) (bc its a grid like (0,0) rb not x,y

#---------------------------#
# map edition
#need to add a ground level layer sprite (bc it will not be the same as the collision sprite due to the character being able to go thru it )
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos) 
        #---------------------------#
        #Y-Sorting
        self.ground = True # attribute 
        #Y-Sorting
        #---------------------------#

# map edition
#---------------------------#

class CollisionSprite(pygame.sprite.Sprite): 
    def __init__(self, pos, surf, groups): # replaced size with surface when adding the map
        super().__init__(groups) #dont forget the . before __init__

        self.image = surf #these two blocks are creating the thing that the sprite will hit, got rid of  pygame.Surface(size) and replaced with surf (surface)
        #self.image.fill('yellow') #yellow so we can see
        
        self.rect = self.image.get_frect(topleft = pos) # changed center to topleft (FOR THE COLLISION SPRITES PLACEMENT )

#---------------------------#
#GUN EDITION
class Gun(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        #player connection
        self.player = player
        self.distance = 100
        self.player_direction = pygame.Vector2(1,0) # this will be the distance of the gun to the player

        #sprite setup 
        super().__init__(groups)
        self.gun_surf = pygame.image.load(join('images','gun','gun8.png')).convert_alpha()  #dont forget convert alpha # we get this using pygame.image.load #since we want the gun to spin (this is what will be stored for later)
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)


    #**************************************#
    #gun to flip with player movements
    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) # pygame.mouse.get_pos() will return a tuple: x and y postion, that can be pased directly into a vector
        player_pos = pygame.Vector2(WINDOW_WIDTH/2,WINDOW_HEIGHT/2)    # since the player is always in the center of the window (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.player_direction = (mouse_pos - player_pos).normalize() 
        #---> vecotr math 
            # if there is a display surface (orgin point at top left); player in center
                #get end point and subtract with start point (end point= mouse_pos)
        #print(self.player_direction)
    #gun to flip with player movements
    #**************************************#
    
    #**************************************#
    #rotate the guns surface
    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90 # subtract 90 from the angle to get the gun to rotate propertly # right angle triangle (with and a height, then this gives yo uthe angle of the triangle)---> this will all return in radians (but change it to degrees )
        if self.player_direction.x > 0: #this means we are on the right side of the player "">0" #fix the issue of the gun not working properly on the left side of the player
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1) # to get the angle (it will be a local variable) #for the scale stick to 1 
        else: #meaning the mouse is on the left sdie of the player
            #print(angle) #printing the angle (to see the error)
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1) # to fix the error of the left side rotation weierness just get the absolute value of the angle (since it would be negative but we want the postive version)
            self.image = pygame.transform.flip(self.image, False, True) #flip the image, and rotate it Flase (not on the hroizonantal axis) but on the vertical one 
    #rotate the guns surface
    #**************************************#

    #**************************************#
    #allowing the gun to follow the player
    def update(self, _): #dont need delta time (put _ in place)
        self.get_direction() # this will allow the gun to basically flip sides if the player does (so if the place goes left the gun will face left )
        self.rotate_gun()#roate the guns surface 
        self.rect.center = self.player.rect.center + self.player_direction * self.distance # this will alllow the gun to follow the player, bc it will update with the players movment to consitstanyl be at the center

    #allowing the gun to follow the player
    #**************************************#

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_frect(center = pos)
        self.spawn_time = pygame.time.get_ticks()#getting rid of the bullets so their is isnt a crash, you could either do it when they collide iwth obsticle or timer
        self.lifetime = 1000 #bullets will live for 1 second (1000 milleseconds )

    #*****************************#
    #ACTUAL Bullet being shot
    
        
        self.direction = direction
        self.speed = 1200

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt 
    
    #ACTUAL Bullet being shot
    #*****************************#
    
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill() #killing the sprite (the bullet image)
#GUN EDITION
#---------------------------#

#---------------------------#
#Enenimes
# Enenimes have to follow and constanly have the walk animation 

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player # this is the enemy

        #image
            #creating the image of the enermy (issue: not going to have the surf (surface of the player (enemy)) instead its the FRAMES of all the enemies)
        self.frames, self.frame_index  = frames, 0 
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6

        #rect 
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20,-40) #look up what exactly inflate does: 
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 350

        #timer 
            #---------------------------#
            #Bullet collision with enemy 
        self.death_time = 0
        self.death_duration = 400 #400 milleseconds
            #Bullet collision with enemy 
            #---------------------------#

    #---------------------------#
    #Enenimes MOVEMENT
    
    def animate(self,dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
    
    def move(self, dt):
        #get direction
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize() #allows for the movment to be mulitple the speed 

        # update the rect position + collision (logic)
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center



    def collision(self,direction): # copied from player.py  
        for sprite in self.collision_sprites: 
            if sprite.rect.colliderect(self.hitbox_rect): 
                if direction == 'horizontal':
                    if self.direction.x > 0: 
                        self.hitbox_rect.right = sprite.rect.left 
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right 
                else:
                    if self.direction.y < 0: 
                        self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: 
                        self.hitbox_rect.bottom = sprite.rect.top
    
    #---------------------------#
    #Bullet collision with enemy 
    #creating the destory method (will be used in main, particularly in the bullet_collision method)
    def destroy(self):
        #start a timer  (once this timer runs out the sprite will be destroyed)
        self.death_time = pygame.time.get_ticks()
        
        #change the image (once the sprite has been hit, the image will be changed to a white surface)
            #^^^^ creating a new surf (surface)
        surf = pygame.mask.from_surface(self.frames[0]).to_surface() #to_surface changes it right away back to a surface
        surf.set_colorkey('black')  # black means remove all the black pixels # how to just get the silloute of the collison enemy once its been killed
        self.image = surf 

    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()
    #Bullet collision with enemy 
    #---------------------------#
    
    def update(self,dt): # 2 things need to be done in this
            #---------------------------#
            #Bullet collision with enemy 
            #only want the enemy to move and update... if:
        if self.death_time == 0:
            


            #Bullet collision with enemy 
            #---------------------------# 
            
            self.move(dt)
            self.animate(dt)
           
            #---------------------------#
            #Bullet collision with enemy 
        else:
            self.death_timer()
            #Bullet collision with enemy 
            #---------------------------# 
    
    #Enenimes  MOVEMENT       
    #---------------------------#
#Enenimes           
#---------------------------#

            