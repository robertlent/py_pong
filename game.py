import pygame
import random

# Initialize pygame
pygame.init()

screen_info = pygame.display.Info()

# Game constants
WIDTH, HEIGHT = screen_info.current_w * \
    0.86, int((screen_info.current_w / 16) * 8.6)

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player scores
left_player_score = 0
right_player_score = 0

# Ball variables
radius = 15
ball_x, ball_y = (WIDTH / 2) - radius, (HEIGHT / 2) - radius
ball_vel_x, ball_vel_y = 0.7, 0.7

# Clone ball variables
clone_ball_x, clone_ball_y = (WIDTH / 2) - radius, (HEIGHT / 2) - radius
clone_ball_vel_x, clone_ball_vel_y = 0.7, 0.7

direction = [0, 1]
angle = [0, 1, 2]

# Paddle variables
paddle_width, paddle_height = 20, 120
left_paddle_x, right_paddle_x = 100 - \
    (paddle_width / 2), WIDTH - (100 - paddle_width / 2)
left_paddle_y = None
right_paddle_y = None
left_paddle_vel = right_paddle_vel = 0

# Powerup variables
left_powerup_clone = right_powerup_clone = False
left_powerup_smash = right_powerup_smash = False
left_powerup_extend = right_powerup_extend = False
left_powerup_clone_remaining = right_powerup_clone_remaining = 3
left_powerup_smash_remaining = right_powerup_smash_remaining = 3
left_powerup_extend_remaining = right_powerup_extend_remaining = 3

run = True


# Main game loop
def main():
    global left_paddle_y, right_paddle_y, run
    left_paddle_y = right_paddle_y = (HEIGHT / 2) - (paddle_height / 2)
    # Create game window
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Py-Pong")

    while run:

        # Handle events
        handle_events()

        # Apply game logic
        apply_logic()

        # Render game state
        render(window)

        # Update display
        pygame.display.update()


# Handle keyboard events
def handle_events():
    global left_paddle_vel, right_paddle_vel, left_powerup_extend_remaining, right_powerup_extend_remaining, left_powerup_extend, right_powerup_extend, left_powerup_clone, left_powerup_smash, right_powerup_clone, right_powerup_smash, run

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:

            # Player 1 controls
            if event.key == pygame.K_w:
                left_paddle_vel = -0.7

            if event.key == pygame.K_s:
                left_paddle_vel = 0.7

            if event.key == pygame.K_a and left_powerup_clone_remaining > 0:
                left_powerup_clone = True

            if event.key == pygame.K_d and left_powerup_smash_remaining > 0:
                left_powerup_smash = True

            if event.key == pygame.K_LCTRL and left_powerup_extend_remaining > 0:
                if not left_powerup_extend:
                    left_powerup_extend = True
                    left_powerup_extend_remaining -= 1

            # Player 2 controls
            if event.key == pygame.K_UP:
                right_paddle_vel = -0.6

            if event.key == pygame.K_DOWN:
                right_paddle_vel = 0.6

            if event.key == pygame.K_LEFT and right_powerup_clone_remaining > 0:
                right_powerup_clone = True

            if event.key == pygame.K_RIGHT and right_powerup_smash_remaining > 0:
                right_powerup_smash = True

            if event.key == pygame.K_RCTRL and right_powerup_extend_remaining > 0:
                if not right_powerup_extend:
                    right_powerup_extend = True
                    right_powerup_extend_remaining -= 1

            if event.key == pygame.K_ESCAPE:
                run = False

        # Reset paddle velocities
        if event.type == pygame.KEYUP:
            left_paddle_vel = 0
            right_paddle_vel = 0


# Update game state
def apply_logic():
    global left_paddle_y, right_paddle_y, ball_vel_x, ball_vel_y, clone_ball_vel_x, clone_ball_vel_y

    # Paddle collision with walls
    if left_paddle_y <= 0:
        left_paddle_y = 0

    if left_paddle_y >= HEIGHT - paddle_height * (2 if left_powerup_extend else 1):
        left_paddle_y = HEIGHT - paddle_height * \
            (2 if left_powerup_extend else 1)

    if right_paddle_y <= 0:
        right_paddle_y = 0

    if right_paddle_y >= HEIGHT - paddle_height * (2 if right_powerup_extend else 1):
        right_paddle_y = HEIGHT - paddle_height * \
            (2 if right_powerup_extend else 1)

    # Ball collision with walls
    if ball_y <= 0 + radius or ball_y >= HEIGHT - radius:
        ball_vel_y *= -1

    if clone_ball_y <= 0 + radius or clone_ball_y >= HEIGHT - radius:
        clone_ball_vel_y *= -1

    # Score and reset ball if ball goes off screen
    if ball_x >= WIDTH - radius:
        handle_left_score()

    if ball_x <= 0 + radius:
        handle_right_score()

    # Ball collision with paddles
    handle_ball_paddle_collision()

    # Update positions
    update_positions()


