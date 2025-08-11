import pygame
import math


# ---------- constants ----------
WIDTH, HEIGHT = 800, 600
BORDER        = 80            # 80-px margin on each side
ROTATION_SPEED = 3            # degrees per frame for rotation
MOVE_SPEED = 3                # pixels per frame for forward/backward movement


# ---------- setup ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Continuous key-hold movement")
clock = pygame.time.Clock()


ship = pygame.image.load("arcade-game.png").convert_alpha()
SW, SH = ship.get_size()      # 64×64


# start near bottom-center
x = (WIDTH - SW) // 2
y = HEIGHT - SH - BORDER
angle = 0  # current rotation angle in degrees (0 = spaceship pointing up/north visually)


# pre-computed movement limits (top-left corner of sprite)
x_min = BORDER
x_max = WIDTH  - BORDER - SW
y_min = BORDER
y_max = HEIGHT - BORDER - SH


# ---------- key-state flags ----------
rotating_left = rotating_right = moving_forward = moving_backward = False


running = True
while running:
    # ---- event handling ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        elif event.type == pygame.KEYDOWN:
            # set movement flags based on key pressed
            if   event.key == pygame.K_LEFT:  
                rotating_left = True
                print("LEFT arrow key pressed - Rotating LEFT")
            elif event.key == pygame.K_RIGHT: 
                rotating_right = True
                print("RIGHT arrow key pressed - Rotating RIGHT")
            elif event.key == pygame.K_UP:    
                moving_forward = True
                print("UP arrow key pressed - Moving FORWARD")
            elif event.key == pygame.K_DOWN:  
                moving_backward = True
                print("DOWN arrow key pressed - Moving BACKWARD")


        elif event.type == pygame.KEYUP:
            if   event.key == pygame.K_LEFT:  
                rotating_left = False
                print("LEFT arrow key released - Stopped rotating LEFT")
            elif event.key == pygame.K_RIGHT: 
                rotating_right = False
                print("RIGHT arrow key released - Stopped rotating RIGHT")
            elif event.key == pygame.K_UP:    
                moving_forward = False
                print("UP arrow key released - Stopped moving FORWARD")
            elif event.key == pygame.K_DOWN:  
                moving_backward = False
                print("DOWN arrow key released - Stopped moving BACKWARD")


    # ---- rotation ----
    if rotating_left:
        angle += ROTATION_SPEED
        print(f"Rotating left - Current angle: {angle}°")
    if rotating_right:
        angle -= ROTATION_SPEED
        print(f"Rotating right - Current angle: {angle}°")
    
    # ---- movement based on current angle ----
    if moving_forward or moving_backward:
        # Convert angle to radians for math functions
        angle_rad = math.radians(angle)
        
        # Calculate movement direction - adjusted for spaceship pointing up at angle=0
        # For spaceship pointing up: use sin for x-direction, cos for y-direction
        direction_x = -math.sin(angle_rad)      # sin gives horizontal movement
        direction_y = -math.cos(angle_rad)     # -cos gives vertical movement (negative because pygame Y increases downward)
        
        if moving_forward:
            new_x = x + direction_x * MOVE_SPEED
            new_y = y + direction_y * MOVE_SPEED
            print(f"Moving forward at angle {angle}° - Direction: ({direction_x:.2f}, {direction_y:.2f})")
        else:  # moving_backward
            new_x = x - direction_x * MOVE_SPEED
            new_y = y - direction_y * MOVE_SPEED
            print(f"Moving backward at angle {angle}° - Direction: ({-direction_x:.2f}, {-direction_y:.2f})")
        
        # Apply boundary constraints
        x = max(x_min, min(x_max, new_x))
        y = max(y_min, min(y_max, new_y))


    # ---- drawing ----
    screen.fill((0, 0, 0))                     # clear screen
    
    # Rotate the ship image based on current angle
    rotated_ship = pygame.transform.rotate(ship, angle)
    # Get the rect of the rotated image to center it properly
    rotated_rect = rotated_ship.get_rect(center=(x + SW//2, y + SH//2))
    
    screen.blit(rotated_ship, rotated_rect)    # draw rotated ship
    pygame.display.flip()


    clock.tick(60)  # 60 FPS → 3° rotation/frame, 3 px movement/frame


pygame.quit()

