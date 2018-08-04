import pygame
import time
import random
from pygame.locals import *

"""
Things to fix:
- Clean up code a bit more
Things to add:
- Title and menu
- Troop and castle upgrade
- Fonts
- Graves/marker to show a troop has died rather than them just disappearing
- Castle defense mechanism
"""

width = 1500
height = 600

display = pygame.display.set_mode((width, height))
pygame.display.set_icon(pygame.image.load("images/Castle Blue.png"))
pygame.display.set_caption("Castles")


def text(window, color_, rect, label, font_size):
    """A function that can render and display text on window."""
    font = pygame.font.SysFont("monospace", font_size)
    render = font.render(label, 1, color_)
    new_rect = render.get_rect(center=(rect.x+rect.width/2, rect.y+rect.height/2))
    window.blit(render, new_rect)


class Button:
    """A Button class, built for all kinds of purposes"""
    def __init__(self, window, rect, message, off_color, on_color, message_color, message_font_size):
        # location
        self.rect = rect
        self.rect[0] -= self.rect[2]/2
        self.rect[1] -= self.rect[3]/2
        # message attributes
        self.message = message
        # on and off colors
        self.color = off_color
        self.off_color = off_color
        self.on_color = on_color
        # message color
        self.message_color = message_color
        # message font
        self.font_size = message_font_size
        # what surface to display on
        self.display = window

    def in_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.Rect(self.rect).collidepoint(mouse_pos[0], mouse_pos[1]):
            return True

    def clicked(self):
        if self.in_button():
            self.color = self.on_color
            if pygame.mouse.get_pressed()[0]:
                return True
        else:
            self.color = self.off_color

    def draw(self):
        pygame.draw.rect(display, self.color, self.rect)
        text(self.display, self.message_color, self.rect, self.message, self.font_size)


class Castle:
    def __init__(self, controls, color_, troop_list):
        self.color = str(color_).lower()
        self.controls = controls
        self.troop_list = troop_list

        # gold IMAGE
        self.gold_image = pygame.image.load("images/Gold.png")

        # time, used to control collection of gold
        self.gold_time = time.time()
        # spawn time interval
        self.spawn_time = time.time()

        if self.color == "blue":  # define a bunch of variables, differing upon color
            self.castle_image = pygame.image.load("images/Castle Blue.png")
            self.rect = self.castle_image.get_rect(topleft=(-40, height-380))  # position the rects, 380, clean
            self.SPAWN_LOCATION = (self.rect.x+320, self.rect.bottom-45-10)
        elif self.color == "orange":  # do the math correlating between the naked numbers and some will make sense
            self.castle_image = pygame.image.load("images/Castle Orange.png")
            self.rect = self.castle_image.get_rect(topleft=(width-380+40, height-380))
            self.SPAWN_LOCATION = (self.rect.x+60, self.rect.bottom-45-10)

        self.k_p = pygame.key.get_pressed()

        # castle stats
        self.stats = {
            "gold": 1000,
            "gold_production": 1,
            "health": 1000,
            "max health": 1000,
            "damage": 10
        }

    def gold_collector(self):
        if time.time()-1 > self.gold_time:
            self.gold_time = time.time()
            self.stats["gold"] += self.stats["gold_production"]

    def gold_draw(self):
        self.gold_collector()
        if self.color == "blue":
            display.blit(self.gold_image, (25, 25))
            text(display, (255, 255, 102), Rect(100, 52, 0, 0), str(self.stats["gold"]), 20)
        elif self.color == "orange":
            display.blit(self.gold_image, (width-75, 25))
            text(display, (255, 255, 102), Rect(self.rect.centerx+50, 52, 0, 0), str(self.stats["gold"]), 20)

    def upgrade(self):
        pass
        # we implement troop upgrades, gold harvesting upgrades, and more here

    def defense(self):
        pass
        # what I plan to do is add some kind of defense mechanism so once a troop gets close enough castle defends
        # and shoots things back. Likely going to be a archer

    def health(self):
        if 0 < self.stats["health"] <= self.stats["max health"]:
            pygame.draw.rect(  # background to health bar, the white part
                display,
                (255, 255, 255),
                (self.rect.centerx-self.stats["max health"]/5/2-1,
                 self.rect.top-10-1,
                 self.stats["max health"]/5+2,
                 7)
            )
            pygame.draw.rect(  # bar actually showing health
                display,
                (0, 255, 0),
                (self.rect.centerx-self.stats["health"]/5/2, self.rect.top-10, self.stats["health"]/5, 5)
            )

    def spawn_troop(self):
        self.k_p = pygame.key.get_pressed()
        if time.time()-1 > self.spawn_time:  # possibly simplify this all to a for loop? later
            self.spawn_time = time.time()

            if self.k_p[self.controls[0]] and self.stats["gold"] >= Swordsman.cost:  # swordsmen
                self.stats["gold"] -= Swordsman.cost
                self.troop_list.append(Swordsman(self.color))

            if self.k_p[self.controls[1]] and self.stats["gold"] >= Rogue.cost:  # rogues
                self.stats["gold"] -= Rogue.cost
                self.troop_list.append(Rogue(self.color))

            if self.k_p[self.controls[2]] and self.stats["gold"] >= Shieldsman.cost:  # shieldsman
                self.stats["gold"] -= Shieldsman.cost
                self.troop_list.append(Shieldsman(self.color))

            if self.k_p[self.controls[3]] and self.stats["gold"] >= Archer.cost:  # archer
                self.stats["gold"] -= Archer.cost
                self.troop_list.append(Archer(self.color))

            if self.k_p[self.controls[4]] and self.stats["gold"] >= Wizard.cost:  # wizard
                self.stats["gold"] -= Wizard.cost
                self.troop_list.append(Wizard(self.color))

    def draw(self):
        if not menu_instance.menu_active:
            self.health()
            self.gold_draw()
        display.blit(self.castle_image, self.rect)  # draw castle

    def __repr__(self):
        return "Castle: {}({}, {}, {})".format(self.__class__.__name__, self.controls, self.color, self.troop_list)