# Render current game state
def render(window):
    window.fill(BLACK)

    # Render scores
    render_scores(window)

    # Render powerups
    render_powerups(window)

    # Draw objects
    pygame.draw.circle(window, BLUE, (ball_x, ball_y), radius)
    pygame.draw.circle(window, BLUE, (clone_ball_x, clone_ball_y), radius)
    pygame.draw.rect(window, RED, pygame.Rect(left_paddle_x, left_paddle_y,
                     paddle_width, paddle_height * (2 if left_powerup_extend else 1)))
    pygame.draw.rect(window, RED, pygame.Rect(right_paddle_x, right_paddle_y,
                     paddle_width, paddle_height * (2 if right_powerup_extend else 1)))

    # Draw powerup indicators
    if left_powerup_clone:
        pygame.draw.circle(window, BLUE, (left_paddle_x + 10,
                           left_paddle_y + (paddle_height / 2)), 5)
        pygame.draw.circle(window, BLUE, (left_paddle_x + 10,
                           left_paddle_y + (paddle_height / 2) + 12), 5)

    if left_powerup_smash:
        pygame.draw.circle(
            window, WHITE, (left_paddle_x + 10, left_paddle_y + 10), 5)

    if right_powerup_clone:
        pygame.draw.circle(window, BLUE, (right_paddle_x +
                           10, right_paddle_y + (paddle_height / 2)), 5)
        pygame.draw.circle(window, BLUE, (right_paddle_x +
                           10, right_paddle_y + (paddle_height / 2) + 12), 5)

    if right_powerup_smash:
        pygame.draw.circle(
            window, WHITE, (right_paddle_x + 10, right_paddle_y + 10), 5)

    # Check if someone won
    check_win_condition(window)


# Handle left player scoring
def handle_left_score():
    global left_player_score, ball_vel_x, clone_ball_vel_x

    left_player_score += 1

    # Reset ball
    reset_ball()

    # Reset powerups
    reset_powerups()

    # Reverse ball direction
    ball_vel_x *= -1
    clone_ball_vel_x *= -1


# Handle right player scoring
def handle_right_score():
    global right_player_score, ball_vel_x, clone_ball_vel_x

    right_player_score += 1

    # Reset ball
    reset_ball()

    # Reset powerups
    reset_powerups()

    # Reverse ball direction
    ball_vel_x *= -1
    clone_ball_vel_x *= -1


# Reset ball to center
def reset_ball():
    global ball_x, ball_y, clone_ball_x, clone_ball_y

    ball_x, ball_y = (WIDTH / 2) - radius, (HEIGHT / 2) - radius
    clone_ball_x, clone_ball_y = (WIDTH / 2) - radius, (HEIGHT / 2) - radius

    # Randomize initial direction
    dir = random.choice(direction)
    ang = random.choice(angle)

    if dir == 0:
        set_ball_vel(ang, -1)
    if dir == 1:
        set_ball_vel(ang, 1)


# Set the ball velocity
def set_ball_vel(angle, direction):
    global ball_vel_x, ball_vel_y, clone_ball_vel_x, clone_ball_vel_y

    if angle == 0:
        ball_vel_y, ball_vel_x = direction * 1.4, 0.7
        clone_ball_vel_y, clone_ball_vel_x = direction * 1.4, 0.7

    if angle == 1:
        ball_vel_y, ball_vel_x = direction * 0.25, 0.25
        clone_ball_vel_y, clone_ball_vel_x = direction * 0.7, 0.7

    if angle == 2:
        ball_vel_y, ball_vel_x = direction * 0.7, 1.4
        clone_ball_vel_y, clone_ball_vel_x = direction * 0.7, 1.4


# Handle ball collision with paddles
def handle_ball_paddle_collision():
    global ball_vel_x, clone_ball_vel_x, clone_ball_vel_y

    # Left paddle
    if left_paddle_x <= ball_x <= left_paddle_x + paddle_width:
        if left_paddle_y <= ball_y <= left_paddle_y + paddle_height * (2 if left_powerup_extend else 1):
            handle_left_paddle_collision()

    # Right paddle
    if right_paddle_x <= ball_x <= right_paddle_x + paddle_width:
        if right_paddle_y <= ball_y <= right_paddle_y + paddle_height * (2 if right_powerup_extend else 1):
            handle_right_paddle_collision()


# Handle collision with left paddle
def handle_left_paddle_collision():
    global ball_vel_x, clone_ball_vel_x, clone_ball_vel_y, left_powerup_clone, left_powerup_smash

    ball_x = left_paddle_x + paddle_width
    clone_ball_x = left_paddle_x + paddle_width

    if left_powerup_clone and left_powerup_smash:
        smash_and_clone("left")
    elif left_powerup_smash:
        smash("left")
    elif left_powerup_clone:
        clone("left")
    else:
        ball_vel_x *= -1
        clone_ball_vel_x *= -1


# Handle collision with right paddle
def handle_right_paddle_collision():
    global ball_vel_x, clone_ball_vel_x, clone_ball_vel_y, right_powerup_clone, right_powerup_smash

    ball_x = right_paddle_x - radius
    clone_ball_x = right_paddle_x - radius

    if right_powerup_clone and right_powerup_smash:
        smash_and_clone("right")
    elif right_powerup_smash:
        smash("right")
    elif right_powerup_clone:
        clone("right")
    else:
        ball_vel_x *= -1
        clone_ball_vel_x *= -1


