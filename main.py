import pygame
import os
import random

if os.path.exists("highscore.txt"):
    file_highscore = open("highscore.txt", "r")
    highscore = file_highscore.readline()
    if(highscore == ''):
        highscore = "0"
else:
    file_highscore = open("highscore.txt", "x")
    highscore = "0"


file_highscore.close()
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Define the sprite class
class PlayerSprite:
    def __init__(self):
        self.direction = True
        self.image = pygame.image.load(os.path.join('sprites', 'main.png'))
        self.player_pos = pygame.Vector2(self.image.get_width(), screen.get_height() - self.image.get_height() / 2 )
        self.rect = pygame.Rect(50, 50, 50, 50)

    def render(self):
        if self.direction:
            screen.blit(self.image, self.player_pos)
        else:
            screen.blit(pygame.transform.flip(self.image, True, False), self.player_pos)

        self.rect.x = self.player_pos.x 
        self.rect.y = self.player_pos.y
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()*0.25 / 2 

        pygame.draw.rect(screen, "red", self.rect)

# Define the bullet class to create bullets
class FallingObject:
    def __init__(self):
        self.x = random.randint(40, 1240)
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, 60, 60)

    def render(self):
        if self.rect.y < screen.get_height():
            self.rect.y += 500 * dt
            pygame.draw.rect(screen, "red", self.rect)
        else:
            return False
        return True
    


# Load your sprite image
my_sprite = PlayerSprite()
falling_objects = []
myfont = pygame.font.SysFont("monospace", 15)
score = 0
gameover = True

#life
player_life = 5

# Timer variables
spawn_timer = 0
spawn_delay = 1.5  # Delay between spawns in milliseconds

nitro_container = 1000
nitro_max = 1000

while running:
    # Handle player input
    keys = pygame.key.get_pressed()
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE and my_sprite.player_pos.x > 0 and my_sprite.player_pos.x + my_sprite.image.get_width() < 1280 and nitro_container != 0:
        #         print("Pressed")
        #         print(my_sprite.direction)
        #         if my_sprite.direction:
        #             if my_sprite.player_pos.x + my_sprite.image.get_width() + 500 > 1280:
        #                 my_sprite.player_pos.x = 1280 - my_sprite.image.get_width()
        #             else:
        #                 my_sprite.player_pos.x += 500 * dt
        #         else:
        #             if my_sprite.player_pos.x - 500 < 0:
        #                 my_sprite.player_pos.x = 0
        #             else:
        #                 my_sprite.player_pos.x -= 500 * dt
                
        #         nitro_container -= 100 * dt
            

    if gameover:

        # Update timer
        spawn_timer += dt

        # Spawn a new falling object if enough time has passed
        if spawn_timer >= spawn_delay:
            # print("spawned!")
            falling_objects.append(FallingObject())
            spawn_timer = 0  # Reset timer

        if nitro_container >= nitro_max:
            nitro_container = 1000

        # Fill the screen with a color to wipe away anything from the last frame
        screen.fill((128, 0, 128))  # Purple color
    

        # Render the sprite
        my_sprite.render()

        label = myfont.render(f"Score: {score} | Highscore: " + highscore, 1, (255,255,0))
        screen.blit(label, (100, 200))

        life_label = myfont.render(f"Player Life: {player_life}", 1, (255,255,0))
        screen.blit(life_label, (100, 100))

        difficulty_label = myfont.render(f"Difficulty: {spawn_delay:.2f}", 1, (255,255,0))
        screen.blit(difficulty_label, (100, 300))


        cooldown_label = myfont.render(f"Nitro: {nitro_container:.2f} | {nitro_max}", 1, (255,255,0))
        screen.blit(cooldown_label, (100, 500))

        # Render and update falling objects
        for obj in falling_objects:
            if not obj.render() or obj.y == screen.get_height():
                falling_objects.remove(obj)
                player_life -= 1
                print("life depleted!")

        # Collision detection
        for obj in falling_objects:
            if my_sprite.rect.colliderect(obj.rect):
                print("Caught!!")
                falling_objects.remove(obj)
                score+=1


        if keys[pygame.K_LEFT] and my_sprite.player_pos.x > 0:
            my_sprite.player_pos.x -= 500 * dt
            my_sprite.direction = False
        if keys[pygame.K_RIGHT] and my_sprite.player_pos.x < 1280 - my_sprite.image.get_width():
            my_sprite.player_pos.x += 500 * dt
            my_sprite.direction = True

        if keys[pygame.K_SPACE] and my_sprite.player_pos.x > 0 and my_sprite.player_pos.x + my_sprite.image.get_width() < 1280 and nitro_container > 0:
            print("Pressed")
            print(my_sprite.direction)
            if my_sprite.direction:
                if my_sprite.player_pos.x > 1280:
                    my_sprite.player_pos.x = 1280 - my_sprite.image.get_width()
                else:
                    my_sprite.player_pos.x += 1000 * dt
            else:
                if my_sprite.player_pos.x  < 0:
                    my_sprite.player_pos.x = 0
                else:
                    my_sprite.player_pos.x -= 1000 * dt

            nitro_container -= 500 * dt if nitro_container > 0 else 0

        else:
            nitro_container += 100 * dt

        if player_life == 0:
            gameover = False

        

        # Flip() the display to put your work on the screen
        pygame.display.flip()

        # Limit FPS to 60
        dt = clock.tick(60) / 1000
        spawn_delay -= 0.01 * dt
        print(spawn_delay)

        # print(my_sprite.player_pos.x)
    else:
        # Flip() the display to put your work on the screen
        screen.fill((0, 0, 0)) 

        gameover_label = pygame.font.SysFont("monospace", 100, True)
    
        label = gameover_label.render("GAMEOVER", 1, (255,0,0))
        screen.blit(label, ((screen.get_width() - label.get_width()) / 2, (screen.get_height() - label.get_height()) / 2))

        pygame.display.flip()

        # Limit FPS to 15
        dt = clock.tick(15) / 1000


print(highscore)
print("done printing!")

if(score > int(highscore)):
    write_highscore = open("highscore.txt", "w+")
    write_highscore.write(str(score))
    write_highscore.close()
    



pygame.quit()