class Particle:
    def __init__(self, start_loc, color_of_particle):
        self.loc = start_loc
        self.color = color_of_particle
        self.speed = 2
        self.life_time = 5
        self.time = time.time()
        self.killed = False
        self.direction = [-1, -0.5, 0.5, 1][random.randint(0, 3)]
        self.offset = random.randint(-17, 17)

    def animate(self):
        """Animates particle"""
        pygame.draw.rect(
            display,
            self.color,
            (self.loc[0], self.loc[1], 10, 10)
        )
        pygame.draw.rect(
            display,
            self.color,
            (self.loc[0]+self.offset, self.loc[1]+self.offset, 7, 7)
        )  # create 2 more rects
        pygame.draw.rect(
            display,
            self.color,
            (self.loc[0]-self.offset, self.loc[1]+self.offset, 7, 7)
        )  # but position randomly differently

        self.loc[0] += self.direction  # we don't handle the movement with pygame.rect.move_ip because
        # that method only accepts integers
        self.loc[1] -= self.speed  # y's are the same, and do not go in different directions
        self.speed -= 0.02

    def kill(self):
        """After the particle has existed for long enough, we can delete it."""
        if self.time <= time.time() - self.life_time:
            self.killed = True

    def all(self):
        """all calls all the neccesary parts of the particle, allowing it to move, be drawn, and more in one method"""
        self.animate()
        self.kill()

    def __repr__(self):
        return "Particle: {}({}, {})".format(self.__class__.__name__, self.loc, self.color)


class Projectile:
    def __init__(self, pos, color_):
        self.image = None
        self.rect = None
        self.start_pos = pos
        self.color = color_
        self.collide_with_target = False
        self.max_distance = 300
        self.distance = 0
        if self.color == "blue":
            self.direction = 1
        elif self.color == "orange":
            self.direction = -1

    def move(self):
        # update rect from image based on color
        self.rect.move_ip(3*self.direction, 0)
        self.distance += 3*self.direction
        if self.distance > self.max_distance:
            self.collide_with_target = False

    def draw(self):
        display.blit(self.image, self.rect)

    def __repr__(self):
        return "Projectile: {}({}, {})".format(self.__class__.__name__, self.start_pos, self.color)


