#THIS IS FOR THE CAMERRRRAAAAAAAAA  (allowing the main sprite to move through the whole map)
from settings import *

class AllSprites(pygame.sprite.Group): # this is copy of a sprite group
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface() #getitng the display surface from anywhere inside the code so we dont need surface in the parameter of the function below (the "draw" fucntion/method)
        self.offset = pygame.Vector2()#turning the vector into an artibute 

    def draw(self, target_pos): #overiding the draw method in class game in the main fucntion
        
        self.offset.x = -(target_pos[0] - (WINDOW_WIDTH / 2)) # subrtracting (+ WINDOW_WIDTH / 2) and then making the whole thing negative so the player isnt always stuck to the left side of the window/screen, it will be centered now 
            #^^ if you dont add the negative number above, the camera follows the player in the OPPOSITE direction
        self.offset.y = -(target_pos[1] - (WINDOW_HEIGHT / 2)) # same thing as above but for the vertical aspect 
        
        #--------------------#
        # Y-SORTING
        #lists below (will be sorted thru)
        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground') ] #only want to get the ground sprite if it has ____ attribute soooo add hasattr (has attribute)
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground') ] #same as above but has NOT bc its flipped 

        for layer in [ground_sprites, object_sprites]: #sorting thru the lists above
            #^^^ always want to start with the ground sprites thats why it is listed first
           
            for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery): # what this line is doing (if you want to see how it workds just comment out the ground level) but whwat its doing is comapring the center positon of the character (main sprite) with the center postion of the colliosn objects #need a lambda function#setting a cutsom key
                    #^^^ what this is doing, is looking a list of all the sprites, and goes through all the values of the sprites... sorting from lowest to highest.... but thats not possible at the moment bc if you have if you have more then a ceratin number of sprities it wont.... so the lambda function is used to with the key, the key vlaues are put in the lambda functions which is extracting one value from the sprities , that way we are getting one value from the sprite (which is the cernter value)  
                    #^^^ To allow this to work with the all the ground peieces we have to exclude it from the sorting
                self.display_surface.blit(sprite.image, sprite.rect.topleft +  self.offset) #more research on blit
                    #^ what "+ pygame.Vector2(500,100)"" is doing is adding a pushed away pixel location showing basically black space 500 pixels from 0,0 from the left and top 
                        #^^ this is just where elements are drawn, it does not change the actual position of the elemnts
                    #^whats happening up above is the orgin point of self.offset is from the mainscript/player and then adding everytthing to topleft, bc if the player is getting further to the right, the left needs to be drawn
        # Y-SORTING
        #--------------------#
        