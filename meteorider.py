# Import and Initialising
import pygame
from pygame.locals import *
import random

pygame.init()

# Display
size = (1280, 960)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Meteorider')


# Entities
class SpaceShip(pygame.sprite.Sprite):
    """This is the class that represents the spaceship. I made a list of sprites and updated them in an increment
    manner so that I can get the effect of the ship moving."""

    def __init__(self):
        super().__init__()
        self.sprites_spaceship = []  # This is the list name and I added all the images in this list by appending them.
        self.sprites_spaceship.append(pygame.image.load('images/spaceship1.PNG'))
        self.sprites_spaceship.append(pygame.image.load('images/spaceship2.PNG'))
        self.sprites_spaceship.append(pygame.image.load('images/spaceship3.PNG'))
        self.sprites_spaceship.append(pygame.image.load('images/spaceship4.PNG'))
        self.sprites_spaceship.append(pygame.image.load('images/spaceship5.PNG'))
        self.sprites_spaceship.append(pygame.image.load('images/spaceship6.PNG'))
        self.sound_spaceship = pygame.mixer.Sound("sound/beep.wav")
        self.sound_spaceship_ambient_sound = pygame.mixer.Sound("sound/ambient_sound.mp3")
        self.sound_spaceship_ambient_sound.set_volume(0.1)
        self.beep_count = 0  # This is used to synchronise the beep with the sprite.
        self.current_sprite_spaceship = 0  # This is used as Index for the sprite_spaceship list.
        self.image = self.sprites_spaceship[self.current_sprite_spaceship]
        self.image = pygame.transform.scale(self.image, (1280, 960))
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]

    def update(self):

        """The update function increments the current_sprite_spaceship (index of the sprite list)so that we get the
         effect of the sprite moving. Here a floating value is used to control the speed of the movement."""

        if game_lost:  # About the boolean variable game_lost in line 200.
            self.current_sprite_spaceship += 0.02
            if int(self.current_sprite_spaceship) >= len(self.sprites_spaceship):
                self.current_sprite_spaceship = 0
                self.beep_count = 0
            if int(self.current_sprite_spaceship) == self.beep_count:  # This if statement checks whether the value of
                self.sound_spaceship.play()  # index have been changed to a whole number and then make the beep sound
                self.sound_spaceship_ambient_sound.play()  # synchronous.
                self.beep_count += 1
            self.image = self.sprites_spaceship[int(self.current_sprite_spaceship)]
            self.image = pygame.transform.scale(self.image, (1280, 960))
        else:  # The contradictory to game_lost is to kill the whole instance. More about this in line 200.
            self.image = pygame.transform.scale(self.image, (0, 0))
            self.rect = pygame.Rect(0, 0, 0, 0)
            self.kill()
            return