class Arrow(Projectile):
    def __init__(self, pos, color_):
        super(Arrow, self).__init__(pos, color_)
        if self.color == "blue":
            self.image = pygame.image.load("images/Arrow blue.png")
            self.rect = self.image.get_rect(midleft=self.start_pos)
        elif self.color == "orange":
            self.image = pygame.image.load("images/Arrow orange.png")
            self.rect = self.image.get_rect(midright=self.start_pos)

    def __repr__(self):
        return "Arrow: {}({}, {})".format(self.__class__.__name__, self.start_pos, self.color)


class Fireball(Projectile):
    def __init__(self, pos, color_):
        super(Fireball, self).__init__(pos, color_)
        if self.color == "blue":
            self.image = pygame.image.load("images/Fireball blue.png")
            self.rect = self.image.get_rect(midleft=self.start_pos)
        elif self.color == "orange":
            self.image = pygame.image.load("images/Fireball orange.png")
            self.rect = self.image.get_rect(midright=self.start_pos)

    def __repr__(self):
        return "Fireball: {}({}, {})".format(self.__class__.__name__, self.start_pos, self.color)


class Troop:
    def __init__(self, color_):
        self.color = str(color_).lower()
        self.stats = {
            "speed": 1,  # changed in child classes, but defaults to these values
            "damage": 10,  # it's even mutable, in case we want to change just one stat
            "health": 100,
            "max health": 100,
            "attack_speed": 0.5,
            "melee": True,
            "range_immune": False
        }
        if self.color == "blue":
            self.image = pygame.image.load("images/Swordsman blue.png")  # images default to this
            self.rect = self.image.get_rect(center=castle_blue.SPAWN_LOCATION)
            self.enemy_troops = orange_troops
            self.enemy_castle = castle_orange
            self.projectile_list = projectile_list_blue
        elif self.color == "orange":
            self.image = pygame.image.load("images/Swordsman orange.png")
            self.rect = self.image.get_rect(center=castle_orange.SPAWN_LOCATION)
            self.enemy_troops = blue_troops
            self.enemy_castle = castle_blue
            self.projectile_list = projectile_list_orange

        self.collide = None
        self.attack_timer = time.time()+self.stats["attack_speed"]  # they come out locked and loaded
        self.attack_time = time.time()-self.stats["attack_speed"] > self.attack_timer
        self.dead = False

    def draw(self):
        display.blit(self.image, self.rect)

    @staticmethod
    def handle_particles():
        """draw and move the particles after they are created -
         they are created during collision, but still continued after"""
        global particle_list
        for particle in particle_list:
            particle.all()

        # filter list
        particle_list = \
            [particle for particle in particle_list if not particle.killed]

    def handle_projectile(self):
        """draw and move the projectiles after they are created - this has to bee continued even after collision"""
        global  projectile_list_orange, projectile_list_blue
        if not self.stats["melee"]:
            for projectile in self.projectile_list:  # moves and draws
                projectile.move()
                projectile.draw()
                # then append projectiles to global projectile lists and draw and attack.
                projectile_collide = projectile.rect.collidelist(self.enemy_troops)  # define variables that help us
                collide_info = projectile_collide != -1, projectile_collide  # detect and handle collision
                # handling
                if projectile.rect.colliderect(self.enemy_castle):  # attacking castles
                    self.enemy_castle.stats["health"] -= self.stats["damage"]/3  # subtract health, but with less damage
                    # append CASTLE GREY particles
                    particle_list.append(
                        Particle(
                            list(projectile.rect.midright if self.color == "blue" else projectile.rect.midleft),
                            (150, 150, 150),
                        )
                    )
                    projectile.collide_with_target = True
                elif collide_info[0]:  # attacking troop
                    if not self.enemy_troops[collide_info[1]].stats["range_immune"]:  # if the enemy is not range immune
                        self.enemy_troops[collide_info[1]].stats["health"] -= self.stats["damage"]  # subtract health
                        particle_list.append(  # append particles that are blood colored
                            Particle(
                                list(projectile.rect.midright if self.color == "blue" else projectile.rect.midleft),
                                (238, 7, 7)
                            )
                        )
                    else:  # else, if the enemy IS range immune
                        self.enemy_troops[collide_info[1]].stats["health"] -= self.stats["damage"]/4  # subtract health
                        # but damage is decreased
                        particle_list.append(
                            Particle(  # append particle the color of the shieledsman shield
                                list(projectile.rect.midright if self.color == "blue" else projectile.rect.midleft),
                                (102, 102, 102)  # a nice dark gray
                            )
                        )
                    projectile.collide_with_target = True

        # update local list afterwards
        if self.color == "blue":
            self.projectile_list = projectile_list_blue
        elif self.color == "orange":
            self.projectile_list = projectile_list_orange

        # filter list of projectiles
        self.projectile_list = \
            [projectile for projectile in self.projectile_list if not projectile.collide_with_target]

    def move(self):
        """Controls moving and attacking-and also essentially everything related to the troop that moves"""
        # update the attack time. for all colors
        self.attack_time = time.time()-self.stats["attack_speed"] > self.attack_timer
        if self.color == "blue":
            self.enemy_troops = orange_troops  # we need a fresh version of the list so we add this
        elif self.color == "orange":
            self.enemy_troops = blue_troops  # otherwise we'd have the same list when this instance was instantiated

        self.collide = self.collide_with(self.enemy_troops, list_sprites=True)  # colliding with castle, gives us info
        if self.collide_with(self.enemy_castle) and self.attack_time:
            self.stats["speed"] = 0  # stop all movement
            self.attack_timer = time.time()  # restart attack time clock
            if self.stats["melee"]:  # if it is a melee troop
                self.enemy_castle.stats["health"] -= self.stats["damage"]/3  # subtract health, but lessened
                # when attacking castle damage is divided by 3
                # append CASTLE GREY particles
                particle_list.append(
                    Particle(
                        list(self.rect.midright if self.color == "blue" else self.rect.midleft),
                        (150, 150, 150),
                    )
                )
            else:  # else, if NOT a melee troop
                if self.color == "blue":  # append projectiles based on weapon and color
                    projectile_list_blue.append(self.stats["weapon"](self.rect.center, self.color))
                elif self.color == "orange":
                    projectile_list_orange.append(self.stats["weapon"](self.rect.center, self.color))

        elif self.collide[0]:  # if NOT colliding with a castle and rather a troop
            # this is the attacking
            if self.attack_time:  # if it is attack time...
                self.attack_timer = time.time()  # restart attack time clock
                if self.stats["melee"]:  # if troop is melee
                    # melee troops have a simple attack process: once a collision is detected, do damage
                    self.enemy_troops[self.collide[1]].stats["health"] -= self.stats["damage"]  # subtract enemy health
                    # add blood red particle (looks a bit like blood spraying everywhere I guess)
                    particle_list.append(
                        Particle(
                            list(self.rect.midright if self.color == "blue" else self.rect.midleft),
                            (218, 7, 7),
                        )
                    )
                else:
                    # ranged troops have to be given more instances of a projectile and then we handle that
                    if self.color == "blue":  # append based on weapon and color
                        projectile_list_blue.append(self.stats["weapon"](self.rect.center, self.color))
                    elif self.color == "orange":
                        projectile_list_orange.append(self.stats["weapon"](self.rect.center, self.color))
        else:
            if self.color == "blue":  # IF NOTHING IS COLLIDED WITH
                self.rect.move_ip(self.stats["speed"], 0)  # keep on moving
                # use speed to modify x coordinate, y coordinate stays the same
            elif self.color == "orange":  # movement depends on color
                self.rect.move_ip(-self.stats["speed"], 0)
                # orange moves left, so speed is negated

        self.handle_projectile()  # then all the projectiles are handled and methods of it are called

    def collide_with(self, target, list_sprites=False):
        """Works only for troops, unfortunately"""
        if not list_sprites:  # for colliding with castle
            if self.stats["melee"]:
                collide = self.rect.colliderect(target.rect)
            else:
                if self.color == "blue":
                    collide = Rect(self.rect.x, self.rect.y, self.rect.width+self.stats["range"], self.rect.height)\
                        .colliderect(target.rect)
                elif self.color == "orange":  # range is shortened when targeting castles
                    collide = Rect(self.rect.x-self.stats["range"], self.rect.y, self.rect.width+self.stats["range"],
                                   self.rect.height).colliderect(target.rect)
            return collide

        else:  # for colliding with troops
            if self.stats["melee"]:
                collide = self.rect.collidelist(self.enemy_troops)
            else:
                if self.color == "blue":  # we have to do this because orange goes left and blue goes right
                    collide = Rect(self.rect.x, self.rect.y, self.rect.width+self.stats["range"], self.rect.height)\
                        .collidelist(target)
                elif self.color == "orange":
                    collide = Rect(self.rect.x-self.stats["range"], self.rect.y, self.rect.width+self.stats["range"],
                                   self.rect.height).collidelist(target)

            return collide != -1, collide  # -1 is the default if nothing collided

    def health(self):
        if 0 < self.stats["health"] < self.stats["max health"]:
            pygame.draw.rect(  # background to health bar, the white part
                display,
                (255, 255, 255),
                (self.rect.centerx-self.stats["max health"]/2-1,
                 self.rect.centery-60-1,
                 self.stats["max health"]+2,
                 5+2)
            )
            pygame.draw.rect(  # bar actually showing health
                display,
                (0, 255, 0),
                (self.rect.centerx-self.stats["health"]/2, self.rect.centery-60, self.stats["health"], 5)
            )
        if self.stats["health"] <= 0:
            self.dead = True

    def all(self):
        """Calls all vital parts in one neat bundle/method"""
        self.health()
        self.draw()
        self.move()

    def special(self):
        """Special action for troop (ex: Swordsman can do extra damage at times). Not all troops have specials"""
        pass

    def __repr__(self):
        return "Troop: {}({})".format(self.__class__.__name__, self.color)
       
        
