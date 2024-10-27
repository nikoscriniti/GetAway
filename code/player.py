from settings import *

# this will be the player/sprite
class Player(pygame.sprite.Sprite): #has to inherit and be the child class of the sprite in pygame
    # setup(2)
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
    #----------#
    #Basic Animation (PART 6)
        self.load_images() #have to call load images method before you "CREATE AN IMAGE"         
        self.state, self.frame_index = 'down', 0
    #Basic Animation (PART 6)
    #----------#
        self.image = pygame.image.load(join('images','player','down', '0.png')).convert_alpha() # convert.alpha() make a png smooth its edges.
            # convert_alpha --> creates a new copy of the surface with the desired pixel format. The new surface will be in a format suited for quick blitting to the given format with per-pixel alpha.
            # in my own words it basically converts it to a smooth surface that matches 
        self.rect = self.image.get_frect(center = pos) # for this i am getting a "f"rectangle, and setting it to the center (of the screen) which is equal to the position
        self.hitbox_rect = self.rect.inflate(-78,-78) # CHANGED Y PORTION FROM 0 TO -30 # IMPORTANTTTTTT, allows the hitbox so the image isnt rly going to be the size of the sprite anymore
        #^^ the center of the rectangle needs to be equal to the center of the hitbox

        # movement 
        self.direction = pygame.Vector2() #allows to go to the right (1,0), (0,0)are default values
        self.speed = 500 #speed obv
        self.collision_sprites = collision_sprites # we can keep the collision logic inside the player, allows us to create another method of collision

    #----------#
    #Basic Animation (PART 6)
    def load_images(self): 
        self.frames = {'left': [],'right': [],'up': [],'down': []} #NAMES OF THESE KEYES HAVE TO MATCH THE FOLDER INSIDE OF THE PLAYER# dictionaries with 4 key value pairs (one for every anaimations) basically one for every single movement in that anaimation  

        for state in self.frames.keys():  #keys of the dictionrary are going to be the states of the game 
            for folder_path, sub_folders,file_names in walk(join('images','player',state)): #using a for loop to see the inforation in that list created below in a easier way
                if file_names:# meaning if theirs a file name
                    print(file_names)
                    file_names = [name for name in file_names if name.split(".")[0].isdigit()] #ADDED so their wouldnt be Ds_store ranodm ass file 
                    for file_name in sorted(file_names, key=lambda name: int(name.split(".")[0])):
                        
 #sort file_names by a key, basically the key is set to the split it by the where the . is, the dot seperates the file name where 0.png, 1.png, 2.png is and so on, and all that we only care about index 0, so you put [0] bc thats always the index in the string, and finally put an int before it all so the index postion string becomes an ACTUAL number that can be sorted:::: THIS ALL IS BASCIALLY NOT NEEDED IF YOU JUST SORT THE FILE IN THE FOLDER ON YOUR LAPTOP: LITERALLY COULD JUST BE "for file_name in file_names:"
                        full_path = join(folder_path, file_name) #combine folder_path with file name
                        surf = pygame.image.load(full_path).convert_alpha() #importing a surface... surf ----> pygame.image.load(full_path).convert_alpha(), to get this to happen we first have to create antoher for loop above this whole big one
                        self.frames[state].append(surf) #get the state of the frames, and then append the surface to the list
        print(self.frames)
            #print(info) # this for loop gives us 5 tuples that dispaly, first value rreturned is a little diffrent then the rest. Generally getting three values returned, the first is folder path you are currenly in, the second is all of the sub folders, the third is the file names 
                #^^ not getting the files, just the name of one
        #print(list((walk(join('images','player')))) #wrap in a list to  see all the info pop up in the terminal

    #Basic Animation (PART 6)
    #----------#

    def input(self): # 3
        keys = pygame.key.get_pressed()
        self.direction.x = (int(keys[pygame.K_RIGHT] or keys[pygame.K_d] )) - (int(keys[pygame.K_LEFT] or keys[pygame.K_a]))    #ADDDED "or keys[pygame.K_d]" d key on the key board --->     #GUN EDITION ---> ACtual bullet image
 # allows the actual movment from right to left
    #^^ SO IMPORTANT
    # THE TWO VALUES THAT ARE BEING SUBTRACTED... ARE BOOLEAN VALUES (CAN EITHER BE TRUE OR FALSE)
        self.direction.y = (int(keys[pygame.K_DOWN] or keys[pygame.K_s])) - (int(keys[pygame.K_UP ] or keys[pygame.K_w]))

        # when you go diagonally it would normally go reallllyyy fast... bc self.direction isnt being normalized
        #^^^ fixed below
        if self.direction: #lines 29 to 32 allow the movmeent speed to be constant
            self.direction = self.direction.normalize()
        else:
            self.direction = self.direction # can be 0 and 0 value or it will just stay at self.direction


    def move(self, dt): # (2) 
        # allows the character to move around, #movment works with this
        self.hitbox_rect.x += self.direction.x * self.speed * dt #chnaged from         self.rect.center += self.direction * self.speed * dt  ----  to  ----  self.rect.x(OR)y += self.direction * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

        

    def collision(self, direction): # the second paramater of direction allows us to see what direction we want to work with, it can either be vertical or horizontal # inroder to acccess this just yet 
        #getting all the obsticles below
        for sprite in self.collision_sprites: # allows the main sprite to go under the collsion sprites
            if sprite.rect.colliderect(self.hitbox_rect): #ADDDED --> hitbox
                #print('overlap')
                if direction == 'horizontal':
                    if self.direction.x > 0: # the player will stop  if the direction is greater then 0 from the collsion sprite( meaning it is about to touch the collsion sprtie), in this case the player image is quite large as of now, so their appears as a gap, and leaves some black space in between (REMEMBER THIS FOR WHEN THE SPRITE IS CHANGED "due to "powers")
                        # ADDDED -> added the hitbox feature, before we added this hitbox feature we didint check if the hitbox of the sprite checked with the collsion sprite, all we did before this was set the hitbox center to the main sprite center, but didnt not check for collsions
                        self.hitbox_rect.right = sprite.rect.left #set them equal to one another so it cant move, basically setting the left side of the collision object to the right side of the sprite object
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right #set them equal to one another so it cant move
                    #^ checking if self.direction.x is smaller then 0, means we are moving to the left
                else:
                    if self.direction.y < 0: #if the main sprite is moving up
                        self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: #if the main sprite is moving up
                        self.hitbox_rect.bottom = sprite.rect.top
                

    #----------#
    #Basic Animation (PART 6)
    def animate(self,dt): # basically two methods here, state and animate, anaimate will happen based on the state we give, to know the state we need to know the direction, we know the direction by what we already have, if x is greater then 0 then we know its going left
        #******************************************************#
        #GET STATE
            
            #based on direction
        if self.direction.x != 0: #if zero its not moving
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0: #if zero its not moving
            self.state = 'down' if self.direction.y > 0 else 'up' #direction set to down, if direction is greater then 0 else it will be set to up (i.e if its less then 0)
        
        #GET STATE
        #******************************************************#


        #******************************************************#
        #ANIMATE
        
        self.frame_index = self.frame_index + 5 *dt if self.direction else 0# UPDATE so the character is not moving all the time; do all that (meaning update the phrases (bascially all of animate method/fucntion)) if self.direction is the case (meaning the character is moving) else the self.frames should be set to 0 which is the int value we changed the first postion of each image to... and that first image is 0, 0 image is the character in the still postiion for whatever postion it is in 
        # ORIGINALLY: self.frame_index += 5 *dt
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        
        #ANIMATE
        #******************************************************#

    #Basic Animation (PART 6)
    #----------#

    def update(self, dt):
        self.input()
        self.move(dt)
        #----------#
        #Basic Animation (PART 6)
        self.animate(dt) # have to actually call the function
        #Basic Animation (PART 6)
        #----------#
