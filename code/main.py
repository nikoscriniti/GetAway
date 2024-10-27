#OPEN THE WHOLE Vampire Survivor folder in vs code, wont fun bc of the paths' of the images 

from settings import *
from player import Player
from sprites import *
from random import randint, choice 
import sys
#---------------------------#
#map edition
from pytmx.util_pygame import load_pygame #importing a tmx map and use it in the code
#map edition
#---------------------------#
#---------------------------#
#Camera edition
from groups import *
#Camera edition
#---------------------------#
WHITE = (255, 255, 255)


# Vector 2
    #---> an ordered pair of numbers (labeled x and y), 
        #which can be used to represent a number of things, 
        #such as: A point in 2D space (i.e. a position on a plane). 
        #A direction and length across a plane.
    

class Game: 
    def __init__(self):
        #setup 
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #taken directly from the settings (ALTER THIS)
        pygame.display.set_caption("MOBILE GAME --> 'GET AWAY!'") #just the name of the window (CHANGE)
        self.clock = pygame.time.Clock() # captial C on Clock
        self.running = True #default to being true
        self.game_active = True  # **New flag to check if the game is active**

        


        #groups
        self.all_sprites = AllSprites() # change from pygame.sprite.Group() to AllSprites bc this is a class now (basically just wrapped it in a class)
        self.collision_sprites = pygame.sprite.Group() #allow us to have access to all the collsion sprites #is going to allow us to have easy access to all the sprites
        #---------------------------#
        #GUN EDITION ---> ACtual bullet image
        self.bullet_sprites = pygame.sprite.Group()
        #GUN EDITION ---> ACtual bullet image
        #---------------------------#
        #---------------------------#
        #Enenimes 
        self.enemy_sprites = pygame.sprite.Group()
        #Enenimes           
        #---------------------------#
        
       
        #---------------------------#
        #GUN EDITION ---> BULLET
        #gun timer 
        self.can_shoot = True 
        self.shoot_time = 0 
        self.gun_cooldown = 100  # this will determine how many bullets can appear per second #100 millaseconds (can shoot 10 bullets per second )
        #GUN EDITION ---> BULLET
        #---------------------------#

        #enemy timer
        
        #---------------------------#
        #Enenimes  
        #The enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300) # getting an enemy spawn every 300 milleseconds
        self.spawn_positions = [] #empty list, all the markers on the map (defined in titled) we want to place the position of all the enenmy markers in this empty list 

        #Enenimes           
        #---------------------------#
        

        #audio 
            #-------------------------------------#
            #Fixxing error for the restart game (when the audio would play over each other, as their instances were ran)
        self.setup_audio()
            #Fixxing error for the restart game (when the audio would play over each other, as their instances were ran)
            #-------------------------------------#
        #self.shoot_sound = pygame.mixer.Sound(join('audio', 'knifeslice.mp3')) #shooot sound
        #self.shoot_sound.set_volume(0.4)
       # self.impact_sound = pygame.mixer.Sound(join('audio', 'impact.ogg'))
        #self.music = pygame.mixer.Sound(join('audio',"80's-city-game-music.mp3"))
        
        #background audio
        self.music.set_volume(0.2)
        self.music.play(loops = -1) #important for the music to loop# loops so it plays forever, it is also in this postion so the music will play forever and right at the start (ALSO ADD: add a feature where you can stop the music (most mobile games have this so idk would be good))
                # CURRENTLY: ERROR: error with the audio file (game music) playing-over/still-playing-the-old-file when the user dies and game restarts

        #SETUP
        #---------------------------# 
        #GUN EDITION ---> ACtual bullet image
        self.load_images()
        #GUN EDITION ---> ACtual bullet image
        #---------------------------#
        #---------------------------#
        #map edition
        self.setup()
        #map edition
        #---------------------------#
       
       #sprites
        # self.player = Player((500, 300), self.all_sprites, self.collision_sprites)  #GOT RIDE OF BECAUE WE NO LONGEr NEED To CREATE ONE INSTANCE OF THE PLAYER, WE START HIM IN THE MIDDLE OF THE MAP#IMPORRRTANTTTT --> all_sprites are added with collusions sprites, but not in the same group, collusionsprites is itself sepeearte, player just has access to it (for obv reasons it will need to hit this collusion, and not colloide with itself) #YOU CAN CHANGE THESE POSITIONS
        # ^ running the Player class and then putting the two values of pos and groups 

        #for i in range(6): #creating 6 collision objects (this number can be altered, its whatever number is in paraenthesis, thats the number thats going to give you the amount of objects)

           # x, y = randint(0,WINDOW_WIDTH), randint(0, WINDOW_HEIGHT) #x set to the first value, y set to the second value
           # w, h = randint(60, 100), randint(50,100) 

           # CollisionSprite((x,y), (w,h), (self.all_sprites, self.collision_sprites)) #IMPORRRTANTTTT --> insdie the ocllisionsprite, youre adding all sprites and collsuions_sprites two sprites esspentially this  #going to need a position, and random size in parenthesis
            #^ the (x,y) and (w,h) are the postion, and then rnaodm size is all_sprints
        #^^ coming from the sprites class
    
    #---------------------------#
    #GUN EDITION ---> BULLET
        
        
    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()

        #-----------------------------#
        #Enenimes
        folders = list(walk(join('images','enemies')))[0][1] #walk and join, then make it a list, and on that list you want to get index 0
        self.enemy_frames = {}
        for folder in folders: #allows to get all the frames
            for folder_path, _, file_names in walk(join('images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                file_names = [name for name in file_names if name.split(".")[0].isdigit()] #ADDED so their wouldnt be Ds_store ranodm ass file 
                for file_name in sorted(file_names, key=lambda name: int(name.split(".")[0])): #if name.split(".")[0].isdigit() else float('inf')):
 #lamdba with a name parameter
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)
       #print(self.enemy_frames)
        
        #Enenimes
        #-----------------------------#

            #-----------------------------#
            #Fixxing error for the restart game (when the audio would play over each other, as their instances were ran)
    def setup_audio(self):
        pygame.mixer.music.stop()  # Ensure any previous music is stopped
        self.shoot_sound = pygame.mixer.Sound(join('audio', 'knifeslice.mp3'))
        self.shoot_sound.set_volume(0.4)
        self.impact_sound = pygame.mixer.Sound(join('audio', 'impact.ogg'))
        self.music = pygame.mixer.Sound(join('audio',"80's-city-game-music.mp3"))
        self.music.set_volume(0.2)
        self.music.play(loops=-1)
            #Fixxing error for the restart game (when the audio would play over each other, as their instances were ran)
            #-----------------------------#


    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:  #before adding "and self.can" it would check on every single frame # without the 0 were getting all the mouse buttons, index 0 allows us to get the left mouse 
            self.shoot_sound.play()  #auido (bullet sound)
            #---------------------------#
            #GUN EDITION ---> ACtual bullet image
            pos = self.gun.rect.center + self.gun.player_direction * 50 
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites)) 
            #GUN EDITION ---> ACtual bullet image
            #---------------------------#
            #print('Shoot')
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            #get the current time then if this is the case
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True
    #GUN EDITION ---> BULLET
    #---------------------------#
   
    #---------------------------#
    # map edition (tiled)
    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))  #research join method a little more
        print(map)
        #****************************************************************
        #Ground layer
        for x, y, image in map.get_layer_by_name('Ground').tiles(): #add titles to return the titles, these lines give us a hug amount of data (on the x and y grid locations not pixel )
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites) #create a sprite fro the x and y pos, then for the surface we want to use an image, and group the groups we want to use self.all_sprites 
                #^^the postion is very important, this x,y postion has to be mutliplied by the tile size (in this case its 64 but i will set later to diff), you have to muiltply that by every postion on the screen of tile,  so for exmaple (0,0) postion is top left, and one over to the right of that is (1,0)
                    #^^ we have the TILE_SIZE stored as a varible in settings.py (i will edit this later)
            #print(x)
            #print(y)
            #print(image)
        #Ground layer   
        #****************************************************************
        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        #Collision objects
        for obj in map.get_layer_by_name('Objects'): # map.get_layer_by_name most commmon way to get layer by name, Objects layer is all the objecst like trees (collision objects)
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites)) # keep (obj.x, obj.y) in a tuple bc its at the pos mark, also collisionsprites is defined in sprites.py, this one line allows no more random (was 6) blocks to apppear 
            #print(obj.x) # x position 
            #print(obj.y) # y position
            #print(obj.image) #surface)
        #Collision objects
        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        for obj in map.get_layer_by_name('Collisions'): # literal name on the file
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites ) # for the gorups, we want self.collision_sprites, so the player can collide with them but they are not visable

        #---------------------------#
        #CAMERA CENTERED TO THE PLAYER
        for obj in map.get_layer_by_name('Entities'): #could be obj or marker, GETTING ALL THE MARKERS (THATS WHAT THIS FOR-LOOP IS DOING)
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
            #print(obj) #print allows to show what is shown through the debugger (what is shown: player (once), then enemy, then none (a bunch of times))
                #---------------------------#
                #GUN EDITION
                    #Creating an instance of the gun in the main function 
                self.gun = Gun(self.player, self.all_sprites) # first of all the gun will not follow the player
                #GUN EDITION
                #---------------------------#
                
            #---------------------------#
            #Enenimes           
            else:    #ALLOW ING TO CHECK FOR ENEMY MARKERS  
               self.spawn_positions.append((obj.x,obj.y)) 
            #Enenimes           
            #---------------------------#
        #CAMERA CENTERED TO THE PLAYER
        #---------------------------#
 
    # map edition (tiled)
    #---------------------------#

    #---------------------------#
    #Bullet collision with enemy 
    
    def bullet_collision(self):
        if self.bullet_sprites: #taking from the __init__ method: self.bullet_sprites
            for bullet in self.bullet_sprites: # if their are colllsions, then check in for bullet in self.bullet_sprites 
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False , pygame.sprite.collide_mask) # also changed true to false, and wrote code under: this is bc their will be a noticable differnce from when the bullet hits the sprtie to the actual time of "death" of that collision sprite# a collide_mask allows more percision on the hits of the collison enemy sprites: wont be as noticable bc the collision sprites are mostly rectangular  # pygame.sprite.spritecollide(sprite, groups (meaning group of sprites), dokill)
                if collision_sprites:
                    self.impact_sound.play() #audio .play() allows a sound to be played
                    for sprite in collision_sprites:
                        sprite.destroy() #created inside sprites of the enmy class
                    bullet.kill()# if their are collisoin sprites wit hthe bullet, kill the bullet (basiclaly remvoeing the bullet )
    #Bullet collision with enemy 
    #---------------------------#
                    
    #---------------------------#
    # PLAyer collision with enenmy 
    def player_collision(self): # could just combine this wilth the bullet_collsion method 
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask): # the collide mask allows for the hitting an enemy more "accurately"
            #self.running = False
            self.game_active = False  # **Set game_active to False on collision**

    # PLAyer collision with enenmy 
    #---------------------------#
    
    def display_game_over(self): #**ADDEDDDD**
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over", True, WHITE)
        restart_text = font.render("Restart", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)) #update the window again, put the text bascially where the player is in the middle (same concept as dividing hte window in half blah blah blah)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

        self.display_surface.blit(game_over_text, game_over_rect)
        self.display_surface.blit(restart_text, restart_rect)
        pygame.display.update()

        while not self.game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        #-------------------------------------#
                        #Fixxing error for the restart game (when the audio would play over each other, as their instances were ran)
                        pygame.mixer.stop() # added before the __init__
                        #Fixxing error for the restart game (when the audio would play over each other, as their instances were ran)
                        #-------------------------------------#
                        self.__init__()  # **Restart the game by reinitializing**
                        
                        self.run()  # **Restart the game loop**


    def run(self):
        while self.running:
            #time 
            dt = (self.clock.tick() / 1000)
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #check if the event type (while running) is equal to the quit (exiting the game loop and game total)
                    self.running  = False 
            #---------------------------#
            #Enenimes           
                if event.type == self.enemy_event and self.game_active: #**ADDED**
                    #print("spawn enemy")
                    #the choice method allows the game to pick one of the enemy animation frames(for example in thje second parameter)
                        #^^ choice cannot work with values directly, they have to be a list, so you have to convert to a list
                    
                    Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)  #the choice and thing in choice has to be imported and this is for the pos (positions) 
                        #^^ for frames, work will be done inside load_images    
            #Enenimes           
            #---------------------------#
            
            if self.game_active: #**ADDED**
                #update
                #---------------------------#
                #GUN EDITION ---> BULLET
                self.gun_timer()
                self.input()#before we are updating evertthing else
                #GUN EDITION ---> BULLET
                #---------------------------#
                    # --------------------
                self.all_sprites.update(dt)
                    # --------------------
                #---------------------------#
                #Bullet collision with enemy 
                self.bullet_collision() # when an enemy is hit with a bullet, it will disappear 
                #Bullet collision with enemy 
                #---------------------------#
                
                #---------------------------#
                # PLAyer collision with enenmy 
                self.player_collision() # see when you call a method insdie a class you have to put the "self" feature (just remember this)
                # PLAyer collision with enenmy 
                #---------------------------#
                
                
                #draw
                self.display_surface.fill("black") # for right now, this allows the sprite (when moved) to not be seen, but rly it is being covered up (works maninly with the Player class)
                self.all_sprites.draw(self.player.rect.center) # self.display_surface not neeed (inside parenthesis) anymore bc of the class ALLsprites
                    #^^ added self.player.rect.center, insdie of partenthis to make sure the "camera" follows the main sprite
                pygame.display.update() #TRY --> pygame.display.flip() ---> notice the flip (works interchanable)
                #---------------------------#
                #GUN EDITION ---> BULLET
                #print(self.bullet_sprites) #got rid of bc no need to print the bullet sprites insdie the game loop
                #GUN EDITION ---> BULLET
                #---------------------------#`
            else: #**ADDED**
                self.display_game_over() #**ADDED**
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