class Swordsman(Troop):
    cost = 10

    def __init__(self, color_):
        super(Swordsman, self).__init__(color_)
        self.color = color_
        self.stats = {
            "speed": 1,
            "damage": 10,
            "health": 100,
            "max health": 100,
            "attack_speed": 0.5,
            "melee": True,
            "range_immune": False
        }
        # image and image rects are defaulted to the swordsman, so we have no need to re-define them.
        # but we do it anyways to avoid confusion ;)  - PROBABLY GONNA CLEAN IT UP
        if self.color == "blue":
            self.image = pygame.image.load("images/Swordsman blue.png")  # images default to this
            self.rect = self.image.get_rect(center=castle_blue.SPAWN_LOCATION)
        elif self.color == "orange":
            self.image = pygame.image.load("images/Swordsman orange.png")
            self.rect = self.image.get_rect(center=castle_orange.SPAWN_LOCATION)

        self.stats["crit_chance"] = 1

    def special(self):
        """This is the Swordsman special ability. He can do extra critical damage"""
        self.stats["damage"] = 10  # ten is the normal for swordsman
        if random.randint(self.stats["crit_chance"], 10) == 10 and self.collide[0]:
            self.stats["damage"] += 10


class Rogue(Troop):
    cost = 25

    def __init__(self, color_):
        super(Rogue, self).__init__(color_)
        self.color = color_
        self.stats = {
            "speed": 2,
            "damage": 7,
            "health": 40,
            "max health": 40,
            "attack_speed": 0.75,
            "melee": True,
            "range_immune": False
        }
        if self.color == "blue":
            self.friendly_castle = castle_blue
            self.image = pygame.image.load("images/Rogue blue.png")
            self.rect = self.image.get_rect(
                center=(castle_blue.SPAWN_LOCATION[0], castle_blue.SPAWN_LOCATION[1]+10))
        elif self.color == "orange":
            self.friendly_castle = castle_orange
            self.image = pygame.image.load("images/Rogue orange.png")
            self.rect = self.image.get_rect(
                center=(castle_orange.SPAWN_LOCATION[0], castle_orange.SPAWN_LOCATION[1]+10))

        self.stats["gold_steal"] = 2

    def special(self):
        """This is the Rogue special ability. He can steal gold from castles."""
        if self.collide_with(self.enemy_castle) and self.attack_time:
            if self.enemy_castle.stats["gold"] > 15:
                self.enemy_castle.stats["gold"] -= self.stats["gold_steal"]
                self.friendly_castle.stats["gold"] += self.stats["gold_steal"]


