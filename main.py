import turtle

screen = turtle.Screen()
screen.title("Breakout Game")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)  # Turn off automatic updates

score = 0
lives = 3
max_speed = 6

score_display = turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-350, 260)
score_display.write(f"Score: {score}  Lives: {lives}", align="left", font=("Arial", 16, "normal"))

# Paddle setup (LONGER PADDLE)
paddle = turtle.Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=7)
paddle.penup()
paddle.goto(0, -250)

# Ball setup
ball = turtle.Turtle()
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, -100)
ball.dx = 2
ball.dy = 2

# Brick setup
bricks = []
colors = ["red", "orange", "yellow", "green", "blue"]

for row in range(5):
    for col in range(-5, 6):
        brick = turtle.Turtle()
        brick.shape("square")
        brick.color(colors[row])
        brick.shapesize(stretch_wid=1, stretch_len=3)
        brick.penup()
        brick.goto(col * 70, 200 - (row * 30))
        bricks.append(brick)

# Paddle movement
def move_left():
    x = paddle.xcor()
    if x > -320:
        paddle.setx(x - 30)

def move_right():
    x = paddle.xcor()
    if x < 320:
        paddle.setx(x + 30)

# Listen for keyboard input
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")

# Function to update score and lives display
def update_display():
    score_display.clear()
    score_display.write(f"Score: {score}  Lives: {lives}", align="left", font=("Arial", 16, "normal"))

# Function to increase ball speed
def increase_speed():
    if abs(ball.dx) < max_speed:
        ball.dx *= 1.05
        ball.dy *= 1.05

# Function to handle Game Over
def display_message(message):
    screen.clear()
    screen.bgcolor("black")
    message_display = turtle.Turtle()
    message_display.color("white")
    message_display.penup()
    message_display.hideturtle()
    message_display.goto(0, 0)
    message_display.write(message, align="center", font=("Arial", 30, "bold"))
    turtle.done()

# Game loop
game_running = True
while game_running:
    screen.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Bounce off walls
    if ball.xcor() > 380:
        ball.setx(380)
        ball.dx *= -1

    if ball.xcor() < -380:
        ball.setx(-380)
        ball.dx *= -1

    # Bounce off the top wall
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -230 and ball.ycor() > -240 and (paddle.xcor() - 80 < ball.xcor() < paddle.xcor() + 80):
        relative_position = (ball.xcor() - paddle.xcor()) / 80  # Normalize position (-1 to 1)
        ball.dy = abs(ball.dy)  # Always bounce upwards
        ball.dx = relative_position * 4  # Adjust horizontal bounce
        increase_speed()

    # Ball falls below paddle (lose a life)
    if ball.ycor() < -290:
        lives -= 1
        update_display()
        ball.goto(0, -100)
        ball.dx = 2
        ball.dy = 2
        if lives == 0:
            display_message("GAME OVER")
            game_running = False

    # Collision with bricks
    for brick in bricks:
        if abs(ball.xcor() - brick.xcor()) < 35 and abs(ball.ycor() - brick.ycor()) < 15:
            ball.dy *= -1
            brick.goto(1000, 1000)
            bricks.remove(brick)
            score += 10
            update_display()
            increase_speed()
            break

    # Check if all bricks are destroyed
    if len(bricks) == 0:
        display_message("YOU WIN!")
        game_running = False
