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
        # Load the image
        self.image = pygame.image.load(os.path.join('sprites', 'main.png'))
        # Scale the image by 50%
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 1.5), int(self.image.get_height() * 1.5)))
        self.player_pos = pygame.Vector2(self.image.get_width(), screen.get_height() - self.image.get_height() / 2)
        # Initialize the rectangle with placeholder values
        self.rect = pygame.Rect(50, 50, 50, 50)

    def render(self):
        # Adjust rectangle size based on the scaled image size
        if self.direction:
            self.rect.x = self.player_pos.x + 130 * 1.5  # Adjusted for the scaling
            self.rect.y = self.player_pos.y + 140 * 1.5  # Adjusted for the scaling
            self.rect.width = self.image.get_width() - 200 * 1.5  # Adjusted for the scaling
            self.rect.height = self.image.get_height() - 300 * 1.5  # Adjusted for the scaling
            screen.blit(self.image, self.player_pos)
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.player_pos)
            # Calculate the new rect position for the flipped image, adjusting for scaling
            self.rect.x = self.player_pos.x + (self.image.get_width() - (130 * 1.5 + self.rect.width))  # Adjust the rect.x for flipped
            self.rect.y = self.player_pos.y + 140 * 1.5  # Adjusted for the scaling
            # Width and height remain the same, but x, y are adjusted




# Define the bullet class to create bullets
class FallingObject:
    def __init__(self, image):
        self.image = pygame.transform.scale(pygame.image.load(image), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = random.randint(100, 1000)

    def render(self):
        
        if self.rect.y < screen.get_height():
            self.rect.y += 500 * dt
            # pygame.draw.rect(screen, "red", self.rect)
        else:
            return False
        
        screen.blit(self.image, self.rect)
        return True
    
class Button:
    def __init__(self, x, y, width, height, text=None, color=(73, 73, 73), text_color=(0, 0, 0), font_size=30, font_name="monospace"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.SysFont(font_name, font_size)

    def draw(self, win):
        # Draw the button rectangle
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text:
            # Add text to the button
            text_surf = self.font.render(self.text, True, self.text_color)
            win.blit(text_surf, ((self.x + (self.width/2 - text_surf.get_width()/2)), (self.y + (self.height/2 - text_surf.get_height()/2))))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

restart_button = Button(screen.get_width() / 2 - 100, screen.get_height() / 2 + 100, 200, 50, "Restart", color=(0, 255, 0))
# Load your sprite image
my_sprite = PlayerSprite()
falling_objects = []
myfont = pygame.font.SysFont("monospace", 25, True)
timer_font = pygame.font.SysFont("monospace", 50, True)
score = 0
gamestate = "menu"

#life
player_life = 0

# Timer variables
spawn_timer = 0
spawn_delay = 1  # Delay between spawns in milliseconds

nitro_container = 1000
nitro_max = 1000

images = [os.path.join('sprites', f'falling_obect{i}.png') for i in range(1, 5)]

background_image = pygame.image.load(os.path.join('sprites', 'background.png'))

start_ticks=pygame.time.get_ticks() #starter tick

countdown_time = 60  # 60 seconds for countdown
start_ticks = pygame.time.get_ticks()  # Start tick for tracking time

# Load heart sprite
heart_image = pygame.image.load(os.path.join('sprites', 'hearts.png'))
heart_image = pygame.transform.scale(heart_image, (30, 30))

timer_ui = pygame.image.load(os.path.join('sprites', 'timer_ui.png'))



while running:
    current_ticks = pygame.time.get_ticks()
    seconds_passed = (current_ticks - start_ticks) / 1000  # Convert milliseconds to seconds

    # Update countdown time
    remaining_time = max(0, countdown_time - seconds_passed)  # Ensure remaining time doesn't go below 0



    # Handle player input
    keys = pygame.key.get_pressed()
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if restart_button.is_over(mouse_pos):
                print("pressed!")
                game_sense = "menu"
                player_life = 5
                start_ticks = pygame.time.get_ticks()
                score = 0
                spawn_delay = 1
                falling_objects.clear()
                nitro_container = nitro_max

    if seconds_passed < 60 and player_life > 0:

        # Update timer
        spawn_timer += dt

        # Spawn a new falling object if enough time has passed
        if spawn_timer >= spawn_delay:
            # print("spawned!")
            falling_objects.append(FallingObject(random.choice(images)))
            spawn_timer = 0  # Reset timer

        if nitro_container >= nitro_max:
            nitro_container = 1000

        # Fill the screen with a color to wipe away anything from the last frame
        screen.blit(background_image, (0, 0))  # Purple color
    

        # Render the sprite
        my_sprite.render()

        # Draw hearts for player life
        for i in range(player_life):
            screen.blit(heart_image, (50 + i * 35, 50))

        label = myfont.render(f"Score: {score} | Highscore: " + highscore, 1, (255,255,0))
        screen.blit(label, (50, 80))

        # difficulty_label = myfont.render(f"Difficulty: {spawn_delay:.2f}", 1, (255,255,0))
        # screen.blit(difficulty_label, (500, 300))

   
        # Update timer label
        timer_text = f"{int(remaining_time)}"  # Convert to int to display whole seconds
        timer_label = timer_font.render(timer_text, 1, (255, 255, 255))

        # Draw timer label in the top right corner
        screen.blit(timer_ui, (screen.get_width() - timer_ui.get_width() - 70, 50))
        screen.blit(timer_label, (screen.get_width() - timer_ui.get_width() - 50, 50))





        cooldown_label = myfont.render(f"Nitro: {nitro_container:.2f} | {nitro_max}", 1, (255,255,0))
        screen.blit(cooldown_label, (50, 600))

        # Render and update falling objects
        for obj in falling_objects:
            if not obj.render() or obj.rect.y == screen.get_height():
                falling_objects.remove(obj)
                player_life -= 1
                print("life depleted!")

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
            gamestate = "gameover"

        

        pygame.display.flip()

        # Limit FPS to 60
        dt = clock.tick(60) / 1000
        spawn_delay -= 0.01 * dt
        # print(spawn_delay)

        # print(my_sprite.player_pos.x)
    else:
        # Flip() the display to put your work on the screen
        screen.fill((0, 0, 0)) 

        gameover_label = pygame.font.SysFont("monospace", 100, True)
    
        label = gameover_label.render("GAME OVER", 1, (255,0,0))
        screen.blit(label, ((screen.get_width() - label.get_width()) / 2, (screen.get_height() - label.get_height()) / 2 ))


        restart_button.draw(screen)

        if(score >= int(highscore)):
            score_label = myfont.render(f"New Highscore: {score}", 1, (255,0,0))
            screen.blit(score_label, ((screen.get_width() - label.get_width()) / 2 + 100, (screen.get_height() - label.get_height()) / 2 + 100))

        elif(score > int(highscore)):
            write_highscore = open("highscore.txt", "w+")
            write_highscore.write(str(score))
            write_highscore.close()

            file_highscore = open("highscore.txt", "r")
            highscore = file_highscore.readline()
            file_highscore.close()
           

        else:
            score_label = myfont.render(f"score: {score}", 1, (255,0,0))
            screen.blit(score_label, ((screen.get_width() - label.get_width()) / 2 + 200, (screen.get_height() - label.get_height()) / 2 + 100))

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