class Shieldsman(Troop):
    cost = 20

    def __init__(self, color_):
        super(Shieldsman, self).__init__(color_)
        self.color = color_
        self.stats = {
            "speed": 1,
            "damage": 5,
            "health": 200,
            "max health": 200,
            "attack_speed": 1.5,
            "melee": True,
            "range_immune": True,  # this is essentially his special: immune to ranged attacks
        }
        if self.color == "blue":
            self.image = pygame.image.load("images/Shieldsman blue.png")
            self.rect = self.image.get_rect(
                center=(castle_blue.SPAWN_LOCATION[0], castle_blue.SPAWN_LOCATION[1]))
        elif self.color == "orange":
            self.image = pygame.image.load("images/Shieldsman orange.png")
            self.rect = self.image.get_rect(
                center=(castle_orange.SPAWN_LOCATION[0], castle_orange.SPAWN_LOCATION[1]))


class Wizard(Troop):
    cost = 30

    def __init__(self, color_):
        super(Wizard, self).__init__(color_)
        self.color = color_
        self.stats = {
            "speed": 1,
            "damage": 40,
            "health": 60,
            "max health": 60,
            "attack_speed": 1.5,
            "melee": False,
            "range": 250,
            "weapon": Fireball,
            "range_immune": False
        }
        if self.color == "blue":
            self.image = pygame.image.load("images/Mage blue.png")
            self.rect = self.image.get_rect(
                center=(castle_blue.SPAWN_LOCATION[0], castle_blue.SPAWN_LOCATION[1]))
        elif self.color == "orange":
            self.image = pygame.image.load("images/Mage orange.png")
            self.rect = self.image.get_rect(
                center=(castle_orange.SPAWN_LOCATION[0], castle_orange.SPAWN_LOCATION[1]))