class Meteorite(pygame.sprite.Sprite):
    """This is the class that represents a meteorite. Here also I have defined a list of sprites for the explosion.
    The meteorite moving is achieved through increasing the size of the meteorite using the transform.scale() method.
    The initial image is the meteorite image and when we hit the meteorite using the mouse pointer the images are
     initialised from the sprite list which is the sprites for the explosion"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites_blast = []
        self.image = pygame.image.load("images/meteorite.PNG")
        self.sprites_blast.append(pygame.image.load('images/blast1.PNG'))
        self.sprites_blast.append(pygame.image.load('images/blast2.PNG'))
        self.sprites_blast.append(pygame.image.load('images/blast3.PNG'))
        self.sprites_blast.append(pygame.image.load('images/blast4.PNG'))
        self.current_sprite_blast = 0  # Index
        self.width = 45.0  # We are using a width and height variable in the class so that it would help us in
        self.height = 45.0  # not losing the values of width and height to increment properly.
        self.value_increment = 1.0  # Increment for height and width
        self.destroyed = False  # This boolean checks whether the meteorite has been destroyed or not
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound("sound/meteorite_explosion.mp3")
        self.rect.center = (random.randint(80, 1200), random.randint(100, 500))  # The center has been
        # randomly created so that the meteorites would be randomly approaching the spaceship.
        self.center_x = self.rect.centerx  # Saves the value of center x and y so that we can use it when the meteorite
        self.center_y = self.rect.centery  # is increasing is length and helps in not losing the center value

    def moving(self):

        """ This controls the meteorite size increase which would help use in achieving the effect of meteorite moving
        towards the spaceship and the size is only allowed to be increase to a height of 750.0 which would in turn mean
         that the meteorite has hit the spaceship."""

        if self.height <= 750.0 and not self.destroyed:  # The meteorite size is only increased upto 750.0 or if
            self.height += self.value_increment  # the meteorite is destroyed it would stop increasing.
            self.width += self.value_increment
            self.value_increment += 0.3
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.rect.size = (self.width, self.height)
            self.rect.center = (self.center_x, self.center_y)

    def destroy_sound(self):
        self.sound.play()

    def hit(self, pos):
        return self.rect.collidepoint(pos)

    def collide(self):
        global game_lost  # Is a really important method that checks whether a meteorite has collided with the
        if self.height >= 750.0:  # spaceship and in turn would set the value of game_lost to False. More about
            game_lost = False  # game lost in line 200.

    def update(self):

        """Here we have the starting condition to be game_lost = False (I did not use game_last = True in the beginning
        and as game_lost is used in so many places I will not be able to correct my mistake now) which when fulfilled 
        would have another if condition inside in which one is to check whether the last meteorite destroy animation
        has been finished and when finished the spaceship_destroyed = False is set which is useful for the condition
        in line 287. The second condition would be only true once we click the mouse button to destroy the meteorite
        which was triggered in line 265. The third condition is the normal condition which would be true unless the
        previous conditions are fulfilled"""

        if not game_lost:  # Line 200.
            if int(self.current_sprite_blast) < len(self.sprites_blast):  # The last blast of meteorite.
                self.current_sprite_blast += 0.15
                if int(self.current_sprite_blast) < len(self.sprites_blast):
                    self.image = self.sprites_blast[int(self.current_sprite_blast)]
                    self.image = pygame.transform.scale(self.image, (self.width, self.height))
            else:
                global spaceship_destroyed  # After the last blast this condition is set to false which is helpful
                spaceship_destroyed = False  # in line 287.
                self.image = pygame.transform.scale(self.image, (0, 0))  # After the last blast the object is 
                self.kill()  # destroyed here.
                self.rect = pygame.Rect(0, 0, 0, 0)
                return

        elif self.destroyed:  # The self.destroyed is only true when mouse button down in line 265.
            if int(self.current_sprite_blast) < len(self.sprites_blast):  # This would trigger the blasting of
                self.current_sprite_blast += 0.2  # the meteorite.
                if int(self.current_sprite_blast) < len(self.sprites_blast):
                    self.image = self.sprites_blast[int(self.current_sprite_blast)]
                    self.image = pygame.transform.scale(self.image, (self.width, self.height))
            else:  # And after the meteorite destroy animation the object is killed.
                self.image = pygame.transform.scale(self.image, (0, 0))
                self.kill()
                self.rect = pygame.Rect(0, 0, 0, 0)
                return

        else:
            self.sound.set_volume(0.1)
            self.moving()
            self.collide()


class CrossHair(pygame.sprite.Sprite):
    """The CrossHair class is a simple class whose only purpose is to be a crosshair sprite on the mouse position."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/crosshair.PNG")
        self.image = pygame.transform.scale(self.image, (35, 45))
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        self.sound = pygame.mixer.Sound("sound/laser.wav")

    def laser_sound(self):
        self.sound.play()

    def update(self):

        """The same logic as all the previous class updates. When game_lost = False, the crosshair object will also be
        killed."""

        if not game_lost:
            self.image = pygame.transform.scale(self.image, (0, 0))
            self.kill()
            self.rect = pygame.Rect(0, 0, 0, 0)
            return
        else:
            self.rect.center = pygame.mouse.get_pos()