# Smash and clone effect
def smash_and_clone(player):
    global ball_vel_x, clone_ball_vel_x, clone_ball_vel_y, left_powerup_clone, left_powerup_smash, right_powerup_clone, right_powerup_smash

    ball_vel_x *= -2.5
    clone_ball_vel_x *= -2.5
    clone_ball_vel_y *= -2.5

    if player == 'left':
        use_left_powerups()
    else:
        use_right_powerups()


# Smash effect
def smash(player):
    global ball_vel_x, clone_ball_vel_x

    ball_vel_x *= -2.5
    clone_ball_vel_x *= -2.5

    if player == 'left':
        use_left_powerups()
    else:
        use_right_powerups()


# Clone effect
def clone(player):
    global ball_vel_x, clone_ball_vel_x, clone_ball_vel_y

    ball_vel_x *= -1
    clone_ball_vel_x *= -1
    clone_ball_vel_y *= -1

    if player == 'left':
        use_left_powerups()
    else:
        use_right_powerups()


# Use left powerups
def use_left_powerups():
    global left_powerup_clone, left_powerup_smash, left_powerup_clone_remaining, left_powerup_smash_remaining

    if left_powerup_clone:
        left_powerup_clone = False
        left_powerup_clone_remaining -= 1

    if left_powerup_smash:
        left_powerup_smash = False
        left_powerup_smash_remaining -= 1


# Use right powerups
def use_right_powerups():
    global right_powerup_clone, right_powerup_smash, right_powerup_clone_remaining, right_powerup_smash_remaining

    if right_powerup_clone:
        right_powerup_clone = False
        right_powerup_clone_remaining -= 1

    if right_powerup_smash:
        right_powerup_smash = False
        right_powerup_smash_remaining -= 1


# Reset powerups
def reset_powerups():
    global left_powerup_extend, right_powerup_extend

    left_powerup_extend = False
    right_powerup_extend = False


# Update object positions
def update_positions():
    global ball_x, ball_y, clone_ball_x, clone_ball_y, left_paddle_y, right_paddle_y

    ball_x += ball_vel_x
    ball_y += ball_vel_y

    clone_ball_x += clone_ball_vel_x
    clone_ball_y += clone_ball_vel_y

    left_paddle_y += left_paddle_vel
    right_paddle_y += right_paddle_vel


# Render scores
def render_scores(window):
    font = pygame.font.SysFont('None', 32)

    left_score = font.render(f"Score: {left_player_score}", True, WHITE)
    right_score = font.render(f"Score: {right_player_score}", True, WHITE)

    window.blit(left_score, (150, 25))
    window.blit(right_score, (WIDTH - 300, 25))


# Render powerups
def render_powerups(window):
    global left_powerup_clone_remaining, left_powerup_smash_remaining, right_powerup_clone_remaining, right_powerup_smash_remaining

    font = pygame.font.SysFont('None', 32)

    left_clones_remaining = font.render(f"{left_powerup_clone_remaining} " + (
        "clone" if left_powerup_clone_remaining == 1 else "clones"), True, WHITE)
    left_smashes_remaining = font.render(f"{left_powerup_smash_remaining} " + (
        "smash" if left_powerup_smash_remaining == 1 else "smashes"), True, WHITE)
    left_extends_remaining = font.render(f"{left_powerup_extend_remaining} " + (
        "extend" if left_powerup_smash_remaining == 1 else "extends"), True, WHITE)

    right_clones_remaining = font.render(f"{right_powerup_clone_remaining} " + (
        "clone" if right_powerup_clone_remaining == 1 else "clones"), True, WHITE)
    right_smashes_remaining = font.render(f"{right_powerup_smash_remaining} " + (
        "smash" if right_powerup_smash_remaining == 1 else "smashes"), True, WHITE)
    right_extends_remaining = font.render(f"{right_powerup_extend_remaining} " + (
        "extend" if right_powerup_smash_remaining == 1 else "extends"), True, WHITE)

    window.blit(font.render("Powerups:", True, WHITE), (150, 85))
    window.blit(left_clones_remaining, (150, 125))
    window.blit(left_smashes_remaining, (150, 165))
    window.blit(left_extends_remaining, (150, 205))

    window.blit(font.render("Powerups:", True, WHITE), (WIDTH - 300, 85))
    window.blit(right_clones_remaining, (WIDTH - 300, 125))
    window.blit(right_smashes_remaining, (WIDTH - 300, 165))
    window.blit(right_extends_remaining, (WIDTH - 300, 205))


# Check if someone won
def check_win_condition(window):
    if left_player_score >= 5:
        show_endscreen(window, "Player One Won!")

    if right_player_score >= 5:
        show_endscreen(window, "Player Two Won!")


# Show end screen
def show_endscreen(window, text):
    winning_font = pygame.font.SysFont('None', 100)

    window.fill(BLACK)
    endscreen = winning_font.render(text, True, WHITE)
    window.blit(endscreen, (WIDTH / 2 - 250, HEIGHT / 2))


if __name__ == "__main__":
    main()