class Archer(Troop):
    cost = 15

    def __init__(self, color_):
        super(Archer, self).__init__(color_)
        self.color = color_
        self.stats = {
            "speed": 1,
            "damage": 10,
            "health": 100,
            "max health": 100,
            "attack_speed": 0.5,
            "melee": False,
            "range": 200,
            "weapon": Arrow,
            "range_immune": False
        }
        if self.color == "blue":
            self.image = pygame.image.load("images/Archer blue.png")
            self.rect = self.image.get_rect(
                center=(castle_blue.SPAWN_LOCATION[0], castle_blue.SPAWN_LOCATION[1]))
        elif self.color == "orange":
            self.image = pygame.image.load("images/Archer orange.png")
            self.rect = self.image.get_rect(
                center=(castle_orange.SPAWN_LOCATION[0], castle_orange.SPAWN_LOCATION[1]))


class Background:
    """The entire background"""
    def __init__(self):
        # main background picture
        self.background_image = pygame.image.load("images/Background.png").convert()
        # cloud image and variables
        self.cloud = pygame.image.load("images/Clouds.png")
        self.cloud_rect = self.cloud.get_rect(
            center=(random.randint(400, width-400), random.randint(50, 100))
        )
        self.cloud_direction = [random.randint(-2, -1), random.randint(1, 2)][random.randint(0, 1)]
        # only moves x directions

    def clouds(self):
        self.cloud_rect = self.cloud_rect.move(self.cloud_direction, 0)
        display.blit(self.cloud, self.cloud_rect)
        if -50 > self.cloud_rect.right:
            self.cloud_direction = random.randint(1, 2)
        elif width+50 < self.cloud_rect.left:
            self.cloud_direction = random.randint(-2, -1)

    def background(self):
        display.blit(self.background_image, (0, 0))

    @staticmethod
    def path():
        """Draws the path that troops walk on"""
        # draw path
        pygame.draw.rect(display, (191, 144, 0), (0, height-10, width, 10))
        # possibly make a picture for this later,