class Fire(pygame.sprite.Sprite):
    """This class Fire is only used when we shoot the laser beam .e when we push the mouse button down. To achieve
    this behaviour we once more use the sprite listing method and incrementing each sprite."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites_fire = []  # This is the list name and I added all the images in this list by appending them.
        self.sprites_fire.append(pygame.image.load('images/crosshair.PNG'))
        self.sprites_fire.append(pygame.image.load('images/fire4.PNG'))
        self.sprites_fire.append(pygame.image.load('images/fire3.PNG'))
        self.sprites_fire.append(pygame.image.load('images/fire2.PNG'))
        self.sprites_fire.append(pygame.image.load('images/fire1.PNG'))
        self.current_sprite_fire = 0  # The Index.
        self.image = self.sprites_fire[self.current_sprite_fire]
        self.image = pygame.transform.scale(self.image, (35, 45))
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        self.fire_boolean = True  # This fire boolean is turned to false when the mouse button is clicked down in line
        # 270

    def update(self):

        """As currently I did not know any other method to achieve the same effect in the sprite list I not only added
        the sprite for the laser beam but also the crosshair at the 0 th position of the sprite list. This is because
        I encountered a situation where I had to use the image attribute in the constructor and if the image attribute
         has the starting ring of the laser beam it would not be right. So I added the crosshair and set up a
         condition inside game_lost when fire_boolean is false which is when the mouse button is clicked 
         start with the second image in the sprite list and increment it to get the animation effect and after this 
         effect the fire.boolean is turned to True and the crosshair is brought back."""

        if game_lost:
            if not self.fire_boolean:  # As mentioned in the description of update method.
                if int(self.current_sprite_fire) >= len(self.sprites_fire) - 1:  # These if else conditions here are
                    self.fire_boolean = True  # used to achieve the desired effect that when the mouse button is 
                    self.current_sprite_fire = 4.0  # pressed down the first element of the list is shown and after
                if self.current_sprite_fire == 0:  # the last element self.fire_boolean is set to true to not make this
                    self.current_sprite_fire += 1  # laser beam shoot unless mouse button pressed and the 
                else:  # current_sprite_fire is set to 4.0 to make the last element before condition is turned to false
                    self.current_sprite_fire += 0.8  # be the laser itself and not the crosshair.
                self.image = self.sprites_fire[int(self.current_sprite_fire)]
                self.image = pygame.transform.scale(self.image, (40, 40))
                self.rect = self.image.get_rect()
                self.rect.center = pygame.mouse.get_pos()
            else:
                self.current_sprite_fire = 0  # The crosshair is set back here.
                self.image = self.sprites_fire[int(self.current_sprite_fire)]
                self.image = pygame.transform.scale(self.image, (35, 45))
                self.rect = self.image.get_rect()
                self.rect.center = pygame.mouse.get_pos()
                self.fire_boolean = True
        else:  # This is when game_lost is set to false and the object is killed.
            self.image = pygame.transform.scale(self.image, (0, 0))
            self.kill()
            self.rect = pygame.Rect(0, 0, 0, 0)
            return


# Entities that are not classes.
sprite_group1 = pygame.sprite.Group()
sprite_group2 = pygame.sprite.Group()
spaceship = SpaceShip()
cross_hair = CrossHair()
fire = Fire()
sprite_group1.add(spaceship)
sprite_group1.add(cross_hair)
sprite_group1.add(fire)
bg = pygame.image.load("images/bg.PNG")
bg = pygame.transform.scale(bg, (1280, 960))
bg_red = pygame.Surface(size)
bg_red.fill((252, 45, 0))
font = pygame.font.Font(None, 100)
sound_game_over = pygame.mixer.Sound("sound/game_over.wav")

# Action --> Alter
# Assign Variables
keepGoing = True
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 200)
meteorite_number = 1  # Is used in line 292 to help in increasing the speed after meteorite number has reached a maximum
# number.
meteorite_speed_increment = 4  # This is the speed with which it increases.
ctr = 0  # This helps in knowing how many meteorites have been destroyed.
spaceship_destroyed = True  # Semantically very wrong should have been initialized with false.
game_lost = True  # Same here very wrong should have been initialized with false.

# Loop
while keepGoing:
    # Timer
    clock.tick(60)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGoing = False
            break
        elif event.type == MOUSEBUTTONDOWN and game_lost:
            cross_hair.laser_sound()
            fire.fire_boolean = False  # Needed for the laser line 214. Semantically wrong.
            for meteorite in sprite_group2:
                if meteorite.hit(pygame.mouse.get_pos()):
                    ctr += 1
                    meteorite.destroyed = True  # Need to show that the meteorite has been destroyed.
                    meteorite.destroy_sound()

        elif event.type == USEREVENT and game_lost:
            pygame.time.set_timer(pygame.USEREVENT, 2000)  # When the event gets triggered a new meteorite object
            for asteroid in range(0, int(meteorite_number)):  # is created.
                meteorite_instance = Meteorite()
                meteorite_instance.value_increment = meteorite_speed_increment
                sprite_group2.add(meteorite_instance)
            if int(meteorite_number) < 3:  # The meteorite_number would increase upto a maximum of 2.
                meteorite_number += 0.4
            elif int(meteorite_number) >= 3:  # When the meteorite_number is bigger than 2 the number would turn to
                meteorite_number = 1  # 1 and instead the speed of the incoming meteorite is increased.
                meteorite_speed_increment += 5

    screen.fill((0, 0, 0))
    sprite_group2.update()
    sprite_group1.update()
    if game_lost:  # Semantically Wrong. What is meant here is that if game is not over draw this.
        screen.blit(bg, (0, 0))
        sprite_group2.draw(screen)
        sprite_group1.draw(screen)
    else:  # Else if the game is over and if spaceship_destroyed is not yet set to false which is when in line 131
        if spaceship_destroyed:  # the last meteorite blast animation which destroyed the ship has not been completed
            sound_game_over.set_volume(0.2)  # do these.
            screen.blit(bg, (0, 0))
            sprite_group2.draw(screen)
            sound_game_over.play()
        else:  # If the last meteorite blast animation is also over draw the screen red.
            screen.blit(bg_red, (0, 0))
    text = font.render(str(ctr), True, Color('white'))  # Text at last because it should be not overdrawn
    screen.blit(text, (613, 100))

    pygame.display.flip()