class Menu:
    def __init__(self):
        # menu picture - shows troop name
        self.menu_image = pygame.image.load("images/Menu.png")
        # is the menu active or not?
        self.menu_active = True
        # buttons on menu
        self.exit_button = None
        self.resume_button = None
        self.home_button = None

    def menu(self):
        display.blit(self.menu_image, (0, 0))
        # blue side
        # Swordsman
        text(display, (0, 0, 0), Rect(width*0.07, 240, 0, 0), "Swordsman".format(Swordsman.cost), 15)  # name
        text(display, (0, 0, 0), Rect(width*0.07, 255, 0, 0), "Cost: {}".format(Swordsman.cost), 15)  # cost
        # Rogue
        text(display, (0, 0, 0), Rect(width*0.15, 240, 0, 0), "Rogue: {}".format(Rogue.cost), 15)
        text(display, (0, 0, 0), Rect(width*0.15, 255, 0, 0), "Cost: {}".format(Rogue.cost), 15)
        # Shieldsman
        text(display, (0, 0, 0), Rect(width*0.24, 240, 0, 0), "Shieldsman: {}".format(Shieldsman.cost), 15)
        text(display, (0, 0, 0), Rect(width*0.24, 255, 0, 0), "Cost: {}".format(Shieldsman.cost), 15)
        # Archer
        text(display, (0, 0, 0), Rect(width*0.33, 240, 0, 0), "Archer: {}".format(Archer.cost), 15)
        text(display, (0, 0, 0), Rect(width*0.33, 255, 0, 0), "Cost: {}".format(Archer.cost), 15)
        # Wizard
        text(display, (0, 0, 0), Rect(width*0.42, 290, 0, 0), "Wizard: {}".format(Wizard.cost), 15)
        text(display, (0, 0, 0), Rect(width*0.42, 255, 0, 0), "Cost: {}".format(Wizard.cost), 15)


def game_setup():
    """Essentially just defining a bunch of variables. This function NOT to be called in a loop"""
    # this just defines a bunch of variables
    global castle_blue, castle_orange, blue_troops, orange_troops, troops, background_instance, \
        particle_list, projectile_list, projectile_list_blue, projectile_list_orange, menu_instance

    # game setup
    # make  background
    background_instance = Background()
    # make menu
    menu_instance = Menu()

    # define troop list (used in castle initiating, so we have to define this before castle defining)
    blue_troops = []
    orange_troops = []
    # make the castles

    castle_blue = Castle([K_q, K_w, K_e, K_r, K_t], "blue", blue_troops)
    castle_orange = Castle([K_y, K_u, K_i, K_o, K_p], "orange", orange_troops)
    # combine the two troop lists
    troops = blue_troops + orange_troops  # creates a shallow copy of the two troops list. Shallow copy is wanted

    particle_list = []  # we define these as globals instead of class instance variables
    projectile_list_blue = []  # so they won't be deleted when instance is deleted
    projectile_list_orange = []  # have to be defined separately

    projectile_list = projectile_list_blue + projectile_list_orange


def menu():
    # a nice background to the menu
    background_instance.background()  # everything normally continuing for the background
    # draw the clouds
    background_instance.clouds()
    # draw castles
    castle_blue.draw()
    castle_orange.draw()
    # draw the path
    background_instance.path()

    menu_instance.menu()


def game():
    """Uses variables defined in game_setup by calling their methods and more. This function to be called in a loop"""
    global troops, blue_troops, orange_troops, projectile_list, projectile_list_blue, projectile_list_orange

    if not menu_instance.menu_active:
        # do stuff for background
        background_instance.background()

        # draw the clouds
        background_instance.clouds()

        # draw castles
        castle_blue.draw()
        castle_orange.draw()

        castle_blue.spawn_troop()
        castle_orange.spawn_troop()

        # update the troop list after being modified by the castles. Also filter
        # then filter "root" lists
        blue_troops = [troop for troop in castle_blue.troop_list if not troop.dead]
        orange_troops = [troop for troop in castle_orange.troop_list if not troop.dead]

        # draw troops
        for troop in troops:
            troop.all()
            # now write in the special abilities
            troop.special()
        # combine the two troop lists
        troops = blue_troops + orange_troops
        # draw particles
        Troop.handle_particles()

        # draw the path
        background_instance.path()
    else:
        menu()


def main():
    game_setup()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == K_SPACE:
                    menu_instance.menu_active = True

        game()

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
